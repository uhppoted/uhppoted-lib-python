# TODO

- [x] anti-passback (cf. https://github.com/uhppoted/uhppoted/issues/60)
- [x] `argparse` args for examples
- [x] async functions (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/4)
- [x] Replace yapf with black
- [x] pylint
- [x] `print(..., flush=True)`
- [ ] UDP dropping packets (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/10)

- [ ] integration tests in github workflow
- [ ] Replace `print(exc)` with proper logging
- [ ] Use site-specific configuration to run examples locally
      - https://docs.python.org/3/library/site.html
      - (?) custom pyproject.toml (a la home-assistant)

## TODO
1. (?) Automatically set-listener address
   - https://stackoverflow.com/questions/5281409/get-destination-address-of-a-received-udp-packet
   - https://stackoverflow.com/questions/39059418/python-sockets-how-can-i-get-the-ip-address-of-a-socket-after-i-bind-it-to-an

2. Unit/integration tests
      - https://hypothesis.readthedocs.io/en/latest/index.html
      - https://docs.python.org/3/library/doctest.html#module-doctest

3. Publish from github
4. Try _ruff_ ?
5. https://fractalideas.com/blog/sans-io-when-rubber-meets-road/
