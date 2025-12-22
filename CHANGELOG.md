# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-12-19

### Added
- Created `AppConfig` class in `config/config_loader.py` to handle unified configuration.
- Added **File Watcher** logic to `AppConfig` to automatically reload JSON data when the file is modified on disk.
- Implemented `get_insert_target_ids_by_button` to automatically convert JSON lists to Python tuples for SQL compatibility.

### Changed
- Refactored `WCSRepository` to use `self.cfg` instead of hardcoded signal maps.
- Updated `DepalletAreaRepository` to remove manual `self.cfg.reload()` calls, improving performance.
- Optimized `update_take_count` API route to use atomic file writes (`os.replace`) to prevent file corruption.

### Fixed
- Fixed a crash in `insert_target_ids()` where a List was treated as a Dictionary.
- Standardized data types to ensure `signal_id` and `value` are handled as integers where required by the DB.

## [1.0.0] - 2025-12-01
### Added
- Initial release with basic Depallet and WCS repository logic.