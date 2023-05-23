from calendar import c
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode
import pandas as pd
import chromedriver_autoinstaller

from bs4 import BeautifulSoup
import requests
 
chromedriver_autoinstaller.install() 

PROXY = "IpOfTheProxy:PORT"
# Create Chromeoptions instance 
options = webdriver.ChromeOptions() 
 
# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
 
#options.add_argument("--proxy-server=%s" % PROXY)

# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 
options.add_argument("headless")
 
def create_session(driver,url,options):
    driver = webdriver.Chrome(options=options) 

    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    driver.get(url)

def get_data(num_properties = 20,verbose=True):
    #options = Options()
    options.add_argument("start-maximized")
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape zoopa
    #url = "https://www.zoopla.co.uk/"

    properties = []
    for code in postcode:
        while len(properties) < (num_properties+1):
            
            print("\nstarting new postcode")
            
            # loop to handle transaction type i.e sale or rent
            for i in range(2):
                for j in range(13):
                
                    print("\nstarting new property type")
                
                #time.sleep(10)
                
                    if i == 0:
                        Transaction_type = "Sale"
                        if j < 1:
                            url = f"https://www.zoopla.co.uk/for-sale/property/{code}/?q={code}&search_source=home"
                        else:
                            url = f"https://www.zoopla.co.uk/for-sale/property/{code}/?q={code}&search_source=home&pn={j+1}"
                    else:
                        Transaction_type = "Rent"
                        if j < 1:
                            url = f"https://www.zoopla.co.uk/to-rent/property/{code}/?price_frequency=per_month&q={code}&search_source=home"
                        else:
                            url = f"https://www.zoopla.co.uk/to-rent/property/{code}/?price_frequency=per_month&q={code}&search_source=home&pn={j+1}"
                    # Setting the driver path and requesting a page 
                    driver = webdriver.Chrome(options=options) 
 
                    # Changing the property of the navigator value for webdriver to undefined 
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

                    driver.get(url)
                    time.sleep(10)
                    try:
                        driver.find_element(By.XPATH,'//*[@id="radix-:r0:"]/main/div[1]/button').click() #clicking to the X.
                        print(' x out worked')
                    except NoSuchElementException:
                        print(' x out failed')
                        pass
                    property = driver.find_elements(By.XPATH, '//div[@class="f0xnzq2"]')

                    # collect list of properties urls
                    
                    property_urls = [p.find_element(By.TAG_NAME, "a").get_attribute("href") for p in property]

                    print(property_urls)

                    driver.close()

                    for url in property_urls:
                        req = requests.get(url + ".html")
                        soup = BeautifulSoup(req.content, "html.parser")
                        price = soup.find("p", {"data-testid": "price"})
                        print(price)
# _1ljm00u2 _1ljm00u7 _1ljm00u1n _1ljm00u3n _1ftx2fq4
get_data()