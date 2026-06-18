# TODO

- [x] 'first card' API (cf. https://github.com/uhppoted/uhppoted/issues/82)

- [ ] UDP broadcast fails randomly (cf. https://github.com/uhppoted/uhppoted-lib-python/issues/21)
      - [x] retry if bind port is 0
      - (?) add check to udp::send
      - [ ] README
      - [x] CHANGELOG
      - [ ] Add to FAQ:
          - ```sudo sysctl -w net.ipv4.ip_local_port_range="40000 59999"```
          - ```sudo sysctl -w net.ipv4.ip_local_reserved_ports=60000```
          - https://stackoverflow.com/questions/7006939/how-to-change-view-the-ephemeral-port-range-on-windows-machines
          - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/default-dynamic-port-range-tcpip-chang
          - ```netsh int ipv4 add excludedportrange protocol=tcp startport=8000 numberofports=1```
          - https://powershell.xevion.dev/scripts/excluded-ports
          - https://support.microsoft.com/en-us/topic/you-cannot-exclude-ports-by-using-the-reservedports-registry-key-in-windows-server-2008-or-in-windows-server-2008-r2-a68373fd-9f64-4bde-9d68-c5eded74ea35

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
