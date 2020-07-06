# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2020.07.0]

### Added
- check now ensures that all state items have default
- compose now calls "check" to ensure that composed protocol is valid

### Changed
- Use flit for packaging and publishing

### Fixed
- Better handling of union types of message request parameters

## [2020.06.3]

### Added
- Support for ndarray in get_measured

### Fixed
- is-sensor measure message request "loop" now default false, as intended
- check no longer breaks when state or config absent in avpr

## [2020.06.2]

### Fixed
- Spelling of "response" in is-discrete `get_identifier`

## [2020.06.1]

### Added
- request is now explicitly set to empty list and is never ommited

### Changed
- null is now `__null__` for tomls

### Fixed
- general fixes for all traits

## [2020.06.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaqd-ti/-/compare/v2020.07.0...master
[2020.06.0]: https://gitlab.com/yaq/yaqd-ti/-/compare/v2020.06.3...v2020.07.0
[2020.06.3]: https://gitlab.com/yaq/yaqd-ti/-/compare/v2020.06.2...v2020.06.3
[2020.06.2]: https://gitlab.com/yaq/yaqd-ti/-/compare/v2020.06.1...v2020.06.2
[2020.06.1]: https://gitlab.com/yaq/yaqd-ti/-/compare/v2020.06.0...2020.06.1
[2020.06.0]: https://gitlab.com/yaq/yaqd-ti/-/tags/v2020.06.0
