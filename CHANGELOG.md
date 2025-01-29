# CHANGELOG

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
