import requests

url = "https://test.api.amadeus.com/v1/security/oauth2/token"

payload='grant_type=client_credentials&client_id=CGwOmHn7cmfAIuUcbqUiaPC5LAyAvwAG&client_secret=rKvILHDsjxcCh6yq'
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)