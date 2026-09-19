import requests

x = requests.get('https://api.irail.be/v1/liveboard?station=Namur&format=json&lang=fr')
print(x.json())