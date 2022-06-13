# import urllib.parse # urllib.parse.quote(name)
import requests
import json
import yaml
import asyncio
import httpx

from nonebot.plugin import require

data = require('data')

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

client = httpx.AsyncClient()

# 获得物品ID
# 返回值：
#   -1 : 查询失败，没找到
#   其他 : 查询成功
async def get_itemID(name: str):
    name_en = name.lower()
    for k, v in data.data.items() :
        if v['name']['en'].lower() == name_en :
            return [ k, v['name']['zh'] + '/' + v['name']['en'] ]
        if ('zh' in v['name']) and (v['name']['zh'] == name) :
            return [ k, v['name']['zh'] + '/' + v['name']['en'] ]
    for k, v in data.data.items() :
        if v['name']['en'].lower().find(name_en) != -1 :
            return [ k, v['name']['zh'] + '/' + v['name']['en'] ]
        if 'zh' in v['name'] and v['name']['zh'].find(name) != -1 :
            return [ k, v['name']['zh'] + '/' + v['name']['en'] ]
    return [ -1, '' ]

async def get_price(name: str, num: int = 1):
    item = await get_itemID(name)
    if item[0] in [ -1 ] :
        return '查询失败，请检查输入的关键字是否准确！'
    itemID = item[0]
    name = item[1]
    try:
        re = await client.get(url=f'https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&type_id={itemID}', headers=headers)
    except httpx.ConnectTimeout:
        return '连接服务器失败，请稍后尝试！'
    if re.status_code != 200 :
        return '连接服务器失败，请稍后尝试！'
    re_json = re.json()
    buy = 0
    sell = 0
    for i in range(len(re_json)) :
        if re_json[i]['is_buy_order'] == True : # 买单
            if re_json[i]['price'] > buy :
                buy = re_json[i]['price']
        else: # 卖单
            if re_json[i]['price'] < sell or sell == 0 :
                sell = re_json[i]['price']
    buy = buy * num
    sell = sell * num
    return name + ' * ' + str(num) + ' :\n' + '    sell: ' + f'{sell:,.2f}' + '\n' + '    buy : ' + f'{buy:,.2f}'

async def get_price_all(name: str):
    item = await get_itemID(name)
    if item[0] in [ -1 ] :
        return '查询失败，请检查输入的关键字是否准确！'
    itemID = item[0]
    if 'marketGroupID' not in data.data[itemID] :
        return f'{name} 没有所属物品组！'
    marketGroupID = data.data[itemID]['marketGroupID']

    try:
        marketGroup_re = await client.get(url=f'https://esi.evetech.net/latest/markets/groups/{marketGroupID}/?datasource=tranquility&language=zh', headers=headers)
    except:
        return '连接服务器失败，请稍后尝试！'
    if marketGroup_re.status_code != 200 :
        return '连接服务器失败，请稍后尝试！'
    marketGroup_json = marketGroup_re.json()

    items = marketGroup_json['types']

    # msg = f'{name} 的查询结果：\n'
    msg = f'{item[1]} 的查询结果：\n'

    for itemID in items :
        name = data.data[itemID]['name']['zh'] + '/' + data.data[itemID]['name']['en']
        try:
            re = await client.get(url=f'https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&type_id={itemID}', headers=headers)
        except:
            return '连接服务器失败，请稍后尝试！'
        if re.status_code != 200 :
            return '连接服务器失败，请稍后尝试！'
        re_json = re.json()
        buy = 0
        sell = 0
        for i in range(len(re_json)) :
            if re_json[i]['is_buy_order'] == True : # 买单
                if re_json[i]['price'] > buy :
                    buy = re_json[i]['price']
            else: # 卖单
                if re_json[i]['price'] < sell or sell == 0 :
                    sell = re_json[i]['price']
        msg = msg + '\n'
        msg = msg + name + ' :\n' + '    sell: ' + f'{sell:,.2f}' + '\n' + '    buy : ' + f'{buy:,.2f}'
    return msg
