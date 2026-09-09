# TODO

- [x] Migrate to codeberg.org (cf. https://codeberg.org/uhppoted/uhppoted/issues/1)
- [x] 'first card' API (cf. https://codeberg.org/uhppoted/uhppoted/issues/2)
- [x] Fix examples to use module syntax, e.g.
- [x] UDP broadcast fails randomly (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/21)
- [x] add first-card privilege to `get-card` and `put-card` (cf. https://codeberg.org/uhppoted/uhppoted/issues/3)
- [x] Implement retry on UDP/TCP connect-to-self (cf. https://codeberg.org/uhppoted/uhppoted/issues/4)
    - [x] broadcast
    - [x] send
    - [x] TCP
    - [x] async::TCP
    - [x] CHANGELOG
    - [x] README

- [ ] event listener examples - get bind/broadcast/listen from command line
- [ ] Put API functions into __init__.py

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
