import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from district import postcode


def get_data(num_properties = 1500):
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
            prop = driver.find_element(By.XPATH, '//div[@class="l-searchResult is-list"]')
            time.sleep(5)
            #prop_buttons = prop.find_elements(By.CLASS_NAME)
            print("success")
            #print(address)
            for p in property:
                location = p.find_element(By.CLASS_NAME, "propertyCard-address").text
                price = p.find_element(By.CLASS_NAME, "propertyCard-priceValue").text
                desc = p.find_element(By.CLASS_NAME, "propertyCard-description").text
                print(desc)
                time.sleep(3)
            
            #time.sleep(10)
            
        break


get_data()