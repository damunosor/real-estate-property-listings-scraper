import requests
from bs4 import BeautifulSoup
import pandas as pd

l=list()
obj={}

# Web scraping
target_url = 'https://www.zillow.com/new-york-ny/'

headers =   {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'upgrade-insecure-requests':'1',
    }

for page in range(1,1000):
    resp = requests.get(target_url, headers=headers).text

    soup = BeautifulSoup(resp,'html.parser')

    properties = soup.find_all('div',{'class':'StyledPropertyCardDataWrapper-c11n-8-84-3__sc-1omp4c3-0 bKpguY property-card-data'})

    for x in range(0,len(properties)):
            try:
                obj['price']=properties[x].find('div',{'class':'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 fDSTNn'}).text
            except:
                obj['price']=None
            try:
                obj['size']=properties[x].find('div',{'class':'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 dbDWjx'}).text
              
            except:
                obj['size']=None
            try:
                obj['address']=properties[x].find('a',{'class':'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link'}).text
            except:
                obj['address']=None
            try:
                obj['url']=properties[x].find("a")["href"]
            except:
                obj['url']=None
            try:
                obj['listing']=properties[x].find('div',{'class':'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jretvB'}).text
            except:
                obj['listing']=None
                    
            l.append(obj)
            obj={}
                   
print(l)

#Data Wrangling 
df = pd.DataFrame(l)
df[['size', 'property_type']] = df['size'].str.split(' - ', 1, expand=True)
df[['address', 'city','code']] = df['address'].str.split(',', 2, expand=True)
df[['size', 'area']] = df['size'].str.split('a', 1, expand=True)
df['size']=df['size'].str[:-1]
df[['bedrooms', 'bathrooms']] = df['size'].str.split(' ', 1, expand=True)
df['bathrooms'] = df['bathrooms'].replace('bds', '', regex=True)
df['bathrooms'] = df['bathrooms'].replace('bd', '', regex=True)
df[['listing', 'agency']] = df['listing'].str.split(': ', 1, expand=True)
df = df.drop('size', axis=1)
df = df.drop('listing', axis=1)
df= df[['property_type','price','address', 'city','code','area','bedrooms', 'bathrooms','url','agency']]

#Save dataframe
df.to_csv('Zillow_New_York_OK.csv', index = True)
