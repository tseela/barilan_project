import requests
import json
import ast

url = "https://transit.router.hereapi.com/v8/routes?apiKey=pGwbEV9EnOVSNh94i8prG-B4oBd8RSO8bP6lk_u6NXI&origin=41.79457,12.25473&destination=41.90096,12.50243"

response = requests.get(url)

# print(response.text)
# print(dict(response.text))
d = ast.literal_eval(response.text)

print(json.dumps(d, sort_keys=False, indent=4))
# print(response.__dict__)
