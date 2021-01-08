import json

with open('events_raw.jsonl', 'r') as json_file:
    json_list = list(json_file)

events = []
organizers = []
for json_str in json_list:
    result = json.loads(json_str)
    organizer = {}
    if "action" in result:
        del result["action"]
    del result["appid"]
    del result["attrs"]
    del result["crawlid"]
    #del result["item_type"]
    del result["logger"]
    del result["spiderid"]
    del result["timestamp"]
    if result['item_type'] == 'event':

        events.append(result)
        print(result['event_name'],result['event_url'],result['organizer_name'])
    if  result['item_type'] == 'organizer':
        organizers.append(result)
        print(result['organizer_profile_url'])

print("No. of Events: ", len(events))
print("No. of Organizers: ", len(organizers))

reformed_events = []
for event in events:
    del event["item_type"]
    #del event["action"]
    location = {}
    if event['venue_name'] != '': 
        location['venue_name'] =event['venue_name']
        del event['venue_name']
    if 'street_address_1' in event:
        location['street_address_1'] = event['street_address_1']
        del event['street_address_1']
    if 'street_address_2' in event:
        location['street_address_2'] = event['street_address_2']
        del event['street_address_2']
    if 'city' in event:
        location['city'] = event['city']
        del event['city']
    if 'state' in event:
        location['state'] = event['state']
        del event['state']
    if 'country' in event:
        location['country'] = event['country']
        del event['country']
    event['event_location'] = location
    organizer_name = event['organizer_name']
    del event['organizer_name']
    for organizer in organizers:
        if organizer['organizer_profile_url'] == event['organizer_profile_url']:
            organizer['organizer_name'] = organizer_name
            if 'item_type' in organizer:
                del organizer['item_type']
            event['event_organizer'] = organizer
            break
    if "organizer_profile_url" in event:
    	del event["organizer_profile_url"]

    reformed_events.append(event)
    
print(json.dumps(reformed_events[0]))
with open("events_US.jsonl", 'w') as f:
    for item in reformed_events:
        f.write(json.dumps(item) + "\n")