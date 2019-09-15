import requests

dweet = {
        'message': 'example!',
        'username': 'deploy'
        }

resp = requests.post('http://67.207.94.120:5000/new', data=dweet)

print(resp)
