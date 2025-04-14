![build](https://github.com/uhppoted/uhppoted-lib-python/workflows/build/badge.svg)

# uhppoted-lib-python

Python wrapper around the request/response API for the UHPPOTE TCP/IP access controllers. 

A demo CLI illustrating the use of the API can be found in the [examples/cli](https://github.com/uhppoted/uhppoted-lib-python/tree/main/examples/cli) folder.

## Installation

```
pip install uhppoted
```

## Release Notes

#### Current Release

**[v0.8.10](https://github.com/uhppoted/uhppoted-lib-python/releases/tag/v0.8.10) - 2025-01-29**

1. Added event _auto-send interval_ to the `get-listener` and `set-listener` API function.

## API

Invoking an API function requires an instance of the `Uhppote` class initialised with the information required
to access a controller:

```
class Uhppote:
    def __init__(self, uhppote=None):

where uhppote is an instance of 

class UHPPOTE:
    bind: str
    broadcast: str
    listen: str
    debug: bool

bind        IPv4 address to which to bind the UDP socket. Defaults to 0.0.0.0
broadcast   IPv4 address:port for broadcast UDP packets. Defaults to 255.255.255.255:60000
listen      IPv4 address:port for events from controller (unused). Defaults to 0.0.0.0:60001
debug       Displays the controller requests/responses if true.
```

e.g.:
```
from uhppoted import uhppote
from pprint import pprint

bind = '0.0.0.0'
broadcast = '255.255.255.255:60000'
listen = '0.0.0.0:60001'
debug = True

u = uhppote.Uhppote(bind, broadcast, listen, debug)
record = u.get_controller(405419896)

pprint(record.__dict__, indent=2, width=1)
```
```
>>> from uhppoted import uhppote
>>> from pprint import pprint
>>> 
>>> bind = '0.0.0.0'
>>> broadcast = '255.255.255.255:60000'
>>> listen = '0.0.0.0:60001'
>>> debug = True
>>> 
>>> u = uhppote.Uhppote(bind, broadcast, listen, debug)
>>> record = u.get_controller(405419896)
   00000000  17 94 00 00 78 37 2a 18  00 00 00 00 00 00 00 00
   00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
   00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
   00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00

   00000000  17 94 00 00 78 37 2a 18  c0 a8 01 64 ff ff ff 00
   00000010  c0 a8 01 01 00 12 23 34  45 56 08 92 20 18 11 05
   00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
   00000030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00

>>> 
>>> pprint(record.__dict__, indent=2, width=1)
{ 'controller': 405419896,
  'date': datetime.date(2018, 11, 5),
  'gateway': IPv4Address('192.168.1.1'),
  'ip_address': IPv4Address('192.168.1.100'),
  'mac_address': '00:12:23:34::45:56',
  'subnet_mask': IPv4Address('255.255.255.0'),
  'version': 'v8.92'}
```

### Notes
1. All API functions raise an `Exception` if the call fails for any reason whatsoever.
2. All API functions (other than `get_controllers` and `listen`) take a `controller` that may be either:
   - a _uint32_s controller serial number (legacy)
   - a tuple comprising `(id,address,protocol)`, where
       - `id` is the (required) controller serial number
       - `address` is the (optional) controller IPv4 address or address:port
       - `protocol` is the (optional) transport protocol ('udp' or 'tcp')
   e.g.:
```
   get_controller(405419896)
   get_controller((405419896, '192.168.1.100', 'tcp'))
   get_controller((405419896, '192.168.1.100:60000', 'tcp'))
   get_controller((405419896, '192.168.1.100'))
   get_controller((405419896, '192.168.1.100:60000'))
   get_controller((405419896)

   Defaults to UDP and udp broadcast if the controller cannot be disambiguated.
```

3. All API functions (other than `listen`) take an optional `timeout` kwarg that sets the time limit (in seconds)
   for the request, e.g.:
```
   get_controller(controller, dest_addr='192.168.1.100:60000', protocol='udp', timeout=0.75)

   Defaults to 2.5s.
```

**API**

- [`get_controllers`](#get_controllers)
- [`get_controller`](#get_controller)
- [`set_address`](#set_address)
- [`get_status`](#get_status)
- [`get_time`](#get_time)
- [`set_time`](#set_time)
- [`get_listener`](#get_listener)
- [`set_listener`](#set_listener)
- [`get_door_control`](#get_door_control)
- [`set_door_control`](#set_door_control)
- [`open_door`](#open_door)
- [`get_cards`](#get_cards)
- [`get_card`](#get_card)
- [`get_card_by_index`](#get_card_by_index)
- [`put_card`](#put_card)
- [`delete_card`](#delete_card)
- [`delete_cards`](#delete_cards)
- [`get_event_index`](#get_event_index)
- [`set_event_index`](#set_event_index)
- [`get_event`](#get_event)
- [`record_special_events`](#record_special_events)
- [`get_time_profile`](#get_time_profile)
- [`set_time_profile`](#set_time_profile)
- [`clear_time_profiles`](#clear_time_profiles)
- [`add_task`](#add_task)
- [`refresh_tasklist`](#refresh_tasklist)
- [`clear_tasklist`](#clear_tasklist)
- [`set_pc_control`](#set_pc_control)
- [`set_interlock`](#set_interlock)
- [`activate_keypads`](#activate_keypads)
- [`set_door_passcodes`](#set_door_passcodes)
- [`get_antipassback`](#get_antipassback)
- [`set_antipassback`](#set_antipassback)
- [`restore_default_parameters`](#restore_default_parameters)
- [`listen`](#listen)

### `get_controllers`
```
get_controllers()

Returns an array of `GetControllerResponse`.

Raises an Exception if the call failed for any reason.
```

### `get_controller`
```
get_controller(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Returns a `GetControllerResponse` with the controller device information.

Raises an Exception if the call failed for any reason.
```

### `set_address`
```
set_address(self, ID, address, subnet, gateway)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
address     string        controller IPv4 address
subnet      string        controller IPv4 subnet mask
gateway     string        controller gateway IPv4 address

Raises an Exception if the call failed for any reason.
```

### `get_status`
```
get_status(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Returns a `GetStatusResponse` with the controller status information. If the response does not contain a
valid event, the event fields are set to `None`.

Raises an Exception if the call failed for any reason.
```

### `get_time`
```
get_time(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Returns a `GetTimeResponse` with the current controller date and time..

Raises an Exception if the call failed for any reason.
```

### `set_time`
```
set_time(controller, datetime)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
datetime    datetime      date/time

Returns a `SetTimeResponse` with the current controller date and time.

Raises an Exception if the call failed for any reason.
```

### `get_listener`
```
get_listener(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Returns a `GetListener` with the configured controller event listener IPv4 address and UDP port, as well
as the controller auto-send interval. The auto-send interval is the interval (in seconds) at which the 
controller sends the current status and most recent event (events are still sent as and when they occur).
Auto-send is disabled if the _interval_ is 0.

Raises an Exception if the call failed for any reason.
```

### `set_listener`
```
set_listener(controller, listener, interval)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
listener    string        listener IPv4 address:port string
interval    uint8         Auto-send interval (seconds). Defaults to 0 (disabled)

Raises an Exception if the call failed for any reason.
```

### `get_door_control`
```
get_door_control(controller, door)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
door        uint8         door ID [1..4]

Returns a DoorControl dataclass instance populated with the controller door configuration if the call succeeded.

Raises an Exception if the call failed for any reason.
```

### `set_door_control`
```
set_door_control(controller, door, mode, delay)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
door        uint8         door ID [1..4]
mode        uint8         normally open (1), normally closed (2) or controlled (3)
delay       uintt8        door open delay in seconds

Raises an Exception if the call failed for any reason.
```

### `open_door`
```
open_door(controller, door)

ID    uint32  controller serial number 
door  uint8   door ID [1..4]

Raises an Exception if the call failed for any reason.
```

### `get_cards`
```
get_cards(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Returns the number of cards stored on the controller if the call succeeded.

Raises an Exception if the call failed for any reason.
```

### `get_card`
```
get_card(controller, card)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
card        uint32        card number

Returns a Card dataclass instance with the controller card information if the call succeeded.

Raises an Exception if the call failed for any reason.
```

### `get_card_by_index`
```
get_card_by_index(controller, index)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
index       uint32        index of card to retrieve

Returns a Card dataclass instance with the controller card information if the call succeeded.

Raises an Exception if the call failed for any reason.
```

### `put_card`
```
put_card(controller, card, start, end, door1, door2, door3, door4)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
card        uint32        card number
from        datetime      card valid from date, inclusive (YYYY-MM-dd)
to          datetime      card valid until, inclusive (YYYY-MM-dd)
door1       uint8         Door 1 access (0: none, 1: all, 2-254: time profile)
door2       uint8         Door 2 access (0: none, 1: all, 2-254: time profile)
door3       uint8         Door 3 access (0: none, 1: all, 2-254: time profile)
door4       uint8         Door 4 access (0: none, 1: all, 2-254: time profile)

Raises an Exception if the call failed for any reason.
```

### `delete_card`
```
delete_card(controller, card)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
card        uint32        card number

Raises an Exception if the call failed for any reason.
```

### `delete_cards`
```
delete_cards(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Raises an Exception if the call failed for any reason.
```

### `get_event_index`
```
get_event_index(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Returns the controller event index if the call succeeded.

Raises an Exception if the call failed for any reason.
```

### `set_event_index`
```
set_event_index(controller, index)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
index       uint32        controller event index

Raises an Exception if the call failed for any reason.
```

### `get_event`
```
get_event(controller, index)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
index       uint32        index of event to retrieve

Returns an event dataclass instance with the controller event stored at the index.

Raises an Exception if the call failed for any reason.
```

### `record_special_events`
```
record_special_events(controller, enabled)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
enabled     bool          Enables/disables recording of door, etc events

Raises an Exception if the call failed for any reason.
```

### `get_time_profile`
```
get_time_profile(controller, profileID)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
profile_ID  uint8         ID [2..254] of time profile to retrieve

Returns a TimeProfile dataclass instance with the time profile stored at the profile ID on the controller.

Raises an Exception if the call failed for any reason.
```

### `set_time_profile`
```
set_time_profile(controller, profile)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
profile     uint8         TimeProfile dataclass instance initialised with the time profile to store on the controller.

Raises an Exception if the call failed for any reason.
```

### `clear_time_profiles`
```
clear_time_profiles(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Raises an Exception if the call failed for any reason.
```

### `add_task`
```
add_task(controller, task)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
task        uint8         Task dataclass instance initialised with the task to store on the controller.

Raises an Exception if the call failed for any reason.
```

### `refresh_tasklist`
```
refresh_tasklist(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Raises an Exception if the call failed for any reason.
```

### `clear_tasklist`
```
clear_tasklist(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple

Raises an Exception if the call failed for any reason.
```

### `set_pc_control`
```
set_pc_control(controller, enabled)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
enabled     bool          enables/disables host control

Raises an Exception if the call failed for any reason.
```

### `set_interlock`
```
set_interlock(controller, interlock)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
interlock   uint8         controller door interlock mode
                          - 0: no interlock
                          - 1: doors 1&2
                          - 2: doors 3&4
                          - 3: doors 1&2,3&4
                          - 4: doors 1&2&3
                          - 8: doors 1&2&3&4


Raises an Exception if the call failed for any reason.
```

### `activate_keypads`
```
activate_keypads(controller, reader1, reader2, reader3, reader4)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
reader1     bool          activates/deactivates reader 1 access keypad
reader2     bool          activates/deactivates reader 2 access keypad
reader3     bool          activates/deactivates reader 3 access keypad
reader4     bool          activates/deactivates reader 4 access keypad


Raises an Exception if the call failed for any reason.
```

### `set_door_passcodes`
```
set_door_passcodes(controller, door, passcode1, passcode2, passcode3, passcode4)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple
door        uint8         door ID [1..4]
passcode1   uint32        supervisor passcode 1 [0..999999] (0 is 'no code')
passcode2   uint32        supervisor passcode 2 [0..999999] (0 is 'no code')
passcode3   uint32        supervisor passcode 3 [0..999999] (0 is 'no code')
passcode4   uint32        supervisor passcode 4 [0..999999] (0 is 'no code')


Raises an Exception if the call failed for any reason.
```

### `get_antipassback`

Retrieves the anti-passback mode from the controller.

```
get_antipassback(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple


Raises an Exception if the call failed for any reason.
```

### `set_antipassback`

Sets the controller anti-passback mode.

```
set_antipassback(controller, antipassback)

controller    uint32|tuple  controller serial number or (id, address, protocol) tuple
antipassback  uint8         anti-passback mode:
                            - 0: disabled
                            - 1: (1:2);(3:4)
                            - 2: (1,3);(2,4)
                            - 3: 1:(2,3)
                            - 4: 1:(2,3,4)


Raises an Exception if the call failed for any reason.
```

### `restore_default_parameters`
```
restore_default_parameters(controller)

controller  uint32|tuple  controller serial number or (id, address, protocol) tuple


Raises an Exception if the call failed for any reason.
```

### `listen`
```
listen(handler)

handler  event handling callback function of the form
         def on_event(event):
              ...

Raises an Exception if the call failed for any reason.
```

`listen` is a blocking call that will invoke the `handler` function for each received event, e.g.:
```
    ...
    u.listen(on_event)

def on_event(event):
    if event != None:
        pprint(event.__dict__, indent=2, width=1)
    ...
```

## Types

### `GetControllerResponse`

Container class for the decoded response from a get-controller request.

    Fields:
        controller   (uint32)       Serial number.
        ip_address   (IPv4Address)  IP address.
        subnet_mask  (IPv4Address)  Subnet mask.
        gateway      (IPv4Address)  Gateway IP address.
        mac_address  (string)       MAC address (XX:XX:XX:XX:XX:XX).
        version      (string)       Firmware version (vN.NN).
        date         (date)         Release date (YYYY-MM-DD).
```
@dataclass
class GetControllerResponse:
    controller: int
    ip_address: IPv4Address
    subnet_mask: IPv4Address
    gateway: IPv4Address
    mac_address: str
    version: str
    date: datetime.date
```


### `GetTimeResponse`

Container class for the decoded response from a get-time request.

    Fields:
        controller   (uint32)    Controller serial number.
        datetime     (datetime)  Controller system date/time.
```
@dataclass
class GetTimeResponse:
    controller: int
    datetime: datetime.datetime
```


### `SetTimeResponse`

Container class for the decoded response from a set-time request.

    Fields:
       controller   (uint32)    Controller serial number.
       datetime     (datetime)  Controller system date/time.

```
@dataclass
class SetTimeResponse:
    controller: int
    datetime: datetime.datetime
```


### `GetStatusResponse`

Container class for the decoded response from a get-status request.

    Fields:
        controller           (uint32)    Controller serial number.
        system_date          (date)      Controller system date.
        system_time          (time)      Controller system time.
        door_1_open          (bool)      Door 1 locked/unlocked.
        door_2_open          (bool)      Door 2 locked/unlocked.
        door_3_open          (bool)      Door 3 locked/unlocked.
        door_4_open          (bool)      Door 4 locked/unlocked.
        door_1_button        (bool)      Pushbutton 1 pressed/released.
        door_2_button        (bool)      Pushbutton 2 pressed/released.
        door_3_button        (bool)      Pushbutton 3 pressed/released.
        door_4_button        (bool)      Pushbutton 4 pressed/released.
        relays               (uint8)     Bit array of relay states.
        inputs               (uint8)     Bit array of door sensor states.
        system_error         (uint8)     System error code.
        special_info         (uint8)     Absolutely no idea.
        event_index          (uint32)    Index of last recorded event.
        event_type           (uint32)    Type of last recorded event.
        event_access_granted (bool)      Last event access granted/denied.
        event_door           (uin8)      Last event door no. [1..4].
        event_direction      (uint8)     Last event direction (0: in, 1: out).
        event_card           (uint32)    Last event card number.
        event_timestamp      (datetime)  Last event timestamp.
        event_reason         (uint8)     Last event access granted/denied reason code.
        sequence_no          (uint32)    Packet sequence number.
```
@dataclass
class GetStatusResponse:
    controller: int
    system_date: datetime.date
    system_time: datetime.time
    door_1_open: bool
    door_2_open: bool
    door_3_open: bool
    door_4_open: bool
    door_1_button: bool
    door_2_button: bool
    door_3_button: bool
    door_4_button: bool
    relays: int
    inputs: int
    system_error: int
    special_info: int
    event_index: int
    event_type: int
    event_access_granted: bool
    event_door: int
    event_direction: int
    event_card: int
    event_timestamp: datetime.datetime
    event_reason: int
    sequence_no: int
```


### `GetListenerResponse`

Container class for the decoded response from a get-listener request.

    Fields:
        controller  (uint32)       Controller serial number.
        address     (IPv4Address)  Configured event listener IP address.
        port        (uint16)       Configured event listener UDP port.
```
@dataclass
    controller: int
    address: IPv4Address
    port: int
```


### `SetListenerResponse`

Container class for the decoded response from a set-listener request.

    Fields:
        controller  (uint32)  Controller serial number.
        ok          (bool)    Succeeded/failed.
```
@dataclass
class SetListenerResponse:
    controller: int
    ok: bool
```


### `GetDoorControlResponse`

Container class for the decoded response from a get-door-control request.

    Fields:
        controller  (uint32)  Controller serial number.
        door        (uint8)   Door no.[1..4]
        mode        (uint8)   Door control mode (1: normally open, 2: normally closed, 3: controlled)
        delay       (uint8)   Door unlock duration (seconds)
```
@dataclass
class GetDoorControlResponse:
    controller: int
    door: int
    mode: int
    delay: int
```


### `SetDoorControlResponse`

Container class for the decoded response from a set-door-control request.

    Fields:
        controller  (uint32)  Controller serial number.
        door        (uint8)   Door no.[1..4]
        mode        (uint8)   Door control mode (1: normally open, 2: normally closed, 3: controlled)
        delay       (uint8)   Door unlock duration (seconds)
```
@dataclass
class SetDoorControlResponse:
    controller: int
    door: int
    mode: int
    delay: int
```


### `OpenDoorResponse`

Container class for the decoded response from an open-door request.

    Fields:
        controller  (uint32)  Controller serial number.
        opened      (bool)    Succeeded/failed.
```
@dataclass
class OpenDoorResponse:
    controller: int
    opened: bool
```


### `GetCardsResponse`

Container class for the decoded response from an open-door request.

    Fields:
        controller  (uint32)  Controller serial number.
        cards       (uint32)  Number of cards stored on controller.
```
@dataclass
class GetCardsResponse:
    controller: int
    cards: int
```


### `GetCardResponse`

Container class for the decoded response from a get-card request.

    Fields:
        controller  (uint32)  Controller serial number.
        card_number (uint32)  Card number.
        start_date  (date)    Card 'valid from' date.
        end_date    (date)    Card 'valid until' date.
        end_date    (date)    Card 'valid until' date.
        door_1      (uint8)   Card access permissions for door 1 (0: none, 1: all, 2-254: time profile ID)
        door_2      (uint8)   Card access permissions for door 2 (0: none, 1: all, 2-254: time profile ID)
        door_3      (uint8)   Card access permissions for door 3 (0: none, 1: all, 2-254: time profile ID)
        door_4      (uint8)   Card access permissions for door 4 (0: none, 1: all, 2-254: time profile ID)
        pin         (uint24)  Card access keypad PIN code (0 for none)
```
@dataclass
class GetCardResponse:
    controller: int
    card_number: int
    start_date: datetime.date
    end_date: datetime.date
    door_1: int
    door_2: int
    door_3: int
    door_4: int
    pin: PIN
```


### `GetCardByIndexResponse`

Container class for the decoded response from a get-card-by-index request.

    Fields:
        controller  (uint32)  Controller serial number.
        card_number (uint32)  Card number.
        start_date  (date)    Card 'valid from' date.
        end_date    (date)    Card 'valid until' date.
        door_1      (uint8)   Card access permissions for door 1 (0: none, 1: all, 2-254: time profile ID)
        door_2      (uint8)   Card access permissions for door 2 (0: none, 1: all, 2-254: time profile ID)
        door_3      (uint8)   Card access permissions for door 3 (0: none, 1: all, 2-254: time profile ID)
        door_4      (uint8)   Card access permissions for door 4 (0: none, 1: all, 2-254: time profile ID)
        pin         (uint24)  Card access keypad PIN code (0 for none)
```
@dataclass
class GetCardByIndexResponse:
    controller: int
    card_number: int
    start_date: datetime.date
    end_date: datetime.date
    door_1: int
    door_2: int
    door_3: int
    door_4: int
    pin: PIN
```


### `PutCardResponse`

Container class for the decoded response from an open-door request.

    Fields:
        controller  (uint32)  Controller serial number.
        stored      (bool)    Succeeded/failed.
```
@dataclass
class PutCardResponse:
    controller: int
    stored: bool
```


### `DeleteCardResponse`

Container class for the decoded response from a delete-card request.

    Fields:
        controller  (uint32)  Controller serial number.
        deleted     (bool)    Succeeded/failed.
```
@dataclass
class DeleteCardResponse:
    controller: int
    deleted: bool
```

### `DeleteAllCardsResponse`

Container class for the decoded response from a delete-all-cards request.

    Fields:
        controller  (uint32)  Controller serial number.
        deleted     (bool)    Succeeded/failed.
```
@dataclass
class DeleteAllCardsResponse:
    controller: int
    deleted: bool
```

### `GetEventResponse`

Container class for the decoded response from a get-event request.

    Fields:
        controller      (uint32)    Controller serial number.
        index           (uint32)    Index of last recorded event.
        event_type      (uint32)    Type of last recorded event.
        access_granted  (bool)      Last event access granted/denied.
        door            (uin8)      Last event door no. [1..4].
        direction       (uint8)     Last event direction (0: in, 1: out).
        card            (uint32)    Last event card number.
        timestamp       (datetime)  Last event timestamp.
        reason          (uint8)     Last event access granted/denied reason code.
```
@dataclass
class GetEventResponse:
    controller: int
    index: int
    event_type: int
    access_granted: bool
    door: int
    direction: int
    card: int
    timestamp: datetime.datetime
    reason: int
```

### `GetEventIndexResponse`

Container class for the decoded response from a get-event-index request.

    Fields:
        controller      (uint32)    Controller serial number.
        index           (uint32)    Downloaded event index.
```
@dataclass
class GetEventIndexResponse:
    controller: int
    event_index: int
```

### `SetEventIndexResponse`

Container class for the decoded response from a set-event-index request.

    Fields:
        controller  (uint32)  Controller serial number.
        updated     (bool)    Succeeded/failed.
```
@dataclass
class SetEventIndexResponse:
    controller: int
    updated: bool
```

### `RecordSpecialEventsResponse`

Container class for the decoded response from a record-special-events request.

    Fields:
        controller  (uint32)  Controller serial number.
        updated     (bool)    Succeeded/failed.
```
@dataclass
class RecordSpecialEventsResponse:
    controller: int
    updated: bool
```

### `GetTimeProfileResponse`

Container class for the decoded response from a get-time-profile request.

    Fields:
        controller        (uint32)  Controller serial number.
        profile_id        (uint8)   Time profile ID [2..254].
        start_date        (date)    Time profile 'valid from' date.
        end_date          (date)    Time profile 'valid until' date.
        monday            (bool)    Time profile enabled on Monday.
        tuesday           (bool)    Time profile enabled on Tuesday.
        wednesday         (bool)    Time profile enabled on Wednesday.
        thursday          (bool)    Time profile enabled on Thursday.
        friday            (bool)    Time profile enabled on Friday.
        saturday          (bool)    Time profile enabled on Saturday.
        sunday            (bool)    Time profile enabled on Sunday.
        segment_1_start   (time)    Time profile segment 1 start time (HHmm).
        segment_1_end     (time)    Time profile segment 1 end time (HHmm).
        segment_2_start   (time)    Time profile segment 2 start time (HHmm).
        segment_2_end     (time)    Time profile segment 2 end time (HHmm).
        segment_3_start   (time)    Time profile segment 3 start time (HHmm).
        segment_3_end     (time)    Time profile segment 3 end time (HHmm).
        linked_profile_id (uint8)   Next profile ID in chain (0 if none).
```
@dataclass
class GetTimeProfileResponse:
    controller: int
    profile_id: int
    start_date: datetime.date
    end_date: datetime.date
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    segment_1_start: datetime.time
    segment_1_end: datetime.time
    segment_2_start: datetime.time
    segment_2_end: datetime.time
    segment_3_start: datetime.time
    segment_3_end: datetime.time
    linked_profile_id: int
```

### `SetTimeProfileResponse`

Container class for the decoded response from a set-time-profile request.

    Fields:
        controller  (uint32)  Controller serial number.
        stored      (bool)    Succeeded/failed.
```
@dataclass
class SetTimeProfileResponse:
    controller: int
    stored: bool
```

### `DeleteAllTimeProfilesResponse`

Container class for the decoded response from a delete-all-time-profiles request.

    Fields:
        controller  (uint32)  Controller serial number.
        deleted     (bool)    Succeeded/failed.
```
@dataclass
class DeleteAllTimeProfilesResponse:
    controller: int
    deleted: bool
```

### `AddTaskResponse`

Container class for the decoded response from an add-task request.

    Fields:
        controller  (uint32)  Controller serial number.
        added       (bool)    Succeeded/failed.
```
@dataclass
class AddTaskResponse:
    controller: int
    added: bool
```

### `RefreshTasklistResponse`

Container class for the decoded response from a refersh-tasklist request.

    Fields:
        controller  (uint32)  Controller serial number.
        refreshed   (bool)    Succeeded/failed.
```
@dataclass
class RefreshTasklistResponse:
    controller: int
    refreshed: bool
```

### `ClearTasklistResponse`

Container class for the decoded response from a clear-tasklist request.

    Fields:
        controller  (uint32)  Controller serial number.
        cleared     (bool)    Succeeded/failed.
```
@dataclass
class ClearTasklistResponse:
    controller: int
    cleared: bool
```

### `SetPcControlResponse`

Container class for the decoded response from a set-pc-control request.

    Fields:
        controller  (uint32)  Controller serial number.
        ok          (bool)    Succeeded/failed.
```
@dataclass
class SetPcControlResponse:
    controller: int
    ok: bool
```

### `SetInterlockResponse`

Container class for the decoded response from a set-interlock request.

    Fields:
        controller  (uint32)  Controller serial number.
        ok          (bool)    Succeeded/failed.
```
@dataclass
class SetInterlockResponse:
    controller: int
    ok: bool
```

### `ActivateKeypadsResponse`

Container class for the decoded response to an activate-keypads request.

    Fields:
        controller  (uint32)  Controller serial number.
        ok          (bool)    Succeeded/failed.
```
@dataclass
class ActivateKeypadsResponse:
    controller: int
    ok: bool
```

### `SetDoorPasscodesResponse`

Container class for the decoded response to a set-door-passcodes request.

    Fields:
        controller  (uint32)  Controller serial number.
        ok          (bool)    Succeeded/failed.
```
@dataclass
class SetDoorPasscodesResponse:
    controller: int
    ok: bool
```

### `GetAntiPassbackResponse`

Container class for the decoded response to a get-antipassback request.

    Fields:
        controller   (uint32)  Controller serial number.
        antipassback (uint8)   Anti-passback mode:
                               - 0: disabled
                               - 1: (1:2);(3:4)
                               - 2: (1,3):(2,4)
                               - 3: 1:(2,3)
                               - 4: 1:(2,3,4)
```
@dataclass
class GetAntiPassbackResponse:
    controller: int
    antipassback: int
```

### `SetAntiPassbackResponse`

Container class for the decoded response to a set-antipassback request.

    Fields:
        controller  (uint32)  Controller serial number.
        ok          (bool)    Succeeded/failed.
```
@dataclass
class SetAntiPassbackResponse:
    controller: int
    ok: bool
```

### `RestoreDefaultParametersResponse`

Container class for the decoded response to a restore-default-parameters request.

    Fields:
        controller  (uint32)  Controller serial number.
        reset       (bool)    Succeeded/failed.
```
@dataclass
class RestoreDefaultParametersResponse:
    controller: int
    reset: bool
```

### `Event`

Container class for a decoded event packet.

       Fields:
        controller           (uint32)    Controller serial number.
        event_index          (uint32)    Index of last recorded event.
        event_type           (uint32)    Type of last recorded event.
        event_access_granted (bool)      Last event access granted/denied.
        event_door           (uin8)      Last event door no. [1..4].
        event_direction      (uint8)     Last event direction (0: in, 1: out).
        event_card           (uint32)    Last event card number.
        event_timestamp      (datetime)  Last event timestamp.
        event_reason         (uint8)     Last event access granted/denied reason code.
        system_date          (date)      Controller system date.
        system_time          (time)      Controller system time.
        door_1_open          (bool)      Door 1 locked/unlocked.
        door_2_open          (bool)      Door 2 locked/unlocked.
        door_3_open          (bool)      Door 3 locked/unlocked.
        door_4_open          (bool)      Door 4 locked/unlocked.
        door_1_button        (bool)      Pushbutton 1 pressed/released.
        door_2_button        (bool)      Pushbutton 2 pressed/released.
        door_3_button        (bool)      Pushbutton 3 pressed/released.
        door_4_button        (bool)      Pushbutton 4 pressed/released.
        relays               (uint8)     Bit array of relay states.
        inputs               (uint8)     Bit array of door sensor states.
        system_error         (uint8)     System error code.
        special_info         (uint8)     Absolutely no idea.
        sequence_no          (uint32)    Packet sequence number.
```
@dataclass
class Event:
    controller: int
    event_index: int
    event_type: int
    event_access_granted: bool
    event_door: int
    event_direction: int
    event_card: int
    event_timestamp: datetime.datetime
    event_reason: int
    system_date: datetime.date
    system_time: datetime.time
    door_1_open: bool
    door_2_open: bool
    door_3_open: bool
    door_4_open: bool
    door_1_button: bool
    door_2_button: bool
    door_3_button: bool
    door_4_button: bool
    relays: int
    inputs: int
    system_error: int
    special_info: int
    sequence_no: int
```
