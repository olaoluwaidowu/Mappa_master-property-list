import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode
import pandas as pd





def get_data(num_properties=20):
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape rightmove
    url = "https://www.rightmove.co.uk/"

    properties = []

    for code in postcode:
        print("\nStarting new area")
        driver.get(url)
        
        try:
            search_box = driver.find_element(By.NAME, "typeAheadInputField")
            search_box.send_keys(code)
            submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
            submit.click()
            time.sleep(5)
            driver.find_element(By.XPATH, '//button[text()="Accept all"]').click()
            time.sleep(5)
            
            while len(properties) < num_properties:
                property_cards = driver.find_elements(By.CLASS_NAME, "propertyCard-wrapper")

                for card in property_cards:
                    try:
                        card_link = card.find_element(By.CLASS_NAME, "propertyCard-link")
                        card_link.click()
                        time.sleep(3)
                        
                        location = driver.find_element(By.CLASS_NAME, "property-header-bedroom-and-price").text
                        price = driver.find_element(By.CLASS_NAME, "property-header-price").text
                        desc = driver.find_element(By.CLASS_NAME, "property-header-title").text

                        # get type, bedroom and toilet of property
                        information = driver.find_elements(By.CLASS_NAME, "dp-features__feature")
                        if len(information) == 1:
                            property_type, bedrooms, toilets = "NA", "NA", "NA"
                        elif len(information) == 2:
                            property_type = information[0].text
                            bedrooms, toilets = information[1].text.split(", ")
                        else:
                            property_type, bedrooms, toilets = [info.text for info in information]

                        agent = driver.find_element(By.CLASS_NAME, "ui-agent__name").text
                        listing_url = driver.current_url

                        properties.append({
                            "Type": property_type,
                            "Description": desc,
                            "Bedroom": bedrooms,
                            "Toilet": toilets,
                            "Agent": agent,
                            "Listing_url": listing_url,
                            "Price": price,
                            "Location": location
                        })
                        
                        print(f"Scraped {len(properties)} properties.")
                    except NoSuchElementException:
                        print("Failed to scrape property information.")
                        
                    driver.back()
                    time.sleep(2)

                next_button = driver.find_element(By.XPATH, '//a[@data-bind="click: getNextPage"]')
                if not next_button.is_enabled():
                    print("No more pages available.")
                    break
                next_button.click()
                time.sleep(5)
                
        except Exception as e:
            print(f"Failed to scrape properties for {code}. Error: {str(e)}")

    driver.quit()
    return properties

get_data()
