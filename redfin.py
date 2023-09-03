#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 16:17:14 2023

@author: Daniela Munoz
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.redfin.com/city/30749/NY/New-York'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'}

soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

beds1 = []
baths1=[]
sqm1=[]
address1 = []
city1=[]
state1=[]
code1=[]
price1=[]
link1 = []


for stats, link, price in zip(soup.select('.HomeStatsV2'),
                              soup.select('.bottomV2 > a'),
                              soup.select('.homecardV2Price')):

    beds, baths, sqm = map(lambda t: t.get_text(strip=True), stats.select('div'))
    address, city, code = link.text.split(',')
    state, code = code.split()
    price = price.text
    link = 'https://www.redfin.com' + link['href']
    
    beds1.append(beds)
    baths1.append(baths)
    sqm1.append(sqm)
    address1.append(address)
    city1.append(city)
    state1.append(state)
    code1.append(code)
    price1.append(price)
    link1.append(link)
    
results_df = pd.DataFrame()
results_df['beds'] = beds1 
results_df['baths'] = baths1 
results_df['sqm'] = sqm1 
results_df['address'] = address1
results_df['city'] = city1
results_df['state'] = state1
results_df['code'] = code1
results_df['price'] = price1
results_df['link'] = link1
