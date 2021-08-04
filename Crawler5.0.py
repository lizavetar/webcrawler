#Import Statements
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import itertools
from selenium import webdriver
import time
import lxml

#Some weird shit
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

url_df = pd.read_csv("url_DE_df.csv")
url_lst = url_df['url'].tolist()


#Setting up browser
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='C:/Users/dtc107809/Detecon Consulting/Jungle Client Service Team - Documents/Kuiper/Architecture/chromedriver.exe', options=options)


def crawler(url):
    #Looking and activating "Load More" buttons and activating them
    driver.get(url)

    #//button[@data-load-tab='fixed'][@class='btn btn-primary btn-lg btn-block-xs']
    while True:
        try:
            loadMoreButton = driver.find_element_by_xpath('//*[@id="fixed"]/div[2]/div/button')
            time.sleep(2)
            loadMoreButton.click()
            time.sleep(5)
        except Exception as e:
            print(e)
            break
    page_source = driver.page_source
    #print("Complete")
    #print(page_source)



    #C:\Users\dtc107809\Detecon Consulting\Jungle Client Service Team - Documents\Kuiper\Architecture

    #Retriving results from the tabpanel
    #test_html = requests.get(page_source)
    #soup = BeautifulSoup(test_html.content, 'html.parser')

    soup = BeautifulSoup(page_source, 'lxml')
    results = soup.find(class_ = "tab-pane pad-0 bor-0 active", id = ["fixed", "all"])
    #print(results)

    #Slicing results into separate rows of the table
    chunks = results.find_all(class_ = "results-item row pad-y-4 sep-b-1 bor-a-8-xs bg-white-xs mar-y-6-xs bor-b-1 rounded-3 position-relative")
    #Getting info from each of the columns

    #Plan names
    plan_name_lst = []
    for item in chunks:
        plan_name_html = item.find_all('h2', class_ = "font-6 font-800 font-feature pad-t-2 mar-0 line-height-12")
        plan_name_text = ""
        for line in plan_name_html:
            line = str(line)
            plan_name_text = plan_name_text + line
        plan_name_text = plan_name_text[87:-18]
        plan_name_lst.append(plan_name_text)
    #print(plan_name_lst)

    #Provider names
    #Note: need to strip OR resplace fuction for beautifying
    provider_lst_lst = []
    provider_lst = []
    for item in chunks:
        provider_html = item.find_all('img', class_ = ['brand-equalizer mar-l-4 mar-r-1 mar-b-3 mar-b-0-xs mar-r-0-xs', 'brand-equalizer mar-l-4 mar-r-1 mar-b-3 mar-b-0-xs mar-r-0-xs hover'])
        provider_text = ""
        for line in provider_html:
            line = str(line)
            provider_text = provider_text + line
        provider_text = provider_text[9:].split(" ", 1)
        provider_lst_lst.append(provider_text[:-1])
        provider_lst = [item for sublist in provider_lst_lst for item in sublist]
    #print(provider_lst)

    #Speed data
    speed_lst = []
    for item in chunks:
        speed_html = item.find_all('span', class_ = "font-7 font-6-sm font-5-xs display-inline-block")
        speed_text = ""
        for line in speed_html:
            line = str(line)
            speed_text = speed_text + line
        speed_text = speed_text[62:-7]
        speed_lst.append(speed_text)
    #print(speed_lst)

    #Data Limits (in GB)
    data_limit_lst = []
    for item in chunks:
        data_limit_html = item.find_all('span', class_ = "font-6 font-5-sm font-5-xs pad-t-1 line-height-12 display-inline-block")
        data_limit_text = ""
        for line in data_limit_html:
            line = str(line)
            data_limit_text = data_limit_text + line
        data_limit_text = data_limit_text[106:-24]
        data_limit_lst.append(data_limit_text)
    #print(data_limit_lst)

    #Pricing (to the nearest dollar)
    price_lst = []
    for item in chunks:
        price_html = item.find_all('span', class_ = "font-9 font-10-xs font-7-sm font-8-md font-feature font-700 line-height-13")
        price_text = ""
        for line in price_html:
            line = str(line)
            price_text = price_text + line
        price_text = price_text[128:130]
        price_lst.append(price_text)
    #print(price_lst)

    #Tech data
    tech_lst_lst = []
    tech_lst = []
    for item in chunks:
        tech_html = item.find_all('span', class_ = "font-2")
        tech_text = ""
        for line in tech_html:
            line = str(line)
            tech_text = tech_text + line
        tech_text = tech_text[41:].split("<", 1)
        tech_lst_lst.append(tech_text[:-1])
        tech_lst = [item for sublist in tech_lst_lst for item in sublist]
    #print(tech_lst)

    #Terms data
    terms_lst = []
    for item in chunks:
        terms_html = item.find_all('span', class_ = "font-2")
        if len(terms_html) >= 3:
            terms_text = str(terms_html[-1])
            terms_text = terms_text[21:-7]
            terms_lst.append(terms_text)
        else:
            terms_lst.append("None")
    #print(terms_lst)

    #Upfront info
    upfront_lst = []
    for item in chunks:
        upfront_html = item.find_all('div', class_ = "font-4 mar-y-2")
        upfront_text = str(upfront_html)
        upfront_text = upfront_text[39:-16]
        upfront_lst.append(upfront_text)
    #print(upfront_lst)


    #Creating dictionary with column names
    US_tarrifs_dict = {'plan_name': plan_name_lst,
                       'provider': provider_lst,
                       'speed': speed_lst,
                       'data_limit': data_limit_lst,
                       'price': price_lst,
                       'tech': tech_lst,
                       'terms': terms_lst,
                       'upfront': upfront_lst,
                       'url': url}

    #Transforming into pandas DF
    US_tarrifs_df = pd.DataFrame(US_tarrifs_dict)

    pd.set_option('display.max_columns', None)
    print(US_tarrifs_df)
    return(US_tarrifs_df)


atlas_tarrif_df = pd.DataFrame({'plan_name': [],
                                'provider': [],
                                'speed': [],
                                'data_limit': [],
                                'price': [],
                                'tech': [],
                                'terms': [],
                                'upfront': [],
                                'url': []})


for url in url_lst:
    crawler_results = crawler(url)
    atlas_tarrif_df = atlas_tarrif_df.append(crawler_results, ignore_index = True)

print(atlas_tarrif_df)

atlas_tarrif_df.to_csv('atlas_tarrif_DE_df.csv')
driver.quit()
#class="results-item row pad-y-4 sep-b-1 bor-a-8-xs bg-white-xs mar-y-6-xs bor-b-1 rounded-3 position-relative"
#class="brand-equalizer mar-l-4 mar-r-1 mar-b-3 mar-b-0-xs mar-r-0-xs"
#class="brand-equalizer mar-l-4 mar-r-1 mar-b-3 mar-b-0-xs mar-r-0-xs hover"
#class="brand-equalizer mar-l-4 mar-r-1 mar-b-3 mar-b-0-xs mar-r-0-xs hover"
#class="font-6 font-800 font-feature pad-t-2 mar-0 line-height-12"
