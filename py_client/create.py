import requests
from getpass import getpass

endpoint = "http://127.0.0.1:8000/api/auth/"
username = input('What is ur username?\n')
password = getpass()
auth_response = requests.post(endpoint, json={'username': username, 'password': password})

endpoint = "http://127.0.0.1:8000/api/products/"
token = auth_response.json() ['token']
print(token)
headers = {
    'Authorization': f'Bearer {token}'
}
endpoint = "http://127.0.0.1:8000/api/products/"
get_response = requests.get(endpoint, headers=headers) # API -> method
print(get_response.json())