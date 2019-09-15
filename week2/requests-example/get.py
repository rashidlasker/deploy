import requests
import json

resp = requests.get('http://67.207.94.120:5000/dweets')
dweets = json.loads(resp.content)

print('10 dweets:')
print(dweets)
print('Individual dweet:')
print(dweets[0])

