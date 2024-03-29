import requests
import pandas as pd 
from bs4 import BeautifulSoup
import re
import pymongo


def read_news( headers, a):
    scarped_data=[]
    url_2 = "https://newspaper.hamshahrionline.ir/?n="

    for p in a:
        print(p)
        url = 'https://newspaper.hamshahrionline.ir'+ p
        response_2 = requests.request("GET",url=url,headers=headers)
        data_2 = BeautifulSoup(response_2.text,'html.parser')
        news_month_id = data_2.find_all('span',attrs={'class','subtitle'})
        for item in news_month_id:
            number= item.text.split()
            print(number[-1])
            url = url_2 + number[-1]
            response_3 = requests.request("GET",url=url,headers=headers)
            data_3 = BeautifulSoup(response_3.text,'html.parser')
            news_data = data_3.find_all('div',attrs={'class','text'})
            date = data_3.find_all('li',attrs={'class','dir-left'})
            for news in news_data:
                news_detail={}
                #print (news)
                news_detail['news_text']=news.text.encode('utf-8')
                for d in date:
                    news_detail['news_date'] = d.text
                scarped_data.append(news_detail)

    return scarped_data


def read_archive():
    url = 'https://newspaper.hamshahrionline.ir/archive'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    a = []
    response_1= requests.request("GET",url=url,headers=headers)
    data_1 = BeautifulSoup(response_1.text,'html.parser')
    for link in data_1.findAll('a', attrs={'href': re.compile("^/archive")}):
        a.append(link.get('href'))
        news_month_id=[]
    return headers,a




headers, a = read_archive()
scarped_data = read_news(headers, a)

dataframe=pd.DataFrame.from_dict(scarped_data)
dataframe.to_csv('news_data_2.csv',index=False)

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

database = client["news"]
people_collection = database[ "hamshahri" ]
result=people_collection.insert_many(scarped_data)
