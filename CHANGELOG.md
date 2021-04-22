# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2021.4.0]

### Changed
- Update for fastavro 1.4, pin version

## [2021.3.2]

### Changed
- `has-turret` trait now uses string identifiers instead of int, adds a `get_turret_options` method

## [2021.3.1]

### Added
- additional message "get_measurement_id" to is-sensor

### Changed
- Add `options_getter` to is-discrete `position_identifier` field, replacing the parallel related field

## [2021.3.0]

### Changed
- yaq-traits compose now accepts directories
- new flag to compose: --save

## [2021.2.1]

### Changed
- yaq-traits check now accepts directories, which are recursively searched for avpr files

### Fixed
- added forgotten config options to is-daemon: enable, log_level, and log_to_file

## [2021.2.0]

### Added
- has-mapping trait definition, see [YEP-311](https://yeps.yaq.fyi/311/)
- fields for has-position
- fields for is-discrete
- fields for has-limits

## [2020.11.0]

### Changed
- yaq-traits check now accepts multiple files passed as args

### Added
- yaq-traits check now has `--fix` to automatically recompose if the toml is colocated

## [2020.10.1]

### Added
- Origin key in avprs identifies trait which defined the config, state, or message
- `get` subcommand which prints fully specified avpr JSON given a trait name
- `list` subcommand which prints a list of available traits

### Changed
- Fail if unexpected trait found as well as expected trait not found
- Remove extraneous "trait" key from daemon avpr"
- Use double precision instead of single precision floats
- Default `loop_at_startup` to false in `has-measure-trigger`

## [2020.10.0]

### Added
- pre-commit support

### Changed
- Default turret index is now null (was nan, which is not the right type)

## [2020.07.3]

### Changed
- Update to fastavro 0.24.0 named schemas

## [2020.07.2]

### Added
- Handle schema defined types and define ndarray
- added new trait `has-measure-trigger`, see [YEP-310](https://yeps.yaq.fyi/310/)

### Changed
- removed `measure` and `stop_looping` messages from `is-sensor` (migrated to `has-measure-trigger`)

## [2020.07.1]

### Changed
- distribute with `-` instead of `_`

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

[Unreleased]: https://gitlab.com/yaq/yaq-traits/-/compare/v2021.4.0...master
[2021.4.0]: https://gitlab.com/yaq/yaq-traits/-/compare/v2021.3.2...v2021.4.0
[2021.3.2]: https://gitlab.com/yaq/yaq-traits/-/compare/v2021.3.1...v2021.3.2
[2021.3.1]: https://gitlab.com/yaq/yaq-traits/-/compare/v2021.3.0...v2021.3.1
[2021.3.0]: https://gitlab.com/yaq/yaq-traits/-/compare/v2021.2.1...v2021.3.0
[2021.2.1]: https://gitlab.com/yaq/yaq-traits/-/compare/v2021.2.0...v2021.2.1
[2021.2.0]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.11.0...v2021.2.0
[2020.11.0]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.10.1...v2020.11.0
[2020.10.1]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.10.0...v2020.10.1
[2020.10.0]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.07.3...v2020.10.0
[2020.07.3]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.07.2...v2020.07.3
[2020.07.2]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.07.1...v2020.07.2
[2020.07.1]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.06.3...v2020.07.0
[2020.06.3]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.06.2...v2020.06.3
[2020.06.2]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.06.1...v2020.06.2
[2020.06.1]: https://gitlab.com/yaq/yaq-traits/-/compare/v2020.06.0...2020.06.1
[2020.06.0]: https://gitlab.com/yaq/yaq-traits/-/tags/v2020.06.0
