'''
Expected responses for UHPPOTE integration tests.
'''

import datetime
import ipaddress

from uhppoted import structs

GetControllerResponse = structs.GetControllerResponse(
    controller=405419896, 
    ip_address=ipaddress.IPv4Address('192.168.1.100'), 
    subnet_mask=ipaddress.IPv4Address('255.255.255.0'), 
    gateway=ipaddress.IPv4Address('192.168.1.1'), 
    mac_address='00:12:23:34:45:56', 
    version='v8.92', 
    date=datetime.date(2018, 11, 5))

SetIPResponse = True

GetTimeResponse = structs.GetTimeResponse(
    controller=405419896, 
    datetime=datetime.datetime(2021, 5, 28, 13, 51, 30))
        
SetTimeResponse = structs.SetTimeResponse(
    controller=405419896, 
    datetime=datetime.datetime(2021, 5, 28, 14, 56, 14))

GetStatusResponse = structs.GetStatusResponse(
    controller=405419896, 
    system_date=datetime.date(2021, 5, 28), 
    system_time=datetime.time(15, 14, 46), 
    door_1_open=False, 
    door_2_open=False, 
    door_3_open=False, 
    door_4_open=False, 
    door_1_button=False, 
    door_2_button=False, 
    door_3_button=False, 
    door_4_button=False, 
    relays=0, 
    inputs=0, 
    system_error=0, 
    special_info=0, 
    event_index=69, 
    event_type=2, 
    event_access_granted=True, 
    event_door=1, 
    event_direction=1, 
    event_card=0, 
    event_timestamp=datetime.datetime(2019, 8, 10, 10, 28, 32), 
    event_reason=44, 
    sequence_no=0)

GetListenerResponse = structs.GetListenerResponse(
    controller=405419896, 
    address=ipaddress.IPv4Address('192.168.1.100'), 
    port=60001)

SetListenerResponse = structs.SetListenerResponse(
    controller=405419896, 
    ok=True)

GetDoorControlResponse = structs.GetDoorControlResponse(
    controller=405419896, 
    door=3, 
    mode=3, 
    delay=7)

SetDoorControlResponse = structs.SetDoorControlResponse(
    controller=405419896, 
    door=3, 
    mode=2, 
    delay=4)

OpenDoorResponse = structs.OpenDoorResponse(
    controller=405419896, 
    opened=True)

GetCardsResponse = structs.GetCardsResponse(
    controller=405419896, 
    cards=3)

GetCardResponse = structs.GetCardResponse(
    controller=405419896, 
    card_number=8165538, 
    start_date=datetime.date(2023, 1, 1), 
    end_date=datetime.date(2023, 12, 31), 
    door_1=1, 
    door_2=0, 
    door_3=29, 
    door_4=1, 
    pin=7531)

GetCardByIndexResponse = structs.GetCardByIndexResponse(
    controller=405419896, 
    card_number=8165539, 
    start_date=datetime.date(2023, 1, 1), 
    end_date=datetime.date(2023, 12, 31), 
    door_1=1, 
    door_2=0, 
    door_3=29, 
    door_4=1, 
    pin=7531)

PutCardResponse = structs.PutCardResponse(
    controller=405419896, 
    stored=True)

DeleteCardResponse = structs.DeleteCardResponse(
    controller=405419896, 
    deleted=True)

DeleteAllCardsResponse = structs.DeleteAllCardsResponse(
    controller=405419896, 
    deleted=True)

GetEventResponse = structs.GetEventResponse(
    controller=405419896, 
    index=29, 
    event_type=2, 
    access_granted=True, 
    door=1, 
    direction=1, 
    card=0, 
    timestamp=datetime.datetime(2019, 8, 3, 10, 34, 29), 
    reason=0)

GetEventIndexResponse = structs.GetEventIndexResponse(
    controller=405419896, 
    event_index=23) 

SetEventIndexResponse = structs.SetEventIndexResponse(
    controller=405419896, 
    updated=True)

RecordSpecialEventsResponse = structs.RecordSpecialEventsResponse(
    controller=405419896, 
    updated=True)

GetTimeProfileResponse = structs.GetTimeProfileResponse(
    controller=405419896, 
    profile_id=29, 
    start_date=datetime.date(2021, 4, 1), 
    end_date=datetime.date(2021, 12, 31), 
    monday=True, 
    tuesday=False, 
    wednesday=True, 
    thursday=False, 
    friday=True, 
    saturday=False, 
    sunday=False, 
    segment_1_start=datetime.time(8, 30), 
    segment_1_end=datetime.time(11, 30), 
    segment_2_start=datetime.time(0, 0), 
    segment_2_end=datetime.time(0, 0), 
    segment_3_start=datetime.time(13, 45), 
    segment_3_end=datetime.time(17, 0), 
    linked_profile_id=3)

SetTimeProfileResponse = structs.SetTimeProfileResponse(
    controller=405419896, 
    stored=True)

DeleteAllTimeProfilesResponse = structs.DeleteAllTimeProfilesResponse(
    controller=405419896, 
    deleted=True)

AddTaskResponse = structs.AddTaskResponse(
    controller=405419896, 
    added=True)

RefreshTaskListResponse = structs.RefreshTasklistResponse(
    controller=405419896, 
    refreshed=True)

ClearTaskListResponse = structs.ClearTasklistResponse(
    controller=405419896, 
    cleared=True)

SetPCControlResponse = structs.SetPcControlResponse(
    controller=405419896, 
    ok=True)

SetInterlockResponse = structs.SetInterlockResponse(
    controller=405419896, 
    ok=True)

ActivateKeypadsResponse = structs.ActivateKeypadsResponse(
    controller=405419896, 
    ok=True)

SetDoorPasscodesResponse = structs.SetDoorPasscodesResponse(
    controller=405419896, 
    ok=True)

RestoreDefaultParametersResponse = structs.RestoreDefaultParametersResponse(
    controller=405419896, 
    reset=True) 
