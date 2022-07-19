from django.test import TestCase

# Create your tests here.
import requests
import json

# url = 'https://movie.vandit.cf/home?suggest=shows'
# response = requests.get(
#     url
# )
# print(response._content)

test = 'season: Never Have I Ever | Season 1'
split_season = test.split("|")[1]
print(split_season.split(" ")[2])