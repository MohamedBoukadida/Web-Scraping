import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import time
import pandas as pd
import os
import re
import unicodedata

start_time = time.time()

links = []
car_brand = []
car_color = []
car_power = []
car_nb_seats = []
car_options = []
car_nb_doors = []
ad_title = []
car_km = []
ad_prices = []
car_energy = []
car_transmission = []
page_num = 2
links_first_version = []
ad_prices1=[]

number = 11
while (number <= 20):
    links_first_version=[]
    result = requests.get(f"https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page={number}",
                          stream=True)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    link_soup = soup.find_all("div", {"class": "searchCard"})
    for i in range(len(link_soup)):
        links_first_version.append(link_soup[i].find("a").attrs['href'])
        links.append(link_soup[i].find("a").attrs['href'])


    ad_title_soup = soup.find_all("span", {"class": "searchCard__makeModel"})
    for i in range(len(ad_title_soup)):
        ad_title.append(ad_title_soup[i].text)

    for i in range(len(ad_title_soup)):
        car_brand.append(ad_title_soup[i].text.split(' ')[0])

    ad_prices_soup = soup.find_all("div", {"class": "searchCard__fieldPrice"})
    for i in range(len(ad_prices_soup)):
        cleaned_string=''
        cleaned_string=(ad_prices_soup[i].text).replace(u'\xa0',u' ')
        ad_prices.append(cleaned_string[0:len(cleaned_string)-2])


    for link in links_first_version:

            in_link_list = []
            in_link_list_sliced = []
            in_link_list_cleaned = []
            result = requests.get("https://www.lacentrale.fr" + link, stream=True)
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            in_link_soup = soup.find_all("div", "cbm-moduleInfos__informationList")
            for i in range(len(in_link_soup)):
                in_link_list.append(in_link_soup[i].text.split(':'))

            cleaning_soup = soup.find_all("span", "optionLabel")
            for i in range(len(cleaning_soup)):
                in_link_list_cleaned.append(cleaning_soup[i].text.split(':'))


            in_link_list_sliced = in_link_list[0]
            list_find = []
            list_auxiliaire = []
            for i in range(len(in_link_list_cleaned)):
                list_find.append(in_link_list_sliced[i].find(in_link_list_cleaned[i][0]))

            car_km.append(in_link_list_sliced[4][0:list_find[4]])
            car_energy.append(in_link_list_sliced[5][0:list_find[5]])
            car_transmission_cleaning = in_link_list_sliced[6][0:list_find[6]]
            if car_transmission_cleaning[1]=='m'  :
                car_transmission.append('Manuelle')
            elif car_transmission_cleaning[1] == 'a':
                car_transmission.append('Automatique')
            else :
                car_transmission.append(' ')
            #car_transmission.append(in_link_list_sliced[6][0:list_find[6]])
            car_color_cleaning=in_link_list_sliced[7][0:list_find[7]]
            if (car_color_cleaning[1]=='I') or (car_color_cleaning[1]=='o') :
                car_color.append(' ')
            elif not(car_color_cleaning[1].isdigit()) :
                car_color.append(car_color_cleaning)
            else :
                car_color.append(' ')
            # car_nb_seats.append(in_link_list_sliced[10][0:2])
            nb_doors_cleaning=in_link_list_sliced[9][0:2]

            if not(nb_doors_cleaning[1].isdigit()) :
                car_nb_doors.append(' ')
            else :
                car_nb_doors.append(nb_doors_cleaning)
            # car_power.append(in_link_list_sliced[15][0:3])
            car_options_soup = soup.find_all("li", {"class": "list-item"})
            for i in range(len(car_options_soup)):
                list_auxiliaire.append(car_options_soup[i].text)
            car_options.append(list_auxiliaire)
    number = number + 1
    print("page switched", number)




data= {'ad_title': ad_title,
       'car_brand': car_brand,
         'ad_prices' :  ad_prices,
         'car_km' :  car_km,
         'car_nb_doors' :  car_nb_doors,
          'car_color':  car_color,
          'car_transmission' : car_transmission,
          'links' : links,
            'car_options' : car_options}

df = pd.DataFrame(data, columns = ['ad_title','car_brand' ,'ad_prices' ,'car_km' ,'car_nb_doors' ,'car_color','car_transmission','links','car_options'])
df.to_csv('lacentrale.csv',sep=';',encoding="utf-8-sig"  ,index=False)


print("Le temps d'exécution totale :--- %s seconds ---" % (time.time() - start_time))
