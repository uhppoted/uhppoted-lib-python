# TODO

- [x] anti-passback (cf. https://github.com/uhppoted/uhppoted/issues/60)
- [x] `argparse` args for examples
- [x] async functions (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/4)
      - [x] UDP broadcast
      - [x] connected UDP sockets
      - [x] TCP
      - [x] listen
      - [x] FIXME: if request[1] == 0x96 return None
      - [x] integration tests
      - [x] examples
      - [x] event-listener example
      - [x] CHANGELOG
      - [x] README

- [x] Replace yapf with black
- [ ] pylint
      - [x] fix decode::MAC
      - [ ] move is_inaddr_any to net
      - [ ] Remove 'all' command from CLI

- [ ] Fix 'all' command
- (?) ruff
- (?) integration tests in github workflow
- (?) https://fractalideas.com/blog/sans-io-when-rubber-meets-road/

- [ ] Use site-specific configuration to run examples locally
      - https://docs.python.org/3/library/site.html

## TODO
1. (?) Automatically set-listener address
   - https://stackoverflow.com/questions/5281409/get-destination-address-of-a-received-udp-packet
   - https://stackoverflow.com/questions/39059418/python-sockets-how-can-i-get-the-ip-address-of-a-socket-after-i-bind-it-to-an

2. Unit/integration tests
      - https://hypothesis.readthedocs.io/en/latest/index.html
      - https://docs.python.org/3/library/doctest.html#module-doctest

3. Publish from github
