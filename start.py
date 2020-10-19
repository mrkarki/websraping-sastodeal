import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

list_data=[]

f=open("ne1.csv",'w', encoding='utf-8')
headers="Name, Regular Price, Sale Price\n"
f.write(headers)

for x in range(1,4):
    URL = 'https://www.sastodeal.com/electronic/televisions.html?p='
    page = requests.get(URL+str(x))
    soup = BeautifulSoup(page.content, 'html.parser')

    #job_elems = soup.find_all('div', {"class": "copyright"})
    #newelem = job_elems.find_all('div', class_='lzd-logo-content')
    contents=soup.find_all('li',class_='product')
    bread=soup.find('div',class_='breadcrumbs')
    bread_li=bread.find_all('li')
    bread_len=len(bread_li)
    if bread_len>1:
        bread_len=bread_len-1
    else:
        bread_len=bread_len
    cat_name=bread_li[bread_len].get_text().strip()
    filename=cat_name+'.csv'
    

    for content in contents:
        title_name=content.find_all('strong',class_='name')
        full_name=title_name[0].a.get_text().strip()

        price_wrap_regular=content.find('span',class_="old-price")        
        price_regular=price_wrap_regular.find('span',class_='price').get_text()
        
        price_wrap_sale=content.find('span',class_="special-price")
        price_sale=price_wrap_sale.find('span',class_='price').get_text()

        price_regular=price_regular.replace('रू', '')
        price_regular=price_regular.replace(',', '')

        price_sale=price_sale.replace('रू', '')
        price_sale=price_sale.replace(',', '')
        # print(price_sale)
        print(price_regular)
        list_dictonary={
            "title":full_name,
            "price_regular":price_regular,
            "price_sale":price_sale,
        }
        list_data.append(list_dictonary)
    
        f.write(full_name+ ',' +price_regular+ ',' +price_sale + '\n')
    time.sleep(5)
f.close()
print(list_data)
df=pd.DataFrame(list_data)
print(df.head())
df.to_csv('hello.csv')