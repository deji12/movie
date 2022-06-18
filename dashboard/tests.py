from django.test import TestCase
import datetime

# Create your tests here.

def calculate_time(current_time=input('Input Time: ')):
    splitted_time = current_time.split(':')[0]
    
