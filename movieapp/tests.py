from django.test import TestCase

# Create your tests here.
import requests
import json

url = 'https://movie.vandit.cf/home?suggest=shows'
response = requests.get(
    url
)
print(response._content)