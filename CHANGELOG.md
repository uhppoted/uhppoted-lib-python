# CHANGELOG

## Unreleased


### Added
1. `get-card-record` and `get-card-record-by-index` convenience API functions.

### Updated
1. Removed legacy `#yapf` directives.


## [0.8.11.2](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.11.2) - 2025-12-08

### Updated
1. Added optional _on_error_ handler to `async` _event-listener_ implementation.


## [0.8.11.1](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.11.1) - 2025-12-04

### Updated
1. Fixed bug in `async` _event-listener_ implementation that swallowed a socket `address in use` error.
2. Added optional `close` event signal to `async` _event-listener_.
3. Fixed changed `TimeoutError` type in _async_ integration tests.


## [0.8.11](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.11) - 2025-07-01

### Added
1. `get/set-antipassback` API function to get/set the anti-passback mode for a controller.
2. Duplicate `async` API with `async` implementations for all API functions.

### Updated
1. Added check to prevent UDP broadcast-to-self.
2. Switched to _black_ formatter.
3. Fixed all pylint warnings.


## [0.8.10](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.10) - 2025-01-29

### Updated
1. Added auto-send interval to get/set-listener API function.
2. Renamed repository from _uhppoted-python_ to _uhppoted-lib-python_.


## [0.8.9](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.91) - 2024-09-06

### Added
1. Enabled per-controller operation timeout configuration.
2. Added support for TCP connections.


## [0.8.8.1](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.8.1) - 2024-04-11

### Added
1. Added support for off-LAN controller configuration in configuration.yaml
2. Enabled per-call operation timeouts.


## [0.8.8](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.8) - 2024-03-26

### Added
1. `restore-default-parameters` function to reset a controller to the manufacturer default configuration.


## [0.8.7.1](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.7.1) - 2024-02-22

### Updated
1. Fixed listen event decoding (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/3)


## [0.8.7](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.7) - 2023-12-01

### Added
1. `set-door-passcodes` function to set supervisor passcodes for a door.

### Updated
1. Reworked `get-status` response decoding to set event fields to `None` if the response
   does not contain an event.
2. Fixed bug decoding IPv4 address in `get-controller` response.
3. Fixed typo decoding MAC address in `get-controller` response.
4. Reworked date/time decoding to unpack invalid date/times as `None`.


## [0.8.6](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.6) - 2023-08-30

### Added
1. Initial release
