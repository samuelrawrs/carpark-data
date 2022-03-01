import json
from json import JSONEncoder
import os
from datetime import datetime


def convert_data_time(time_data):
    try:
        time_data = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S+08:00')
    except ValueError:
        time_data = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S')
    return (time_data)

with open('data/Results 01-03-2022 135932.json', 'r') as file:
    data = json.loads(file.read())

pairs = data.items()

new_dict={}
carpark_dict={}

for k, v in pairs: #items, etc...
    for x in v: #somehow this is a list wth
        new_dict = x

last_global_update = new_dict["timestamp"]
last_global_update = convert_data_time(last_global_update) ## first check if global update time is similar

for a in new_dict["carpark_data"]:
    carpark_dict[a["carpark_number"]] = ([a["carpark_info"][0]["lot_type"], a["carpark_info"][0]["lots_available"], a["carpark_info"][0]["total_lots"]], convert_data_time(a["update_datetime"]))

json_object = json.dumps(carpark_dict, indent = 4, sort_keys = True, default = str)
f = open("carpark_data.txt", "a")
f.write(json_object)
f.close()


# carparks = []
# counter = 0
# for a in new_dict["carpark_data"]:
#     carparks.append(Carpark(a["carpark_number"]))
#     carparks[counter].update_time = convert_data_time(a["update_datetime"])
#     for b in a["carpark_info"]:
#         carparks[counter].lot_type = b["lot_type"]
#         carparks[counter].lots_available = b["lots_available"]
#         carparks[counter].total_lots = b["total_lots"]
#     counter+=1


# print(repr(carparks[0]))