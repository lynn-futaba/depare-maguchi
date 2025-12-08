
# depare_maguchi/config/config_loader.py

import json
import os
from typing import Any, Dict, List, Optional

class AppConfig:
    def __init__(self, config_path: Optional[str] = None):
        base_dir = os.path.dirname(__file__)
        # default path: depare_maguchi/config/app_config.json
        self._config_path = config_path or os.path.join(base_dir, "app_config.json")

        with open(self._config_path, "r", encoding="utf-8") as f:
            self._config: Dict[str, Any] = json.load(f)

        # Materialize sub-maps with sane defaults
        self.take_count_map: Dict[str, str] = self._config.get("take_count", {})
        self.flowrack_no_map: Dict[str, str] = self._config.get("flowrack_no", {})
        self.maguchi_no_map: Dict[str, str] = self._config.get("maguchi_no", {})
        self.shelf_codes: Dict[str, List[str]] = self._config.get("shelf_codes", {})
        self.shelf_code_list_map: Dict[str, str] = self._config.get("shelf_code_list", {})

        # Optional: basic validation
        self._validate()

    def _validate(self) -> None:
        # Example validations; expand as needed
        if not isinstance(self.take_count_map, dict):
            raise ValueError("Config error: 'take_count' must be an object.")
        if not isinstance(self.shelf_codes.get("R1_R2_L1_L2", []), list):
            raise ValueError("Config error: 'shelf_codes.R1_R2_L1_L2' must be a list.")
        # Add more structural checks here…

    # ---- Helper getters
    def get_take_count(self, kanban_no: str) -> str:
        return self.take_count_map.get(kanban_no, "-0")

    def get_flowrack_no(self, kanban_no: str) -> str:
        return self.flowrack_no_map.get(kanban_no, "")

    def get_maguchi_no(self, plat: int | str) -> str:
        # JSON keys are strings; ensure we look up the string key
        key = str(plat)
        return self.maguchi_no_map.get(key, "")

    def get_shelf_codes_group(self, group_name: str) -> List[str]:
        return self.shelf_codes.get(group_name, [])

    def get_shelf_code_by_flowrack_no(self, flowrack_no: str) -> str:
        return self.shelf_code_list_map.get(flowrack_no, "")

    # Expose raw config if needed
    @property
    def data(self) -> Dict[str, Any]:
        return self._config
