from django.test import TestCase

# Create your tests here.
import requests
import json

response = requests.get(
    url  = 'http://127.0.0.1:8000/api/all-movies/'
)


print(response._content)