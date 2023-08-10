'''
Shared dataclass definitions.
'''

import datetime
import struct

from ipaddress import IPv4Address
from dataclasses import dataclass
from typing import NewType

PIN = NewType('PIN', int)


@dataclass
class GetControllerResponse:
    '''
    Container class for the decoded response from a get-controller request.

       Fields:
          controller   (uint32)       Serial number.
          ip_address   (IPv4Address)  IP address.
          subnet_mask  (IPv4Address)  Subnet mask.
          gateway      (IPv4Address)  Gateway IP address.
          mac_address  (string)       MAC address (XX:XX:XX:XX:XX:XX).
          version      (string)       Firmware version (vN.NN).
          date         (date)         Release date (YYYY-MM-DD).
    '''
    controller: int
    ip_address: IPv4Address
    subnet_mask: IPv4Address
    gateway: IPv4Address
    mac_address: str
    version: str
    date: datetime.date


@dataclass
class GetTimeResponse:
    '''
    Container class for the decoded response from a get-time request.

       Fields:
          controller   (uint32)    Controller serial number.
          datetime     (datetime)  Controller system date/time.
    '''
    controller: int
    datetime: datetime.datetime


@dataclass
class SetTimeResponse:
    '''
    Container class for the decoded response from a set-time request.

       Fields:
          controller   (uint32)    Controller serial number.
          datetime     (datetime)  Controller system date/time.
    '''
    controller: int
    datetime: datetime.datetime


@dataclass
class GetStatusResponse:
    '''
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
    '''
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


@dataclass
class GetListenerResponse:
    '''
    Container class for the decoded response from a get-listener request.

       Fields:
          controller  (uint32)       Controller serial number.
          address     (IPv4Address)  Configured event listener IP address.
          port        (uint16)       Configured event listener UDP port.
    '''
    controller: int
    address: IPv4Address
    port: int


@dataclass
class SetListenerResponse:
    '''
    Container class for the decoded response from a set-listener request.

       Fields:
          controller  (uint32)  Controller serial number.
          ok          (bool)    Succeeded/failed.
    '''
    controller: int
    ok: bool


@dataclass
class GetDoorControlResponse:
    '''
    Container class for the decoded response from a get-door-control request.

       Fields:
          controller  (uint32)  Controller serial number.
          door        (uint8)   Door no.[1..4]
          mode        (uint8)   Door control mode (1: normally open, 2: normally closed, 3: controlled)
          delay       (uint8)   Door unlock duration (seconds)
    '''
    controller: int
    door: int
    mode: int
    delay: int


@dataclass
class SetDoorControlResponse:
    '''
    Container class for the decoded response from a set-door-control request.

       Fields:
          controller  (uint32)  Controller serial number.
          door        (uint8)   Door no.[1..4]
          mode        (uint8)   Door control mode (1: normally open, 2: normally closed, 3: controlled)
          delay       (uint8)   Door unlock duration (seconds)
    '''
    controller: int
    door: int
    mode: int
    delay: int


@dataclass
class OpenDoorResponse:
    '''
    Container class for the decoded response from an open-door request.

       Fields:
          controller  (uint32)  Controller serial number.
          opened      (bool)    Succeeded/failed.
    '''
    controller: int
    opened: bool


@dataclass
class GetCardsResponse:
    '''
    Container class for the decoded response from an open-door request.

       Fields:
          controller  (uint32)  Controller serial number.
          cards       (uint32)  Number of cards stored on controller.
    '''
    controller: int
    cards: int


@dataclass
class GetCardResponse:
    '''
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
    '''
    controller: int
    card_number: int
    start_date: datetime.date
    end_date: datetime.date
    door_1: int
    door_2: int
    door_3: int
    door_4: int
    pin: PIN


@dataclass
class GetCardByIndexResponse:
    '''
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
    '''
    controller: int
    card_number: int
    start_date: datetime.date
    end_date: datetime.date
    door_1: int
    door_2: int
    door_3: int
    door_4: int
    pin: PIN


@dataclass
class PutCardResponse:
    '''
    Container class for the decoded response from an open-door request.

       Fields:
          controller  (uint32)  Controller serial number.
          stored      (bool)    Succeeded/failed.
    '''
    controller: int
    stored: bool


@dataclass
class DeleteCardResponse:
    '''
    Container class for the decoded response from a delete-card request.

       Fields:
          controller  (uint32)  Controller serial number.
          deleted     (bool)    Succeeded/failed.
    '''
    controller: int
    deleted: bool


@dataclass
class DeleteAllCardsResponse:
    '''
    Container class for the decoded response from a delete-all-cards request.

       Fields:
          controller  (uint32)  Controller serial number.
          deleted     (bool)    Succeeded/failed.
    '''
    controller: int
    deleted: bool


@dataclass
class GetEventResponse:
    '''
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
    '''
    controller: int
    index: int
    event_type: int
    access_granted: bool
    door: int
    direction: int
    card: int
    timestamp: datetime.datetime
    reason: int


@dataclass
class GetEventIndexResponse:
    '''
    Container class for the decoded response from a get-event-index request.

       Fields:
          controller      (uint32)    Controller serial number.
          index           (uint32)    Downloaded event index.
    '''
    controller: int
    event_index: int


@dataclass
class SetEventIndexResponse:
    '''
    Container class for the decoded response from a set-event-index request.

       Fields:
          controller  (uint32)  Controller serial number.
          updated     (bool)    Succeeded/failed.
    '''
    controller: int
    updated: bool


@dataclass
class RecordSpecialEventsResponse:
    '''
    Container class for the decoded response from a record-special-events request.

       Fields:
          controller  (uint32)  Controller serial number.
          updated     (bool)    Succeeded/failed.
    '''
    controller: int
    updated: bool


@dataclass
class GetTimeProfileResponse:
    '''
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
    '''
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


@dataclass
class SetTimeProfileResponse:
    '''
    Container class for the decoded response from a set-time-profile request.

       Fields:
          controller  (uint32)  Controller serial number.
          stored      (bool)    Succeeded/failed.
    '''
    controller: int
    stored: bool


@dataclass
class DeleteAllTimeProfilesResponse:
    '''
    Container class for the decoded response from a delete-all-time-profiles request.

       Fields:
          controller  (uint32)  Controller serial number.
          deleted     (bool)    Succeeded/failed.
    '''
    controller: int
    deleted: bool


@dataclass
class AddTaskResponse:
    '''
    Container class for the decoded response from an add-task request.

       Fields:
          controller  (uint32)  Controller serial number.
          added       (bool)    Succeeded/failed.
    '''
    controller: int
    added: bool


@dataclass
class RefreshTasklistResponse:
    '''
    Container class for the decoded response from a refersh-tasklist request.

       Fields:
          controller  (uint32)  Controller serial number.
          refreshed   (bool)    Succeeded/failed.
    '''
    controller: int
    refreshed: bool


@dataclass
class ClearTasklistResponse:
    '''
    Container class for the decoded response from a clear-tasklist request.

       Fields:
          controller  (uint32)  Controller serial number.
          cleared     (bool)    Succeeded/failed.
    '''
    controller: int
    cleared: bool


@dataclass
class SetPcControlResponse:
    '''
    Container class for the decoded response from a set-pc-control request.

       Fields:
          controller  (uint32)  Controller serial number.
          ok          (bool)    Succeeded/failed.
    '''
    controller: int
    ok: bool


@dataclass
class SetInterlockResponse:
    '''
    Container class for the decoded response from a set-interlock request.

       Fields:
          controller  (uint32)  Controller serial number.
          ok          (bool)    Succeeded/failed.
    '''
    controller: int
    ok: bool


@dataclass
class ActivateKeypadsResponse:
    '''
    Container class for the decoded response from an activate-keypads request.

       Fields:
          controller  (uint32)  Controller serial number.
          ok          (bool)    Succeeded/failed.
    '''
    controller: int
    ok: bool


@dataclass
class Event:
    '''
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
    '''
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
