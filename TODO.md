# TODO

- [x] anti-passback (cf. https://github.com/uhppoted/uhppoted/issues/60)
- [x] `argparse` args for examples

- [ ] async functions (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/4)
      - [x] UDP broadcast
      - [x] connected UDP sockets
      - [x] TCP
      - [ ] listen
      - [x] FIXME: if request[1] == 0x96 return None
      - [ ] FIXME: sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      - [ ] integration tests
      - [x] examples
      - (?) pylint
      - (?) ruff
      - (?) maybe replace yapf with black
      - (?) integration tests in github workflow
      - https://lucas-six.github.io/python-cookbook/recipes/core/udp_client_asyncio.html
      - https://docs.python.org/3/library/asyncio-protocol.html#udp-echo-client

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

