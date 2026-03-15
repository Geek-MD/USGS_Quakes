# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-03-15

### Changed
- Changed integration domain from `usgs_quakes` to `usgs_earthquakes_feed` to override the built-in HA core integration of the same name
- Kept integration name as "USGS Quakes"
- Renamed `custom_components/usgs_quakes/` folder to `custom_components/usgs_earthquakes_feed/`
- Updated `manifest.json`, `hacs.json`, `mypy.ini`, and GitHub Actions workflow to reflect new domain
- Updated `README.md` references to new domain and sensor/service names
- Updated `STORAGE_KEY` and device identifiers to use `usgs_earthquakes_feed`
- Brand images remain in `custom_components/usgs_earthquakes_feed/brand/` for local brand image support

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
