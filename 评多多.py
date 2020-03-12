import re
import time
import pymongo
import requests
from bs4 import BeautifulSoup

MONGO_URI='localhost'
MONGO_DB='PingDD'

headers={
    'Host':'www.pinduoduo.com',
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding':'gzip, deflate, br',
    'Referer':'https://www.baidu.com/link?url=pDbq4xwJXDh1c2fIDJ4LBcROJBI4VW041I-OwN-VObrGyPlkCn588gSrSWBkhJvb&wd=&eqid=edace145000f5603000000065e6a1d16',
    'Connection':'keep-alive',
    'Cookie':'api_uid=rBQQsF5qHRgTbji+3A8FAg==; _nano_fp=XpdJn09aX5djl0PbnC_N6g2JWOCLC3Tw8HVJxagT',
    'Upgrade-Insecure-Requests':'1',
    'Cache-Control':'max-age=0',
}
headers_index={
    'Host':'cdn.pinduoduo.com',
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Accept':'*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'Referer':'https://www.pinduoduo.com/',
    'Cookie':'api_uid=rBQQsF5qHRgTbji+3A8FAg==',
}
headers_subject={
    'Host':'apiv2.pinduoduo.com',
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Accept':'application/json, text/javascript',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding':'gzip, deflate, br',
    'Content-Type':'application/json;charset=UTF-8',
    'Origin':'https://www.pinduoduo.com',
    'Connection':'keep-alive',
    'Referer':'https://www.pinduoduo.com/',
}

def Request():
    url = 'https://www.pinduoduo.com/'
    response=requests.get(url,headers=headers)
    with open('PingDD.html','wb')as f:
        f.write(response.content)

def url_index():
    html=open('PingDD.html','r').read()
    print(html)
    soup = BeautifulSoup(html, 'lxml')
    url_index ='https:' + soup.select_one('#__NEXT_PAGE__\/').get('src')
    print(url_index)
    response_index = requests.get(url_index, headers=headers_index)
    with open('PingDD_index.html','wb')as f:
        f.write(response_index.content)

def Subject_id():
    html = open('PingDD_index.html', 'r').read()
    pattern=re.compile('subject_id:(\d+)')
    subject_id=re.findall(pattern,html)
    return subject_id

def Subject_Request(subject_id):
    subject_url ='https://apiv2.pinduoduo.com/api/gindex/subject/limited/goods?subject_id={ID}&page=1&size=10'
    for id in subject_id:
        url=subject_url.format(ID=id)
        print(url)
        response=requests.get(url,headers=headers_subject).json()
        for goods in response['data']:
            DOODS={
                'short_name':goods.get('short_name'),
                'group_price':goods.get('group_price')/100,
                'market_price':goods.get('market_price')/100,
                'sales_tip':goods.get('sales_tip')
            }
            print(DOODS)
            time.sleep(1)
            save(goods.get('short_name'),DOODS)

def save(name,goods):
    client=pymongo.MongoClient(MONGO_URI)
    table=client[MONGO_DB]
    table[name].insert(goods)

def main():
    Request()
    url_index()
    subject_id = Subject_id()
    Subject_Request(subject_id)

if __name__ == '__main__':
    main()




