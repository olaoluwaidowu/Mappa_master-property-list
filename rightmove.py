import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode
import pandas as pd




def get_data(num_properties = 20,verbose=True):
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape rightmove
    url = "https://www.rightmove.co.uk/"



    properties = []
    
        #time.sleep(10)
    for code in postcode:
        while len(properties) < (num_properties+1):
            driver.get(url)
            print("\nstarting new area")
            search_box = driver.find_element(By.XPATH, '//input[@name="typeAheadInputField"]').send_keys(code)
            submit = driver.find_element(By.XPATH, '//*[@id="HomeDesktopLayout_searchPanel__vTqkA"]/div/div/div/button[1]').click()
            driver.find_element(By.XPATH, '//button[@id="submit"]').click()
            
            while True:

                property = driver.find_elements(By.CLASS_NAME, "propertyCard-wrapper")
                print(len(property))
                prop = driver.find_element(By.XPATH, '//div[@class="l-searchResult is-list"]')
                time.sleep(5)
                #prop_buttons = prop.find_elements(By.CLASS_NAME)
                print("success")
                #print(address)
                for p in property:

                    try:
                        print("success 6")
                        # get location, price and description
                        time.sleep(10)
                        location = p.find_element(By.CLASS_NAME, "propertyCard-address")


                        
                        print("success 7")
                        price = p.find_element(By.CLASS_NAME, "propertyCard-priceValue").text
                        desc = p.find_element(By.CLASS_NAME, "propertyCard-description").text
                        agent = p.find_element(By.CLASS_NAME, "propertyCard-branchSummary").text
                        #propertyCard-branchSummary property-card-updates
                        a = p.find_element(By.TAG_NAME, "a")
                        listing_url = a.get_attribute("href")

                        print(agent)
                        print(listing_url)
                            

                        # get type, bedroom and toilet of property
                            
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

                        properties.append({"Type" : type,
                        "Description" : desc,
                        "Bedroom" : bedroom,
                        "Toilet" : toilet,
                        "Agent" : agent,
                        "Listing_url" : listing_url,
                        "Price" : price})
                        print(f"Scraped {len(properties)} properties.")
                    except NoSuchElementException:
                        print("Failed to scrape property information.")
                if len(properties) > 49:
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

