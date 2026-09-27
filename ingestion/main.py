import requests
from datetime import datetime
import time

import pandas as pd

stations = ["Namur", "Gent-Sint-Pieters", "Luxembourg", "Hugo", "Liège", "Anvers"]

v_counter = 0
f_counter = 0
rows = []
for station in stations:

    f_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        rr = requests.get(f'https://api.irail.be/v1/liveboard?station={station}&format=json&lang=fr')
        status = rr.status_code

        if status == 200:

            data = rr.json()
            departures = data["departures"]["departure"]

            for departure in departures:
                row = {
                    "destination": departure["station"],
                    "delay": departure["delay"],
                    "time": departure["time"],
                    "canceled": departure["canceled"],
                    "platform": departure["platform"],
                    "train_type": departure["vehicleinfo"]["type"],
                    "source_station": station,
                    "ingested_at": f_time,
                }
                rows.append(row)

            v_counter += 1

        else:
            print(f"Failed for {station}: {status}")
            f_counter += 1

    except requests.exceptions.RequestException as e:
        print(f"Network error for {station}: {e}")
        f_counter += 1

    time.sleep(0.5)

print(f"{v_counter} succeeded, {f_counter} failed, {len(rows)} departures collected")

df = pd.DataFrame(rows)
df.to_parquet(f"data/bronze/departures_{f_time}.parquet", index=False)

print(df.shape)
print(df.head())