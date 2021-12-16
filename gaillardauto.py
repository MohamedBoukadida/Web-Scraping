import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import time
import os
import pandas as pd
import csv
start_time = time.time()


list_pages=[]
list_auxiliaire_2=[]
car_km=[]
ad_price=  []
ad_title=[]
page_num=1
car_options=[]
car_power=[]
car_energy=[]
car_transmission=[]
car_color=[]
list_auxiliaire_3=[]
car_brand=[]
links=[]

result = requests.get (f"https://www.gaillardauto.com/voiture/",stream = True)
src = result.content
soup = BeautifulSoup(src,"lxml")
number_page_soup = soup.find_all("ul", {"class": "page-numbers"})
for i in range(len(number_page_soup)):
        list_pages.append(number_page_soup[i].text.split())
last_page = list_pages[0][len(list_pages[0]) - 2]



while (page_num <= int(last_page)) :
    links_first_version=[]
    list_auxiliaire_1=[]
    result = requests.get (f"https://www.gaillardauto.com/voiture/page/{page_num}/",stream = True)
    src = result.content
    soup = BeautifulSoup(src,"lxml")
    link_soup = soup.find_all("div", {"class":"item_offre clearfix"})
    for i in range(len(link_soup)) :
        links.append(link_soup[i].find("a").attrs['href'])
        links_first_version.append(link_soup[i].find("a").attrs['href'])
    data_soup = soup.find_all("div", {"class": "up"})
    for i in range(len(data_soup)):
        list_auxiliaire_1.append(data_soup[i].text.split("\n"))
    del list_auxiliaire_1[len(list_auxiliaire_1) - 1]
    for x in list_auxiliaire_1:
        list_auxiliaire_2.append(x[1])
        ad_title.append(x[1])
        ad_price.append(x[2][:len(x[2])-1])
        car_km.append(x[4])
        car_power.append(x[6])
        car_energy.append(x[7])
        car_transmission.append(x[8])
        car_color.append(x[9])

    for i in range(len(list_auxiliaire_2)):
        list_auxiliaire_3.append(list_auxiliaire_2[i].split(' '))
    for j in range(len(list_auxiliaire_3)):
        car_brand.append(list_auxiliaire_3[j][0])

    list_auxiliaire_2=[]
    list_auxiliaire_3=[]
    for link in links_first_version :
        list_auxiliaire_4=[]
        result = requests.get(link,stream=True)
        src = result.content
        soup = BeautifulSoup(src,"lxml")
        car_options_soup = soup.find_all("div", {"class": "l-6 option"})
        for i in range(len(car_options_soup)):
            list_auxiliaire_4.append(car_options_soup[i].text)
        car_options.append(list_auxiliaire_4)
    print("page switched", page_num)
    page_num += 1



data= {'ad_title': ad_title,
       'car_brand': car_brand,
         'ad_price' :  ad_price,
         'car_km' :  car_km,
          'car_color':  car_color,
          'car_transmission' : car_transmission,
          'links' : links,
          'car_options': car_options}



df = pd.DataFrame(data, columns = ['ad_title','car_brand' ,'ad_price' ,'car_km'  ,'car_color','car_transmission','links','car_options'])
df.to_csv('data_gaillairdauto.csv',sep=';',encoding="utf-8-sig" ,index=False)


print("Le temps d'exécution totale :--- %s seconds ---" % (time.time() - start_time))