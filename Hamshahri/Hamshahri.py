import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import pymongo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
def get_f_news_id():
    # get the oldest issue number and link
    url = 'https://newspaper.hamshahrionline.ir/archive'
    response = requests.request("GET", url=url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    news_data = data.find_all('li', attrs={'class', 'page-item'})[-2]
    per_date_archive = news_data.find('a').get('href')
    url_per_date_archive = 'https://newspaper.hamshahrionline.ir'+per_date_archive
    response_per_date_archive = requests.request("GET", url=url_per_date_archive, headers=headers)
    data_per_date_archive = BeautifulSoup(response_per_date_archive.text, 'html.parser')
    news_data_per_date_archive = data_per_date_archive.find_all('div', attrs={'class', 'col-md-4'})[-1]
    news_data_per_date_archive = news_data_per_date_archive.find('a').get('href')
    first_news_id= news_data_per_date_archive.replace('/?n=','')
    first_news_id =int(first_news_id)
    return first_news_id

def get_lat_news_id():
    # get the latest issue number and link
    url = 'https://newspaper.hamshahrionline.ir/archive'
    response = requests.request("GET", url=url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    news_link = data.find('div', attrs={'class', 'col-md-4'})
    news_link = news_link.find('a').get('href')
    latest_news_id= news_link.replace('/?n=','')
    latest_news_id = int(latest_news_id)
    return latest_news_id


scarped_data = []

latest_news_id = get_lat_news_id()
first_news_id = get_f_news_id()
while first_news_id < latest_news_id:
    url = 'https://newspaper.hamshahrionline.ir/?n=' + str(first_news_id)
    response = requests.request("GET", url=url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    date = data.find_all('li', attrs={'class', 'dir-left'})
    news_data = data.find_all('div',attrs={'class','post'})
    for news in news_data:
        news_detail = {}
        #news_detail['news_title'] = news.title
        news_detail['news_text'] = news.text        
        for d in date:
            news_detail['news_date'] = d.text
        scarped_data.append(news_detail)
    first_news_id += 1
    print(first_news_id)
dataframe = pd.DataFrame.from_dict(scarped_data)
dataframe.to_csv('hamshahrionline.csv', index=False,encoding="utf-8")