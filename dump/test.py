from bs4 import BeautifulSoup
import requests


req = requests.get("https://www.onthemarket.com/details/13123519/")
soup = BeautifulSoup(req.content, "html.parser")
#print(soup)
#price = soup.find_all("div")
price = soup.find("div", {"class": "otm-Price"})
print(price)
print(req)