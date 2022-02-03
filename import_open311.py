import csv
import datetime
import json
import requests
from time import sleep

OPEN311_BASE_URL = "https://asiointi.hel.fi/palautews/rest/v1/requests.json"


def import_open311(years: int = 2) -> dict:
    now = datetime.datetime.now()
    start_time = now - datetime.timedelta(days=years * 365)
    print(now)
    print(start_time)
    data = []
    while start_time < now:
        # Here we have to do some assumptions about the amount of data available.
        # It looks like two weeks or so give < 200 entries, which is the maximum.
        # To be on the safe side, fetch the entries week by week and raise an
        # exception if something is missing.
        end_time = start_time + datetime.timedelta(weeks=1)
        print(f"Fetching data from {start_time} to {end_time}")
        response = requests.get(
            OPEN311_BASE_URL,
            params={
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
            },
        )

        # save the response to file AND dict, so we get a local backup
        # of all the responses and will not have to spam the API ever again
        received_data = json.loads(response.text)
        if isinstance(received_data, list):
            if len(received_data) > 0:
                print(f"Found {len(received_data)} results, saving...")
                data.extend(received_data)
            else:
                print(f"No results found from {start_time} to {end_time}")
        else:
            print(received_data)

        # Here we rewrite the whole file every time. Easier than having to
        # remove the JSON ending tokens and paste the JSONs together every time IMO.
        # If this gets too slow, fix it.
        with open("data/data.json", "w") as file:
            json.dump(data, file)

        # do not flood the API
        sleep(0.5)
        start_time = end_time
    return data
