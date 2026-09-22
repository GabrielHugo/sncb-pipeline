import requests
from datetime import datetime

f_time = datetime.now().strftime("%Y%m%d_%H%M%S")

bronze_file = f"data/bronze/namur_{f_time}.json"

x = requests.get('https://api.irail.be/v1/liveboard?station=Namur&format=json&lang=fr')

with open(bronze_file, "w", encoding="utf-8") as f:
    f.write(x.text)