import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode, borough
import pandas as pd
from datetime import date

logging.basicConfig(filename='./logs/otm.log', filemode='a', format='%(levelname)s - %(asctime)s - %(message)s',level=logging.INFO)

start = time.time()


def get_data(verbose=True):
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape rightmove
    url = "https://www.onthemarket.com/"



    properties = []
    
    for code, town in zip(postcode, borough):
            
        print("\nstarting new area")
        
        for i in range(2):

                try:
                    #driver.implicitly_wait(20)
                    driver.get(url)
                    print("\nstarting new property type")
                    
                    time.sleep(3)
                    if i == 0:
                        Transaction_type = "Sale"
                        driver.find_element(By.XPATH, '//button[@id="headlessui-tabs-tab-1"]').click()
                        
                        search_box = driver.find_element(By.XPATH, '//input[@class="landing-search-input landing-search-input--with-btn"]').send_keys(code)
                        time.sleep(2)
                        driver.find_element(By.XPATH, '//*[@id="search-location-sale-btn"]').click()
                    elif i == 1:
                        Transaction_type = "Rent"
                        driver.find_element(By.XPATH, '//button[@id="headlessui-tabs-tab-2"]').click()
                        
                        search_box = driver.find_element(By.XPATH, '//input[@class="landing-search-input landing-search-input--with-btn"]').send_keys(code)
                        time.sleep(2)
                        driver.find_element(By.XPATH, '//*[@id="headlessui-tabs-panel-6"]/div[1]/div/div/button').click()
                        
                    
                    
                    
                    time.sleep(3)
                    
                    while True:
                        currenturl = driver.current_url
                        #img_check = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "img")))
                        #property =  WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "otm-PropertyCard")))
                        property = driver.find_elements(By.CLASS_NAME, "otm-PropertyCard")
                        print(len(property))
                        
                        time.sleep(2)
                        
                        print("success")
                        #driver.find_element(By.XPATH, '//*[@id="pagination-controls"]/div/a[2]/button').click()
                        #time.sleep(10)
                        for p in property:

                            
                            # get property details
                            
                            location = p.find_element(By.CLASS_NAME, 'address').text
                            price = p.find_element(By.CLASS_NAME, "otm-Price").text
                            property_type = p.find_element(By.CLASS_NAME, 'title').text
                            result_id = p.find_element(By.TAG_NAME, "div")
                            result_id = result_id.get_attribute("id")
                            
                            try:
                                bedroom = p.find_element(By.XPATH, f'//*[@id="{result_id}"]/div[2]/div[4]/div[1]').text
                            except:
                                bedroom = None

                            try:
                                bathroom = p.find_element(By.XPATH, f'//*[@id="{result_id}"]/div[2]/div[4]/div[2]').text
                            except:
                                bathroom = None

                            try:
                                agent_logo = p.find_element(By.XPATH, f'//*[@id="{result_id}"]/div[3]/div[1]/div[1]/a/div/img')
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
                            print(currenturl)
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

                            logging.info(f"Scraped {len(properties)} properties.")
                            
                            
                            """if len(properties) > 10:
                                return pd.DataFrame(properties).reset_index(), len(properties)"""

                            if verbose:
                                print(f"Scraped {len(properties)} properties.")
                        print("Expecting a click")
                        next_button = driver.find_element(By.XPATH, '//a[@title="Next page"]')
                        if not next_button.is_enabled():
                            print("No more pages available.")
                            break
                        try:
                            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Next page"]'))).click()
                        except ElementClickInterceptedException:
                            driver.find_element(By.XPATH, '//*[@id="cookie-notification"]/div/div[2]/button').click()
                            time.sleep(2)
                            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Next page"]'))).click()

                        except ElementClickInterceptedException:
                            driver.find_element(By.XPATH,'//*[@class="w-7 flex-shrink-0 h-8"]').click()
                            time.sleep(2)
                            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Next page"]'))).click()


                        #next_button.click()
                        print("next_page clicked")
                        time.sleep(5)
                except Exception as error:
                    logging.warning(f"Exception: {error}")
                    logging.info(f"Property in url:{url}, not scraped")
                
                
    return pd.DataFrame(properties).reset_index(), len(properties)
        
df, quantity = get_data()
df.to_csv("data/onthemarket.csv")
logging.info("Success! onthemarket scraped data created with %d properties" % quantity)
end = time.time()
logging.info("onthemarket scrapping runtime: %d seconds" % (end-start))

