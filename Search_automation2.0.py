from selenium import webdriver
import time
import pandas as pd
import numpy as np
import random as r
import requests
from flask import request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#Setting up browser
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("start-maximized")
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/Users/lizavetaradzevich/Downloads/chromedriver', options=options)

#Importing zip_code_df
#zip_code_df = pd.read_csv("ZIP-COUNTY-FIPS_2018-03.csv",
#                            converters={"ZIP": str,
#                                        "STCOUNTYFP": str})

#zip_code_filter = zip_code_df[zip_code_df['STATE'] == 'NM']
#zip_code_lst = zip_code_filter['ZIP'].tolist()
zip_code_lst = ['94107', '94109', '02215', '94088', '95050']
print(zip_code_lst)

url_lst = []

#defifning
def url_crawler(zip):

    driver.get("https://www.whistleout.com/Internet")
    time.sleep(r.randint(10,12))
    enter_address = driver.find_element_by_xpath('//*[@id="enterAddressLocationInput-1"]')

    #print("Element is visible? " + str(enter_address.is_displayed()))
    time.sleep(r.randint(2,4))

    enter_address.click()
    time.sleep(r.randint(2,4))
    enter_address.send_keys(zip)

    time.sleep(r.randint(4,6))
    search = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div[2]/button')
    search.click()

    WebDriverWait(driver, 10).until(EC.url_contains("www.whistleout.com/Internet/Search?"))
    currentURL = driver.current_url

    url = requests.get(str(currentURL))
    soup = BeautifulSoup(url.content, 'html.parser')

    location = soup.find_all('h5', class_ = 'mar-t-0 pad-b-5 bor-b-1 font-feature font-700 font-8 font-7-xs')
    location_text = ""
    for line in location:
        line = str(line)
        location_text = location_text + line
    location_text = location_text[119:-9]

    zip_code = str(currentURL)[-5:]
    state_code = str(currentURL)[-8:-6]

    return([location_text, currentURL,zip_code, state_code])

for index, zip in enumerate(zip_code_lst[3:]):
    print(index, ': ', zip)
    full_url = url_crawler(zip)
    url_lst.append(full_url)


url_df = pd.DataFrame(url_lst, columns=['wo_region', 'url', 'zip_code', 'state_code'])
pd.set_option('display.max_columns', None)
print(url_df)

url_df.drop_duplicates(subset ="wo_region", keep = "first", inplace = True)
index_names = url_df[url_df['state_code'] == 'ab'].index
url_df.drop(index_names, inplace = True)


#print(url_df)

url_df.to_csv('url_test_df.csv', mode='a', header=False)

#url_df.to_csv('url_test_df.csv')
driver.quit()

print(url_df)
