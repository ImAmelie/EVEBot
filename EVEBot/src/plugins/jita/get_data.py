import re
import httpx
import urllib.parse

from nonebot.plugin import require

data = require('data')

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

client = httpx.AsyncClient()

# 获得物品ID
# 返回值：
#   -1 : 查询失败，没找到
#   -2 : 网络错误
#   其他 : 查询成功
async def get_itemID(name: str):
    name_en = name.lower()
    for k, v in data.data.items() :
        if v['name']['en'].lower() == name_en :
            if 'zh' in v['name'] :
                return [ k, v['name']['zh'] + '/' + v['name']['en'] ]
            else:
                return [ k, v['name']['en'] ]
        if ('zh' in v['name']) and (v['name']['zh'] == name) :
            return [ k, v['name']['zh'] + '/' + v['name']['en'] ]
    for k, v in data.data.items() :
        if v['name']['en'].lower().find(name_en) != -1 :
            if 'zh' in v['name'] :
                return [ k, v['name']['zh'] + '/' + v['name']['en'] ]
            else:
                return [ k, v['name']['en'] ]
        if 'zh' in v['name'] and v['name']['zh'].find(name) != -1 :
            return [ k, v['name']['zh'] + '/' + v['name']['en'] ]

    name = re.sub('[\"\']', '', name)
    name_en = re.sub('[\"\']', '', name_en)
    if len(name) <= 2 :
        name = f' {name} '
    if len(name_en) <= 2 :
        name_en = f' {name_en} '
    url_name_zh = urllib.parse.quote(name)
    url_name_en = urllib.parse.quote(name_en)
    try:
        re_zh = await client.get(url=f'https://esi.evetech.net/latest/search/?categories=inventory_type&datasource=tranquility&language=zh&search={url_name_zh}&strict=false', headers=headers)
    except:
        return [ -2, '' ]
    re_zh_json = re_zh.json()
    if 'inventory_type' in re_zh_json :
        itemID = re_zh_json['inventory_type'][0]
        itemName = ''
        if 'zh' in data.data[itemID]['name'] :
            itemName = itemName + data.data[itemID]['name']['zh'] + '/'
        itemName = itemName + data.data[itemID]['name']['en']
        return [ itemID, itemName ]
    try:
        re_en = await client.get(url=f'https://esi.evetech.net/latest/search/?categories=inventory_type&datasource=tranquility&language=en&search={url_name_en}&strict=false', headers=headers)
    except:
        return [ -2, '' ]
    re_en_json = re_en.json()
    if 'inventory_type' in re_en_json :
        itemID = re_en_json['inventory_type'][0]
        itemName = ''
        if 'zh' in data.data[itemID]['name'] :
            itemName = itemName + data.data[itemID]['name']['zh'] + '/'
        itemName = itemName + data.data[itemID]['name']['en']
        return [ itemID, itemName ]

    return [ -1, '' ]

async def get_price(name: str, num: int = 1):
    item = await get_itemID(name)
    if item[0] in [ -1 ] :
        return '查询失败，请检查输入的关键字是否准确！'
    if item[0] in [ -2 ] :
        return '连接服务器失败，请稍后尝试！'
    itemID = item[0]
    name = item[1]
    try:
        re = await client.get(url=f'https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&type_id={itemID}', headers=headers)
    except:
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
