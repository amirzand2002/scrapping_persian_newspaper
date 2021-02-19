import requests
import pandas as pd 
from bs4 import BeautifulSoup
number = 7271
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

scarped_data=[]
while number<8164:
    url = 'https://newspaper.hamshahrionline.ir/?n='+ str(number)
    response = requests.request("GET",url=url,headers=headers)
    data = BeautifulSoup(response.text,'html.parser')
    news_data = data.find_all('div',attrs={'class','text'})
    date = data.find_all('li',attrs={'class','dir-left'})

    for news in news_data:
        news_detail={}
        #print (news)
        news_detail['news_text']=news.text.encode('utf-8')
        for d in date:
            news_detail['news_date'] = d.text
            if number%100==0:
                print(d.text)
        scarped_data.append(news_detail)
    number+=1
    print number
dataframe=pd.DataFrame.from_dict(scarped_data)
dataframe.to_csv('news_data.csv',index=False)