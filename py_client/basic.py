import requests

#endpoint = "https://httpbin.org/status/200" # Generates responses with given status code
#endpoint = "https://httpbin.org/anything"
endpoint = "http://127.0.0.1:8000/api/"

get_response = requests.post(endpoint, params={'abs': 123}, json={'title': 'ol', 'content': 'content'}) # API -> method
print(get_response.json())

# HTTP REQUEST -> HTML
# REST API HTTP -> JSON (xml)