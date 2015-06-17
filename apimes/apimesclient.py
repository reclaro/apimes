from requests import get
from requests import post


res = post('http://localhost:5000/cars', data={'data': 'New car record'}).json()
print res
# pasing not in form-encoded, just pass a string
res = post('http://localhost:5000/cars', data='New car record')
print res.text
