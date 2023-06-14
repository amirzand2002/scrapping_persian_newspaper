import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}


def get_f_news_id():
    # get the oldest issue number and link
    url = 'https://newspaper.hamshahrionline.ir/archive'
    response = requests.request("GET", url=url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    news_data = data.find_all('li', attrs={'class', 'page-item'})[-2]
    per_date_archive = news_data.find('a').get('href')
    url_per_date_archive = 'https://newspaper.hamshahrionline.ir' + per_date_archive
    response_per_date_archive = requests.request("GET", url=url_per_date_archive, headers=headers)
    data_per_date_archive = BeautifulSoup(response_per_date_archive.text, 'html.parser')
    news_data_per_date_archive = data_per_date_archive.find_all('div', attrs={'class', 'col-md-4'})[-1]
    news_data_per_date_archive = news_data_per_date_archive.find('a').get('href')
    first_news_id = news_data_per_date_archive.replace('/?n=', '')
    first_news_id = int(first_news_id)
    return first_news_id


def get_lat_news_id():
    # get the latest issue number and link
    url = 'https://newspaper.hamshahrionline.ir/archive'
    response = requests.request("GET", url=url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    news_link = data.find('div', attrs={'class', 'col-md-4'})
    news_link = news_link.find('a').get('href')
    latest_news_id = news_link.replace('/?n=', '')
    latest_news_id = int(latest_news_id)
    return latest_news_id


scarped_data = []
latest_news_id = get_lat_news_id()
old_news_id = get_f_news_id()
while old_news_id <= latest_news_id:
    print(latest_news_id-old_news_id)
    url = 'https://newspaper.hamshahrionline.ir/?n=' + str(old_news_id)
    old_news_id += 1
    response = requests.request("GET", url=url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    date_element = data.find('li', class_='dir-left')
    date = date_element.get_text(strip=True)
    links = data.find_all(re.compile("^h[1-6]$"))
    for i in links:
        news_detail = {}
        new_page = i.findChild("a")['href']
        response = requests.request("GET", url=new_page, headers=headers)
        data = BeautifulSoup(response.text, 'html.parser')
        title = data.find_all(re.compile("^h[1-6]$"), attrs={'class', 'title'})
        news_data = data.find_all('div', attrs={'class', 'text'})
        for y in title:
            news_detail['title'] = y.text
        for x in news_data:
            news_detail['text'] = x.text

        date_element = data.find('span', id='publishdate')
        news_detail['per_date'] = date_element.get_text(strip=True)
        # news_detail['en_date'] = date
        # time_element = data.find('span', id='publishtime')
        # ['time'] = time_element.get_text(strip=True)

        # writer_element = data.find('div', string='نویسنده :')
        # news_detail['writer'] = writer_element.next_sibling.strip()

        # code_element = data.find('div', string='کد مطلب :')
        # news_detail['code'] = code_element.next_sibling.strip()

        scarped_data.append(news_detail)
dataframe = pd.DataFrame.from_dict(scarped_data)
dataframe.to_csv('hamshahrionline.csv', index=False, encoding="utf-8")

