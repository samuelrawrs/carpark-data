from collections import namedtuple
import json
from json import JSONEncoder
import os
from datetime import datetime

new_dict = {}
carpark_list = []
class Carpark:
    def __init__(self, number):
        self.number = number
        self.lot_type = ""
        self.lots_available = 0
        self.total_lots = 0
        self.update_time = ""
    def capacity(self):
        percentage = float(int(self.lots_available)/int(self.total_lots))
        return(percentage)

    def __repr__(self):
        return f'Carpark:"{self.number}", Info:"{self.lot_type}",{self.lots_available},{self.total_lots},{self.update_time}'
    def __str__(self):
        return f'Carpark:"{self.number}", Capacity:"{self.capacity()}"'


def convert_data_time(time_data):
    try:
        time_data = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S+08:00')
    except ValueError:
        time_data = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S')
    return (time_data)

# didn't work
# def object_decoder(carpark_dict):
#     return namedtuple('X', carpark_dict.keys())(*carpark_dict.values())

with open('test_data.json', 'r') as file:
    data = file.read()

json_object = json.loads(data)
pairs = json_object.items()

for k, v in pairs: #items, etc...
    for x in v: #somehow this is a list wth
        new_dict = x

last_global_update = new_dict["timestamp"]
last_global_update = convert_data_time(last_global_update) ## first check if global update time is similar

carparks = []
counter = 0
for a in new_dict["carpark_data"]:
    carparks.append(Carpark(a["carpark_number"]))
    carparks[counter].update_time = convert_data_time(a["update_datetime"])
    for b in a["carpark_info"]:
        carparks[counter].lot_type = b["lot_type"]
        carparks[counter].lots_available = b["lots_available"]
        carparks[counter].total_lots = b["total_lots"]
    counter+=1


# print(carparks[1].capacity())
# print(carparks[1].lots_available)
# print(carparks[1].total_lots)

print(repr(carparks[0]))