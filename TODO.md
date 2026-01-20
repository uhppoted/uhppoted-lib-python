# TODO

- [x] Implement get_xxx_record API (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/9)s
- [x] Fix `# pylint: disable` (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/19)
- [x] Use 'uv dev' to avoid packaging integration tests (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/17)

- [ ] `set-ip`
   - [ ] Fix integration test
   - [ ] encode unit test
   
- [ ] integration tests in github workflow
- [ ] Replace `print(exc)` with proper logging
- [ ] Use site-specific configuration to run examples locally
      - https://docs.python.org/3/library/site.html
      - (?) custom pyproject.toml (a la home-assistant)

## TODO
1. (?) Automatically set-listener address
   - https://stackoverflow.com/questions/5281409/get-destination-address-of-a-received-udp-packet
   - https://stackoverflow.com/questions/39059418/python-sockets-how-can-i-get-the-ip-address-of-a-socket-after-i-bind-it-to-an

2. Publish from github
3. Try _ruff_ ?
4. https://fractalideas.com/blog/sans-io-when-rubber-meets-road/
