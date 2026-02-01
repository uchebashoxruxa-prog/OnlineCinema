from django.test import TestCase
import requests
# Create your tests here.

HEADERS = {
    'Authorization': 'Token 5e2146abf58df7e167b8e0254c92cc519a9ebece'
}
cinemas = requests.get('http://127.0.0.1:8000/api/v1/cinemas/', headers=HEADERS).json()
print(cinemas)