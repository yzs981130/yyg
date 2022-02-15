import os
import requests
import json

ftapi = os.getenv('FT_ENDPOINT')
larkapi = os.getenv('LARK_ENDPOINT')

headers = {
    'authority': 'vtravel.link2shops.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'token': 'null',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://vtravel.link2shops.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://vtravel.link2shops.com/yiyuan/',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
}

data = '{"activityTag":"yyg","catagoryId":"HDFL202012230001"}'

response = requests.post('https://vtravel.link2shops.com/vfuliApi/api/client/ypJyActivity/goodsList', headers=headers,
                         data=data)

goods_list = json.loads(response.text).get('data').get('goodsList')

print(len(goods_list))

concern_goods_list = ['爱奇艺', '腾讯视频']


# concern_goods_list = ['简单心理']


def ft_notify(content):
    a = {
        'text': content
    }
    requests.post(ftapi, data=a)


def lark_notify(content):
    a = {
        'msg_type': 'text',
        'content': {
            'text': content
        }
    }
    requests.post(larkapi, json=a)


def isConcern(n):
    for t in concern_goods_list:
        if t in n:
            return True
    return False


for goods in goods_list:
    if isConcern(goods['name']) and goods['stock'] > 0:
        print(goods)
        text = "{}:{}个".format(goods['name'], goods['stock'])
        lark_notify(text)
