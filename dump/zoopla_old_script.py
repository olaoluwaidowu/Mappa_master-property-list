from calendar import c
from cmath import nan
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.keys import Keys
import requests
from district import postcode, borough
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


def scrape_urls(url, driver_options, properties, code, town, Transaction_type, fails, connected=True):
    counter = 0
    
    while connected:
        try:
            # Setting the driver path and requesting a page 
            driver = webdriver.Chrome(options=options) 

            # Changing the property of the navigator value for webdriver to undefined 
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


            driver.get(url)

            driver.implicitly_wait(10)
            print("session created")

            

            price = driver.find_element(By.XPATH, '//p[@data-testid="price"]').text
            
            location  = driver.find_element(By.XPATH, '//address[@data-testid="address-label"]').text

            property_type = driver.find_element(By.XPATH, '//div[@data-testid="title-label"]').text
            

            try:
                agent = driver.find_element(By.XPATH, '//p[@class="_164l98j3 _1ftx2fq6"]').text 
            
            except:
                agent = None

            try:
                desc = driver.find_element(By.XPATH, '//div[@class="_1qfzbjk3"]').text
            except:
                desc = None

            


            """try:
                bedroom = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[1]/div[1]/div').text    # _1ljm00u6r _1ljm00u0
            except NoSuchElementException:
                bedroom = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div/div[6]/div[1]/div[1]/div[1]/div').text
                print("bedroom 2.0 success")
            finally:
                bedroom = None"""
            changed = True
            try:
                #time.sleep(3)
                bedroom  = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[1]/div[1]/div').text
                changed = False
                bathroom = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[1]/div[2]/div').text
            except NoSuchElementException:
                if changed == False:
                    logging.warning("bedroom success | bathroom Failed detected! at %s" % url)
                    bedroom, bathroom = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[1]/div[1]/div').text, None
                else:
                    try:
                        bedroom  = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[6]/div[1]/div[1]/div[1]/div').text
                        bathroom = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[6]/div[1]/div[1]/div[2]/div').text
                    except NoSuchElementException:
                        
                        bedroom  = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div/div[6]/div[1]/div[1]/div[1]/div').text
                        bathroom = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div/div[6]/div[1]/div[1]/div[2]/div').text
                        logging.warning("Bedroom path switched at:  %s" % url) 
            except:
                bedroom, bathroom = None, None
                del changed
                logging.warning("Bedroom path switched from all options:  %s" % url) 

            if Transaction_type == "Sale":

                try:
                    
                        
                    tenure = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div/div[6]/div[1]/div[2]/div/div[1]/div[2]').text

                    tax_band = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div/div[6]/div[1]/div[2]/div/div[2]/div[2]').text

                except NoSuchElementException:
                    logging.warning("Tenure section class switched at:  %s" % url)

                    tenure = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[2]/div/div[1]/div[2]').text

                    tax_band = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]').text

                    print(f"No tenure element found for:  {url}")
                except NoSuchElementException:
                    tenure = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[2]/div/div[1]/div[2]').text
                    tax_band = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]').text
                    logging.info("Tax band element found while tenure switched at:  %s" % url)

                except:
                    tenure = None
                    tax_band = None


                print(f"Property tenure : {tenure}     ")
            else:
                try:
                    
                        
                    tenure = "NA"

                    tax_band = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div/div[6]/div[1]/div[2]/div/div[2]/div[2]').text

                except NoSuchElementException:
                    logging.warning("Tax band section switched at:  %s" % url)

                    tenure = "NA"

                    tax_band = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]').text

                    print(f"No tenure element found for:  {url}")
                except NoSuchElementException:
                    tenure = "NA"
                    tax_band = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]').text
                    logging.info("Tax band element found while tenure switched at:  %s" % url)

                except:
                    tenure = "NA"
                    tax_band = None


                


            

            print(price)
            print(location)

            print(f"Tax Band : {tax_band}")





        
            driver.close()
            time.sleep(3)

            properties.append({"Transaction_type" : Transaction_type,
            "Bedroom" : bedroom,
            "Bathrooms" : bathroom,
            "Description" : desc,
            "Property_type" : property_type,
            "Tax_band" : tax_band,
            "Price" : price,
            "Location" : location,
            "Agent" : agent,
            "Listing_url" : url,
            "Borough" : town,
            "Date" : date.today()
            })

            connected = False
                
                

        except WebDriverException:
            counter += 1
            logging.warning(f"Webdriver disconnected after {len(properties)} properties")
            if counter > 3:
                logging.info(f"Webdriver disconnects over 3 times: {url} not scraped")
                return properties
            connected = True
            
        except Exception as error:
            fails += 1
            if fails % 10 == 0:
                logging.critical("Fails more than %d" % fails-1)
            print(f"Property in url:{url}, not found")
            print("Exception: ", error)

    return properties


def get_data(verbose=True):
    #options = Options()
    options.add_argument("start-maximized")
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    # scrape zoopa
    fails = 0
    properties = []

    # scrape by postcode
    for code, town in zip(postcode, borough):
        
        print("\nstarting new postcode")
        
        #  ourter loop to handle transaction type i.e sale or rent
        for i in range(2):
            for j in range(13):   # range to cover number of pages
            
                print("\nstarting new property type")
            
            
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
                        url = f"https://www.zoopla.co.uk/to-rent/property/{code}/?price_frequency=per_month&q={code}&search_source=home&pn={j+1}"

                # Setting the driver path and requesting a page 
                driver = webdriver.Chrome(options=options)

                # Changing the property of the navigator value for webdriver to undefined 
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                # launch browser to specified url
                try:
                    driver.get(url)
                except:
                    break

                time.sleep(4)

                # get webelement of properties on page
                property = driver.find_elements(By.XPATH, '//div[@class="f0xnzq2"]')

                # collect list of properties urls on page
                property_urls = [p.find_element(By.TAG_NAME, "a").get_attribute("href") for p in property]


                driver.close()


                # scrape each properties in different browsing sessions
                for url in property_urls:

                    properties = scrape_urls(url, options, properties, code, town, Transaction_type, fails)

                

    return pd.DataFrame(properties).reset_index(), len(properties)


# collect data and output csv file
df, quantity = get_data()
df.to_csv("data/zoopla.csv")
logging.info("Success! zoopla scraped data created with %d properties" % quantity)
end = time.time()
logging.info("Zoopla scrapping runtime: %d seconds" % (end-start))
