# import json
# import os
# from typing import Any, Dict, List, Optional
# import logging

# # Ensure logging is configured if it hasn't been already (optional, for safety)
# # logging.basicConfig(level=logging.INFO)

# class AppConfig:
#     """
#     Handles loading, parsing, and reloading of the application configuration 
#     from app_config.json.
#     """
#     def __init__(self, config_path: Optional[str] = None):
#         base_dir = os.path.dirname(__file__)
#         # Set the default path to app_config.json
#         self.CONFIG_PATH = os.path.join(base_dir, "app_config.json")
        
#         # Initialize internal state variables
#         self._config: Dict[str, Any] = {}
#         self.take_count_map: Dict[str, str] = {}
#         self.flowrack_no_map: Dict[str, str] = {}
#         self.maguchi_no_map: Dict[str, str] = {}
#         self.shelf_codes: Dict[str, List[str]] = {}
#         self.shelf_code_list_map: Dict[str, str] = {}
#         self.insert_target_ids_map: Dict[str, Any] = {}
        
#         # Load and process config upon initialization
#         self._load_and_process() 

#     def _load_from_file(self) -> Dict[str, Any]:
#         """Loads the raw dictionary from the JSON file."""
#         try:
#             with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
#                 return json.load(f)
#         except FileNotFoundError:
#             logging.error(f"Configuration file not found at: {self.CONFIG_PATH}")
#             return {}
#         except json.JSONDecodeError as e:
#             logging.error(f"Error decoding JSON in {self.CONFIG_PATH}: {e}")
#             return {}

#     def _process_config(self, data: Dict[str, Any]) -> None:
#         """Parses the raw loaded dictionary and sets all the map attributes."""
#         self._config = data
        
#         # Materialize sub-maps with sane defaults
#         self.take_count_map = self._config.get("take_count", {})
#         self.flowrack_no_map = self._config.get("flowrack_no", {})
#         self.maguchi_no_map = self._config.get("maguchi_no", {})
#         self.shelf_codes = self._config.get("shelf_codes", {})
#         self.shelf_code_list_map = self._config.get("shelf_code_list", {})
#         self.insert_target_ids_map = self._config.get("insert_target_ids", {})

#         # Optional: basic validation
#         self._validate()

#     def _load_and_process(self):
#         """Loads data from file and processes it."""
#         raw_data = self._load_from_file()
#         if raw_data:
#             self._process_config(raw_data)
        
#     def reload(self):
#         """Force a reload of the configuration from disk."""
#         logging.info(f"Reloading configuration from disk: {self.CONFIG_PATH}")
#         self._load_and_process()

#     def _validate(self) -> None:
#         """Performs basic validation on the loaded configuration structure."""
#         if not isinstance(self.take_count_map, dict):
#             raise ValueError("Config error: 'take_count' must be an object.")
#         if not isinstance(self.flowrack_no_map, dict):
#             raise ValueError("Config error: 'flowrack_no_map' must be an object.")
#         if not isinstance(self.maguchi_no_map, dict):
#             raise ValueError("Config error: 'maguchi_no_map' must be an object.")
#         if not isinstance(self.shelf_codes.get("R1_R2_L1_L2", []), list):
#             raise ValueError("Config error: 'shelf_codes.R1_R2_L1_L2' must be a list.")
#         if not isinstance(self.shelf_code_list_map, dict):
#             raise ValueError("Config error: 'shelf_code_list_map' must be an object.")
#         if not isinstance(self.insert_target_ids_map, dict):
#             raise ValueError("Config error: 'insert_target_ids' must be an object.")
        
#     # ---- Helper getters
#     def get_take_count(self, kanban_no: str) -> str:
#         """Return take_count for given kanban_no from the in-memory map."""
#         # Returns a default value of "-0" if not found
#         return self.take_count_map.get(kanban_no, "-0")

#     def get_flowrack_no(self, kanban_no: str) -> str:
#         """Return flowrack_no for given kanban_no from the in-memory map."""
#         return self.flowrack_no_map.get(kanban_no, "")

#     def get_maguchi_no(self, plat: int | str) -> str:
#         """Return maguchi_no for a given plat ID."""
#         # JSON keys are strings; ensure we look up the string key
#         key = str(plat)
#         return self.maguchi_no_map.get(key, "")

#     def get_shelf_codes_group(self, group_name: str) -> List[str]:
#         """Return a list of shelf codes for a given group name."""
#         return self.shelf_codes.get(group_name, [])

#     def get_shelf_code_by_flowrack_no(self, flowrack_no: str) -> str:
#         """Return the shelf code list for a given flowrack number."""
#         return self.shelf_code_list_map.get(flowrack_no, "")
    
#     def get_insert_target_ids(self, insert_target_ids: str) -> List[str]:
#         """Return insert_target_ids_map for given insert_target_ids from the in-memory map."""
#         # Returns a default value of "{}" if not found
#         return self.insert_target_ids_map.get(insert_target_ids, "{}")

#     # Expose raw config if needed
#     @property
#     def data(self) -> Dict[str, Any]:
#         """Returns the raw, fully loaded configuration dictionary."""
#         return self._config

import json
import os
from typing import Any, Dict, List, Optional
import logging

class AppConfig:
    """
    Handles loading, parsing, and reloading of the application configuration 
    from app_config.json with an automatic file watcher.
    """
    def __init__(self, config_path: Optional[str] = None):
        base_dir = os.path.dirname(__file__)
        # Set the default path to app_config.json
        self.CONFIG_PATH = config_path or os.path.join(base_dir, "app_config.json")
        
        # Initialize internal state variables
        self._config: Dict[str, Any] = {}
        self._last_mtime: float = 0  # Track last modification time for the watcher
        
        self.take_count_map: Dict[str, str] = {}
        self.flowrack_no_map: Dict[str, str] = {}
        self.maguchi_no_map: Dict[str, str] = {}
        self.shelf_codes: Dict[str, List[str]] = {}
        self.shelf_code_list_map: Dict[str, str] = {}
        self.insert_target_ids_map: Dict[str, Any] = {}
        
        # Initial load
        self.reload_if_changed()

    def reload_if_changed(self) -> None:
        """
        Checks if the file has been modified on disk.
        If yes, reloads the configuration into memory.
        """
        try:
            current_mtime = os.path.getmtime(self.CONFIG_PATH)
            if current_mtime > self._last_mtime:
                logging.info(f"Config change detected. Reloading: {self.CONFIG_PATH}")
                self._load_and_process()
                self._last_mtime = current_mtime
        except FileNotFoundError:
            logging.error(f"Configuration file not found at: {self.CONFIG_PATH}")
        except Exception as e:
            logging.error(f"Error checking config file timestamp: {e}")

    def _load_from_file(self) -> Dict[str, Any]:
        """Loads the raw dictionary from the JSON file."""
        try:
            with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in {self.CONFIG_PATH}: {e}")
            # Return current config to prevent wiping data on a typo
            return self._config 
        except Exception as e:
            logging.error(f"Error reading file {self.CONFIG_PATH}: {e}")
            return self._config

    def _process_config(self, data: Dict[str, Any]) -> None:
        """Parses the raw loaded dictionary and sets all the map attributes."""
        self._config = data
        
        # Materialize sub-maps with sane defaults
        self.take_count_map = self._config.get("take_count", {})
        self.flowrack_no_map = self._config.get("flowrack_no", {})
        self.maguchi_no_map = self._config.get("maguchi_no", {})
        self.shelf_codes = self._config.get("shelf_codes", {})
        self.shelf_code_list_map = self._config.get("shelf_code_list", {})
        self.insert_target_ids_map = self._config.get("insert_target_ids_map", {})

        # Basic validation
        self._validate()

    def _load_and_process(self):
        """Loads data from file and processes it."""
        raw_data = self._load_from_file()
        if raw_data:
            self._process_config(raw_data)
        
    def reload(self):
        """Force a manual reload of the configuration from disk."""
        logging.info(f"Force reloading configuration: {self.CONFIG_PATH}")
        self._load_and_process()
        if os.path.exists(self.CONFIG_PATH):
            self._last_mtime = os.path.getmtime(self.CONFIG_PATH)

    def _validate(self) -> None:
        """Performs basic validation on the loaded configuration structure."""
        maps_to_validate = [
            ("take_count", self.take_count_map),
            ("flowrack_no", self.flowrack_no_map),
            ("maguchi_no", self.maguchi_no_map),
            ("shelf_code_list", self.shelf_code_list_map),
            ("insert_target_ids_map", self.insert_target_ids_map)
        ]
        for name, obj in maps_to_validate:
            if not isinstance(obj, dict):
                logging.warning(f"Config error: '{name}' must be an object.")

    # ---- Helper getters (All call reload_if_changed for fresh data) ----

    def get_take_count(self, kanban_no: str) -> str:
        self.reload_if_changed()
        return self.take_count_map.get(kanban_no, "-0")

    def get_flowrack_no(self, kanban_no: str) -> str:
        self.reload_if_changed()
        return self.flowrack_no_map.get(kanban_no, "")

    def get_maguchi_no(self, plat: int | str) -> str:
        self.reload_if_changed()
        key = str(plat)
        return self.maguchi_no_map.get(key, "")

    def get_shelf_codes_group(self, group_name: str) -> List[str]:
        self.reload_if_changed()
        return self.shelf_codes.get(group_name, [])

    def get_shelf_code_by_flowrack_no(self, flowrack_no: str) -> str:
        self.reload_if_changed()
        return self.shelf_code_list_map.get(flowrack_no, "")
    
    def get_insert_target_ids_by_button(self, button_id: int | str) -> List[List[int]]:
        """
        Return signal mapping for given button_id.
        Automatically ignores '_comment' keys in JSON.
        """
        self.reload_if_changed()
        # Returns empty list if button_id not found
        return self.insert_target_ids_map.get(str(button_id), [])

    @property
    def data(self) -> Dict[str, Any]:
        """Returns the raw, fully loaded configuration dictionary."""
        self.reload_if_changed()
        return self._config