from calendar import c
from cmath import nan
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode_batch9, borough_batch9
import pandas as pd
import chromedriver_autoinstaller
import logging
from datetime import date


logging.basicConfig(filename='./logs/zoopla.log', filemode='a', format='%(levelname)s - %(asctime)s - %(message)s',level=logging.INFO)

start = time.time()
 
chromedriver_autoinstaller.install() 

PROXY = "103.225.11.135:80"
# Create Chromeoptions instance 
options = webdriver.ChromeOptions() 
 
# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
 
#options.add_argument("--proxy-server=%s" % PROXY)

# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 
#options.add_argument("--headless")
 
def create_session(driver,url,options):
    driver = webdriver.Chrome(options=options)

    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    driver.get(url)


def scrape_urls(p, properties, code, town, Transaction_type, connected=True):
    counter = 0
    
    
             
    # get property details
    result_id = p.get_attribute("id")       
    location = p.find_element(By.TAG_NAME, 'h3').text
    price = p.find_element(By.XPATH, '//p[@data-testid="listing-price"]').text
    property_type = p.find_element(By.XPATH, f'//*[@id="{result_id}"]/div[1]/div/div/div/div[2]/div/a/div/div[3]/h2').text
    
    
    print("result id: ",result_id)
    try:
        bedroom = p.find_element(By.XPATH, f'//*[@id="{result_id}"]/div[1]/div/div/div/div[2]/div/a/div/div[2]/ul/li[1]/span[2]').text
    except:
        bedroom = None

    try:
        bathroom = p.find_element(By.XPATH, f'//*[@id="{result_id}"]/div[1]/div/div/div/div[2]/div/a/div/div[2]/ul/li[2]/span[2]').text
    except:
        bathroom = None

    try:
        agent_logo = p.find_element(By.XPATH, f'//*[@id="{result_id}"]/div[1]/div/div/div/div[3]/a/img')
        agent = agent_logo.get_attribute("alt")
    except:
        agent = None

    
    

    print("address: ", location)
    print(price)
    print("agent: ", agent)
    print("bed: ", bedroom)
    print("bath: ", bathroom)
    print(property_type)
    
    a = p.find_element(By.TAG_NAME, "a")
    listing_url = a.get_attribute("href")
    print(listing_url)
    print("p id : ", result_id)



    
    properties.append({"Result_id" : result_id,
    "Transaction_type" : Transaction_type,
    "Bedroom" : bedroom,
    "Bathroom" : bathroom,
    "Property_type" : property_type,
    "Price" : price,
    "Location" : location,
    "Agent" : agent,
    "Listing_url" : listing_url,
    "postcode" : code,
    "Borough" : town,
    "Date" : date.today()
    })

        
            
            

        
        

    return properties


def get_data(verbose=True):
    #options = Options()
    options.add_argument("start-maximized")
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape zoopa
    fails = 0
    properties = []

    # scrape by postcode
    for code, town in zip(postcode_batch9, borough_batch9):
        
        print("\nstarting new postcode")
        
        #  ourter loop to handle transaction type i.e sale or rent
        for i in range(2):
            
            for j in range(20):   # range to cover number of pages
            
                print("\nstarting new page")
            
            
                # generate urls based on transaction type, postcode and page number
                if i == 0:
                    logging.info("Started scrapping for Sale")
                    Transaction_type = "Sale"
                    if j < 1:
                        url = f"https://www.zoopla.co.uk/for-sale/property/{code}/?q={code}&search_source=home"
                    else:
                        url = f"https://www.zoopla.co.uk/for-sale/property/{code}/?q={code}&search_source=home&pn={j+1}"
                else:
                    logging.info("Started scrapping for Rent")
                    Transaction_type = "Rent"
                    if j < 1:
                        url = f"https://www.zoopla.co.uk/to-rent/property/{code}/?price_frequency=per_month&q={code}&search_source=home"
                    else:
                        url = f"https://www.zoopla.co.uk/to-rent/property/{code}/?price_frequency=per_month&q={code}&search_source=home&pn={j+1}"   #{j+1}

                # Setting the driver path and requesting a page 
                driver = webdriver.Chrome(options=options)

                # Changing the property of the navigator value for webdriver to undefined 
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                # launch browser to specified url
                try:
                    driver.get(url)
                except:
                    print("Page url not valid")
                    break
                try:
                    time.sleep(3)
                    web_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[4]/div[2]/section/div[2]/div[2]/h2').text
                    if web_element == "No results found":
                        print("page ends")
                        break
                except:
                    pass
                time.sleep(3)
                try:
                    # get webelement of properties on page
                    property = driver.find_elements(By.XPATH, '//div[@class="f0xnzq2"]')
                    #print("Prop: ",property)
                except:
                    print("Property not reachable")
                    break

                # collect list of properties urls on page
                property_urls = [p.find_element(By.TAG_NAME, "a").get_attribute("href") for p in property]


                


                # scrape each properties in different browsing sessions
                for p in property:
                    time.sleep(2)
                    try:

                        properties = scrape_urls(p, properties, code, town, Transaction_type)
                        print(f"Scraped {len(properties)}")
                    except:
                        print("P elements not scrapped")
                        continue
                if verbose:
                    print(f"Scraped {len(properties)} properties.")
                driver.close()

    return pd.DataFrame(properties).reset_index(), len(properties)


# collect data and output csv file
df, quantity = get_data()
df.to_csv("data/zoopla_batch9.csv")
logging.info("Success! zoopla scraped data created with %d properties" % quantity)
end = time.time()
logging.info("Zoopla batch9 scrapping runtime: %d seconds" % (end-start))
