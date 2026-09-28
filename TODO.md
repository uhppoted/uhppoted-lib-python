# TODO


- [ ] bind before connect to assign socket port
```
import asyncio

async def main():
    # This binds locally to port 50000 during creation, avoiding a spurious connect
    reader, writer = await asyncio.open_connection('example.com', 80, local_addr=('127.0.0.1', 50000))

    # You can verify it immediately
    print(writer.get_extra_info('sockname'))

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
```

## To Be Done
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

## Other
1. (?) Automatically set-listener address
   - https://stackoverflow.com/questions/5281409/get-destination-address-of-a-received-udp-packet
   - https://stackoverflow.com/questions/39059418/python-sockets-how-can-i-get-the-ip-address-of-a-socket-after-i-bind-it-to-an

2. Publish from github
3. Try _ruff_ ?
4. https://fractalideas.com/blog/sans-io-when-rubber-meets-road/
