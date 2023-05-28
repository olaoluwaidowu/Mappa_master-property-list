import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode
import pandas as pd


def get_data(num_properties = 20):
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape rightmove
    url = "https://www.rightmove.co.uk/"



    properties = []
    while len(properties) < (num_properties+1):
        #time.sleep(10)
        for code in postcode:
            driver.get(url)
            print("\nstarting new area")
            search_box = driver.find_element(By.XPATH, '//input[@name="typeAheadInputField"]').send_keys(code)
            submit = driver.find_element(By.XPATH, '//*[@id="HomeDesktopLayout_searchPanel__vTqkA"]/div/div/div/button[1]').click()
            driver.find_element(By.XPATH, '//button[@id="submit"]').click()
            property = driver.find_elements(By.CLASS_NAME, "propertyCard-wrapper")
            print(property)
            prop = driver.find_element(By.XPATH, '//div[@class="l-searchResult is-list"]')
            time.sleep(5)
            #prop_buttons = prop.find_elements(By.CLASS_NAME)
            print("success")
            #print(address)
            for p in property:
                print(p)
                print("success 6")
                 # get location, price and description
                time.sleep(10)
                failed = True
                """ while failed:
                    try:
                        time.sleep(10)
                        location = p.find_element(By.CLASS_NAME, "propertyCard-address").text
                        print("success 7")
                        price = p.find_element(By.CLASS_NAME, "propertyCard-priceValue").text
                        desc = p.find_element(By.CLASS_NAME, "propertyCard-description").text
                    

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
                        # get other info by click on property link
                        p.find_element(By.CLASS_NAME, "propertyCard-address").click()
                        failed = False
                        print("passed")
                    except:
                        time.sleep(10)"""

                time.sleep(10)
                # location = p.find_element(By.CLASS_NAME, "propertyCard-address").text
                
                
                print("success 7")
                price = p.find_element(By.CLASS_NAME, "propertyCard-priceValue").text
                desc = p.find_element(By.CLASS_NAME, "propertyCard-description").text
                    

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
                # get other info by click on property link
                p.find_element(By.CLASS_NAME, "propertyCard-address").click()


                time.sleep(10)
                try:
                    agent = driver.find_element(By.XPATH,'//*[@id="root"]/main/div/div[2]/div/article[4]/div[1]/div/h3').text
                except NoSuchElementException:
                    agent = "NOT FOUND"
                #try:
                #    location = driver.find_element(By.XPATH,'//*[@id="root"]/main/div/div[2]/div/div[1]/div[1]/div/h1').text
                #except NoSuchElementException:
                #    location = "NOT FOUND"
                listing_url = driver.current_url
                
                print("success 3")
                driver.back()
                print("success 4")
                time.sleep(3)

                properties.append({"Type" : type,
                "Description" : desc,
                "Bedroom" : bedroom,
                "Toilet" : toilet,
                "Agent" : agent,
                "Listing_url" : listing_url,
                "Price" : price})
                #print(properties)
                
# 
                    
    print(pd.DataFrame(properties).reset_index())
                

# 
                
                
                #print(len(information))
                
            
            #time.sleep(10)
            
# "Address" : location,

get_data()