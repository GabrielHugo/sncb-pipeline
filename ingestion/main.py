import requests
from datetime import datetime
import time

stations = ["Namur", "Gent-Sint-Pieters", "Luxembourg", "Hugo", "Liège", "Anvers"]

v_counter = 0
f_counter = 0

for station in stations :

    f_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    bronze_file = f"data/bronze/{station}_{f_time}.json"

    try:

        rr = requests.get(f'https://api.irail.be/v1/liveboard?station={station}&format=json&lang=fr')

        status = rr.status_code

        if status == 200:

            with open(bronze_file, "w", encoding="utf-8") as f:
                f.write(rr.text)

            v_counter+=1

        else:
              print(f"Failed for {station}: {status}")
              f_counter+=1

    except requests.exceptions.RequestException as e:
        print(f"Error for {station} : {e}")
        f_counter+=1

    time.sleep(0.5)

print(f"{v_counter} victory")
print(f"{f_counter} failure")