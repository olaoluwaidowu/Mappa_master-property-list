import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode
import pandas as pd




def get_data(num_properties = 500,verbose=True):
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape rightmove
    url = "https://www.rightmove.co.uk/"



    properties = []
    
    for code in postcode:
        while len(properties) < (num_properties+1):
            
            print("\nstarting new area")
            
            for i in range(2):
                driver.get(url)
                print("\nstarting new property type")
                search_box = driver.find_element(By.XPATH, '//input[@name="typeAheadInputField"]').send_keys(code)
                time.sleep(3)
                if i == 0:
                    Transaction_type = "Sale"
                    driver.find_element(By.XPATH, '//*[@id="HomeDesktopLayout_searchPanel__vTqkA"]/div/div/div/button[1]').click()
                elif i == 1:
                    Transaction_type = "Rent"
                    driver.find_element(By.XPATH, '//*[@id="HomeDesktopLayout_searchPanel__vTqkA"]/div/div/div/button[2]').click()
            
                driver.find_element(By.XPATH, '//button[@id="submit"]').click()
                
                while True:

                    property = driver.find_elements(By.CLASS_NAME, "propertyCard-wrapper")
                    print(len(property))
                    #prop = driver.find_element(By.XPATH, '//div[@class="l-searchResult is-list"]')
                    time.sleep(5)
                    #prop_buttons = prop.find_elements(By.CLASS_NAME)
                    print("success")
                    #print(address)
                    for p in property:

                        try:
                            # get property details
                            time.sleep(5)
                            location = p.find_element(By.CLASS_NAME, "propertyCard-address").text
                            price = p.find_element(By.CLASS_NAME, "propertyCard-priceValue").text
                            desc = p.find_element(By.CLASS_NAME, "propertyCard-description").text
                            agent = p.find_element(By.CLASS_NAME, "propertyCard-branchSummary").text
                            
                            a = p.find_element(By.TAG_NAME, "a")
                            listing_url = a.get_attribute("href")

                            information = p.find_element(By.CLASS_NAME, "property-information").text

                            information = information.split("\n")
                            type = information[0]
                            if len(information) < 2:
                                bedroom = toilet = "NA"
                            elif len(information) < 3:
                                bedroom = information[1]
                                toilet = "NA"
                            else:
                                bedroom = information[1]
                                toilet = information[2]
                            
                                

                            print(f"length of info {len(information)}")

                            properties.append({"Transaction_type" : Transaction_type,
                            "Bedroom" : bedroom,
                            "Bathrooms" : toilet,
                            "Description" : desc,
                            "Property_type" : type,
                            "Price" : price,
                            "Location" : location,
                            "Agent" : agent,
                            "Listing_url" : listing_url})

                            print(f"Scraped {len(properties)} properties.")
                        except NoSuchElementException:
                            print("Failed to scrape property information.")
                        #if len(properties) > 10:
                            #break
                    if len(properties) > 500:
                        break

                    if verbose:
                        print(f"Scraped {len(properties)} properties.")
                    next_button = driver.find_element(By.XPATH, '//button[@class="pagination-button pagination-direction pagination-direction--next"]')
                    if not next_button.is_enabled():
                        print("No more pages available.")
                        break
                    next_button.click()
                    time.sleep(5)
    return pd.DataFrame(properties).reset_index()
        
df = get_data()
df.to_csv("data/rightmove.csv")

