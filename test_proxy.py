import requests

proxy = "190.61.88.147:8080"


r = requests.get("https://httpbin.org/ip", proxies={'http': proxy, 'https': proxy}, timeout=3)


print(r.json())