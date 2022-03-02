import json
import glob
from datetime import datetime
from collections import Counter

def convert_data_time(time_data):
    try:
        time_data = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S+08:00')
    except ValueError:
        try:
            time_data = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S')
        except:
            try:
                time_data = datetime.strptime(time_data, '%d-%m-%Y %H%M%S')
            except:
                time_data = datetime.strptime(time_data, '%Y-%m-%d %H:%M:%S')
    return (time_data)

def datadate_to_datetime(list): #convert file names to datetime
    list2 = []
    list3 = []
    for a,b in list:
        b = b.strip(' data/Results.json')
        list2.append([a,b])
    for a,b in list2:
        b = convert_data_time(b)
        list3.append([a,b])
    return list3


def jsonfile_to_firstdict(filename):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        pairs = data.items()
        new_dict={}
        carpark_dict={}

        for k, v in pairs: #items, etc...
            for x in v: #somehow this is a list wth
                new_dict = x

        last_global_update = new_dict["timestamp"]
        last_global_update = convert_data_time(last_global_update) ## update file with update time
        carpark_dict["timestamp"] = str(last_global_update)

        for a in new_dict["carpark_data"]:
            carpark_dict[a["carpark_number"]] = ([a["carpark_info"][0]["lot_type"], a["carpark_info"][0]["lots_available"], a["carpark_info"][0]["total_lots"], convert_data_time(a["update_datetime"])])

        return carpark_dict

def jsonfile_to_nextdict(filename):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        pairs = data.items()
        new_dict={}
        carpark_dict={}

        for k, v in pairs: #items, etc...
            for x in v: #somehow this is a list wth
                new_dict = x

        last_global_update = new_dict["timestamp"]
        last_global_update = convert_data_time(last_global_update) ## update file with update time
        carpark_dict["timestamp"] = str(last_global_update)

        for a in new_dict["carpark_data"]:
            carpark_dict[a["carpark_number"]] = [a["carpark_info"][0]["lots_available"], convert_data_time(a["update_datetime"])]
        return carpark_dict

def combine_dict(d1, d2):
    d3 = {x: d1.get(x, 0) + d2.get(x, 0) for x in set(d1).union(d2)}
    d3["timestamp"] = d2["timestamp"] #last updated time
    return(d3)


def combine_dict2(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = [value , dict_1[key]]
   return dict_3

def main():
    new_results_list = []

    try: #compare old data with new results in /data
        with open("carpark_data.json", 'r') as f:
            old_data = json.load(f)
        carpark_data_time = convert_data_time(old_data["timestamp"]) #check time of old data
        data_list = glob.glob("data/*")
        data_list = sorted(list(enumerate(data_list)), key=lambda x:x[1]) #enumerate to keep track of file name
        data_dict = {k[0]: k[1] for k in data_list} #converted to dictionary to help us reference later

        data_list_converted = datadate_to_datetime(data_list)
        for a,b in data_list_converted:
            if carpark_data_time<b: #carpark_data.json is outdated
               new_results_list.append(a)
        d = old_data
        final_dict = {}
        for i in new_results_list: #now we can open the data files in the right order to append
            new_carpark_dict = jsonfile_to_nextdict(data_dict[i])
            d = combine_dict(d,new_carpark_dict)
        new_json = json.dumps(d, indent = 4, sort_keys = True, default = str)
        f = open("final_carpark_data.json", "w")
        f.write(new_json)
        f.close()



    except IOError: #remake carpark_data.json from 01-03-2022 135932 results
        print("File not found, making a new file.")
        first_carpark_dict = jsonfile_to_firstdict('data/Results 01-03-2022 135932.json')
        json_object = json.dumps(first_carpark_dict, indent = 4, sort_keys = True, default = str)
        f = open("carpark_data.json", "a")
        f.write(json_object)
        f.close()

if __name__ == "__main__":
    main()