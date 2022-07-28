from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import chromedriver_binary
import pandas as pd
import requests 
from selenium.webdriver.common.by import By

startURL = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('chromedriver_win32\chromedriver.exe')
browser.get(startURL)
time.sleep(10)
plants_data = []
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]

def scrape():
   
    for i in range(1,5):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            curret_page_num = int(soup.find_all('input',attrs={'class','page_num'})[0].get('value'))
            if curret_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif curret_page_num> i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else: break
        for ul_tag in soup.find_all('ul',attrs = {'class','exoplanet'}):
            li_tags = ul_tag.find_all("li") 
            templist = []
            for index,li_tag in enumerate(li_tags): 
                if index == 0:
                    templist.append(li_tag.find_all('a')[0].contents[0])
                else:
                    try:
                        templist.append(li_tag.contents[0])
                    except:
                        templist.append('')
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planets_data.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f'page{i} scraping completed')

scrape()
new_planets_data=[]

def scrape_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content,'html.parser')
    temp_list = []
    for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}): 
        td_tags = tr_tag.find_all("td")
        for td_tag in td_tags:
            (temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]))
    new_planets_data.append(temp_list)

for index,data in enumerate(planets_data):
    scrape_more_data(data[5])
    print(f'scraping at hyperlink {index+1} is completed')
            
with open('final.csv','w')as f:
    csvwritter = csv.writer(f)
    csvwritter.writerow(headers)
    csvwritter.writerows(planetData)
