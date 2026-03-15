# Changelog

All notable changes to this project will be documented in this file.

## [1.2.2] - 2026-03-15

### Fixed
- **Restored `latest_events` attribute**: The sensor's `extra_state_attributes` now includes a `latest_events` key that was inadvertently removed in v1.2.1.
  - On the first update, `latest_events` contains all events reported by the integration, ordered from most recent to oldest.
  - On subsequent updates, `latest_events` contains only the new events since the previous update, ordered from most recent to oldest.

### Changed
- **`format_events` service now reads from `latest_events`**: The `format_events` action now formats events sourced from the `latest_events` attribute (new events only per update) instead of the full cumulative `events` list.

## [1.2.1] - 2026-03-15

### Fixed
- **Sensor state "unknown"**: The sensor state was incorrectly showing `unknown` even when events were present. The root cause was that `entry.time` from `aio_geojson_usgs_earthquakes` is a `datetime` object, and the code tried to call `.replace("Z", "+00:00")` on it as if it were a string. `datetime.replace()` does not accept positional string arguments, causing a `TypeError` that was silently caught and left `_attr_native_value` as `None`.
- Removed erroneous `@callback` decorator from `async def _async_update_events` in `sensor.py` (correct pattern for async dispatcher callbacks).

### Changed
- Removed `formatted_events` attribute from the sensor's `extra_state_attributes`.
- Added new `format_events` action (service) that returns formatted earthquake events in a response variable (`formatted_events`). Call this action with a `response_variable` to get the human-readable text output.

## [1.2.0] - 2026-03-15

### Changed
- Changed integration domain from `usgs_quakes` to `usgs_earthquakes_feed` to override the built-in HA core integration of the same name
- Kept integration name as "USGS Quakes"
- Renamed `custom_components/usgs_quakes/` folder to `custom_components/usgs_earthquakes_feed/`
- Updated `manifest.json`, `hacs.json`, `mypy.ini`, and GitHub Actions workflow to reflect new domain
- Updated `README.md` references to new domain and sensor/service names
- Updated `STORAGE_KEY` and device identifiers to use `usgs_earthquakes_feed`
- Brand images remain in `custom_components/usgs_earthquakes_feed/brand/` for local brand image support
- Updated `README.md` with a prominent notice about the core integration override and a migration guide for users upgrading from `usgs_quakes` (v1.1.x)

## [1.1.5] - 2026-03-15

### Changed
- Moved `logo.png`, `logo@2x.png`, `icon.png`, and `icon@2x.png` to `custom_components/usgs_quakes/brand/`
- Updated README.md icon image link to reference new brand directory location

## [1.1.4] - 2025-12-11

### Fixed
- **Critical**: Added missing OptionsFlowHandler class to enable configuration changes through the UI
  - Users can now modify Radius, Minimum Magnitude, and Feed Type after initial setup
  - Fixed integration reload when options are updated

### Changed
- Enhanced README badge section with additional quality indicators
  - Added Ruff + Mypy + Hassfest combined workflow badge
  - Added Ruff quality badge
  - Added Mypy type checking badge
- Added "Proudly developed with GitHub Copilot" footer to README
- All badges now properly reference USGS_Quakes repository

### Quality
- Verified code passes all ruff linting checks
- Verified code passes all mypy type checks
- No code errors found - all Python files are compliant with configured standards

## [1.1.3] - Previous Release
- Previous version (details not available in current repository)
