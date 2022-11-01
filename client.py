import requests

search_image = '3.jpg'
search_url = 'http:localhost:5000/static/uploads/{}'.format(search_image)

response = requests.get(search_url)
