from bs4 import BeautifulSoup
import requests


req = requests.get("https://www.zoopla.co.uk/for-sale/details/64657234/?search_identifier=9e8656ea15397ce789e5fe04f4239450fc00994d5991be60f5a65d9aa77394" + ".html")
soup = BeautifulSoup(req.content, "html.parser")
#print(soup)
#price = soup.find_all("div")
price = soup.find("div", {"class": "main-content"}).find("a")
print(price)