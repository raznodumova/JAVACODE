# Запрос с использованием библиотеки requests

# import requests
# from pprint import pprint
#
# BASE_URL = "https://www.google.com"
#
# response = requests.get(BASE_URL)
# status = response.status_code
# data = response.text
# pprint(status)
# pprint(data[:100])

#Сырой запрос

GET / HTTP/1.1
Host: www.google.com
Content-Type: text/html
User-Agent: Yandex/1.0
Accept-Language: ru
