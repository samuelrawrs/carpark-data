# carpark-data
This repository pulls data from https://api.data.gov.sg/v1/transport/carpark-availability every hour using Github Actions. Raw results are stored in /data using `script.py`

Everytime new data arrives, `data_parser_usingdict.py` checks for when `carpark_data.json` is last updated and appends the unupdated data to the dictionary in `final_carpark_data.json`

`final_carpark_data.json` is a dictionary where the **keys** are the **carpark numbers** while the **values** are ordered in the following manner:

```
carpark_number: [
				lot_type,
				lots_available (at time1),
				total_lots,
				time,
				lots_available (at time2),
				time2,
				lots_available (at time3),
				time3,
				...]
```
The end of the file also containts a `timestamp` that indicates when the file was last updated. Admittedly, I would've prefered for the appending of `lots_available` to be in the form of a nested list to seperate each timing nicely but unfortunately this was the best way I could find combining dictionaries with similar keys.

## Note
Stopped on 8/3/2022. Github actions failed after new carparks was added to the data and broke my code OOPS. looks like combining dictionaries with different keys was the problem... D:							
							
## Future Developments
~~- Parse data from /data to create a master file for each carpark.~~ done!
- Automate a graph from the data that updates over time.
