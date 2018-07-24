import requests

r = requests.get('https://z-monitor.ru/api/v2/profile/?sessionID=ua69d201edk6pk49eu7qditt82&device=android')
print(r.json()['data']['email'])
