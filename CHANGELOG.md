# Changelog

All notable changes to this project will be documented in this file.

## [1.2.6] - 2026-03-16

### Fixed
- **Conceptual error in v1.2.5**: `latest_events` was incorrectly made a cumulative list that grew on every update, always containing all historical events. The correct behaviour is:
  - `latest_events` contains **only the new events** detected in the current update cycle (events whose IDs have not been seen before).
  - On the **first run** (or after HA restarts), all events returned by the feed are considered new, so `latest_events` is populated with all of them.
  - On **subsequent runs** where no new earthquakes have been reported, `latest_events` is empty (`[]`), the sensor state does not change, and automations that trigger on state change are not fired.
  - When a **new earthquake** is detected, `latest_events` contains only that event (or those events), the sensor state updates to the most recent event's timestamp, and the automation is triggered.

### Changed
- Replaced the cumulative `_latest_events` accumulator with an internal `_seen_ids: set[str]` that tracks which event IDs have already been reported. This is not exposed as a sensor attribute.
- Removed the now-unused `MAX_EVENTS` constant from `sensor.py`.

## [1.2.5] - 2026-03-16

### Fixed
- **`latest_events` was always empty after the first update cycle**: The sensor previously maintained two separate lists — `events` (cumulative) and `latest_events` (new events only per cycle). Because `latest_events` was reset to only the newly-detected IDs on every update, it became empty whenever no brand-new earthquakes arrived, causing the `format_events` service to return an empty result.

### Changed
- **Removed `events` attribute from the sensor**: Seismic events are now exposed solely through the `latest_events` attribute, which accumulates all events (up to 50) ordered from most recent to oldest — mirroring the previous behaviour of the `events` attribute.
- **Diagnostics now report `latest_events`**: The diagnostics payload has been updated to expose `latest_events` instead of the removed `events` key.

## [1.2.4] - 2026-03-16

### Fixed
- **`OptionsFlowHandler` no longer raises `AttributeError` on reconfiguration**: Removed the `__init__` method from `OptionsFlowHandler` that tried to set `self.config_entry = config_entry`. In newer versions of Home Assistant, `config_entry` is a read-only property on `OptionsFlow` and is automatically injected by the framework. The `async_get_options_flow` method now returns `OptionsFlowHandler()` without passing `config_entry` manually.

## [1.2.3] - 2026-03-15

### Fixed
- **Redundant lambda wrappers removed from `sensor.py`**: Both `sorted()` calls that used `key=lambda e: parse_event_time(e)` now use `key=parse_event_time` directly, as suggested by code review.
- **`parse_event_time` now handles event dicts**: Updated `helpers.py` so that `parse_event_time` correctly extracts the `"time"` field when passed a full event dict, allowing it to be used directly as a sort key without an intermediate lambda.

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
