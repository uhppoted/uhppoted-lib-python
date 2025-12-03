# TODO


- [ ] async event listener does not report 'OSError: [Errno 48] Address already in use' (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/16)
   - [x] Fix `udp.listen`
   - [x] Fix 'uhppote-async.listen'
   - [x] Fix CLI _listen_
   - [x] Fix example event listener
   - [ ] Integration test
   - [ ] CHANGELOG
   - [ ] README



- [ ] github CI build
```
. .venv/bin/activate; pylint --rcfile=.pylintrc --disable=duplicate-code integration-tests/uhppoted
************* Module expected
integration-tests/uhppoted/expected.py:12:0: C0103: Constant name "GetControllersResponse" doesn't conform to UPPER_CASE naming style (invalid-name)
```

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

2. Unit/integration tests
      - https://hypothesis.readthedocs.io/en/latest/index.html
      - https://docs.python.org/3/library/doctest.html#module-doctest

3. Publish from github
4. Try _ruff_ ?
5. https://fractalideas.com/blog/sans-io-when-rubber-meets-road/
