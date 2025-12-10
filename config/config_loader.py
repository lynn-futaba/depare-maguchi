import json
import os
from typing import Any, Dict, List, Optional
import logging

# Ensure logging is configured if it hasn't been already (optional, for safety)
# logging.basicConfig(level=logging.INFO)

class AppConfig:
    """
    Handles loading, parsing, and reloading of the application configuration 
    from app_config.json.
    """
    def __init__(self, config_path: Optional[str] = None):
        base_dir = os.path.dirname(__file__)
        # Set the default path to app_config.json
        self.CONFIG_PATH = os.path.join(base_dir, "app_config.json")
        
        # Initialize internal state variables
        self._config: Dict[str, Any] = {}
        self.take_count_map: Dict[str, str] = {}
        self.flowrack_no_map: Dict[str, str] = {}
        self.maguchi_no_map: Dict[str, str] = {}
        self.shelf_codes: Dict[str, List[str]] = {}
        self.shelf_code_list_map: Dict[str, str] = {}
        
        # Load and process config upon initialization
        self._load_and_process() 

    def _load_from_file(self) -> Dict[str, Any]:
        """Loads the raw dictionary from the JSON file."""
        try:
            with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found at: {self.CONFIG_PATH}")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in {self.CONFIG_PATH}: {e}")
            return {}

    def _process_config(self, data: Dict[str, Any]) -> None:
        """Parses the raw loaded dictionary and sets all the map attributes."""
        self._config = data
        
        # Materialize sub-maps with sane defaults
        self.take_count_map = self._config.get("take_count", {})
        self.flowrack_no_map = self._config.get("flowrack_no", {})
        self.maguchi_no_map = self._config.get("maguchi_no", {})
        self.shelf_codes = self._config.get("shelf_codes", {})
        self.shelf_code_list_map = self._config.get("shelf_code_list", {})

        # Optional: basic validation
        self._validate()

    def _load_and_process(self):
        """Loads data from file and processes it."""
        raw_data = self._load_from_file()
        if raw_data:
            self._process_config(raw_data)
        
    def reload(self):
        """Force a reload of the configuration from disk."""
        logging.info(f"Reloading configuration from disk: {self.CONFIG_PATH}")
        self._load_and_process()

    def _validate(self) -> None:
        """Performs basic validation on the loaded configuration structure."""
        if not isinstance(self.take_count_map, dict):
            raise ValueError("Config error: 'take_count' must be an object.")
        if not isinstance(self.flowrack_no_map, dict):
            raise ValueError("Config error: 'flowrack_no_map' must be an object.")
        if not isinstance(self.maguchi_no_map, dict):
            raise ValueError("Config error: 'maguchi_no_map' must be an object.")
        if not isinstance(self.shelf_codes.get("R1_R2_L1_L2", []), list):
            raise ValueError("Config error: 'shelf_codes.R1_R2_L1_L2' must be a list.")
        if not isinstance(self.shelf_code_list_map, dict):
            raise ValueError("Config error: 'shelf_code_list_map' must be an object.")
        
    # ---- Helper getters
    def get_take_count(self, kanban_no: str) -> str:
        """Return take_count for given kanban_no from the in-memory map."""
        # Returns a default value of "-0" if not found
        return self.take_count_map.get(kanban_no, "-0")

    def get_flowrack_no(self, kanban_no: str) -> str:
        """Return flowrack_no for given kanban_no from the in-memory map."""
        return self.flowrack_no_map.get(kanban_no, "")

    def get_maguchi_no(self, plat: int | str) -> str:
        """Return maguchi_no for a given plat ID."""
        # JSON keys are strings; ensure we look up the string key
        key = str(plat)
        return self.maguchi_no_map.get(key, "")

    def get_shelf_codes_group(self, group_name: str) -> List[str]:
        """Return a list of shelf codes for a given group name."""
        return self.shelf_codes.get(group_name, [])

    def get_shelf_code_by_flowrack_no(self, flowrack_no: str) -> str:
        """Return the shelf code list for a given flowrack number."""
        return self.shelf_code_list_map.get(flowrack_no, "")

    # Expose raw config if needed
    @property
    def data(self) -> Dict[str, Any]:
        """Returns the raw, fully loaded configuration dictionary."""
        return self._config