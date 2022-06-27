import httpx
import asyncio
from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.plugin import require as pluginR

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

bind = pluginR('bind')

data = pluginR('data')

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

client = httpx.AsyncClient()

suit = on_regex(r'^[\.。](suit) \s*\S+')
@suit.handle()
async def _(bot: Bot, event: Event):
    global bind

    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() or await util.isBan(event.user_id) :
        return
    name = str(event.get_message()).split(' ', 1)[1].strip()
    if len(name) < 2 :
        await suit.finish(message=Message('查询关键字必须不少于2字'))
        return

    if name in bind.bind :
        name = bind.bind[name]

    ret = await get_price_all(name)
    ret_count = len(ret)
    for msg in ret :
        await suit.send(message=Message(msg))
        if ret_count != 1 :
            await asyncio.sleep(1)

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

async def get_price_all(name: str):
    item = await get_itemID(name)
    if item[0] in [ -1 ] :
        return [ '查询失败，请检查输入的关键字是否准确！' ]
    itemID = item[0]
    if 'marketGroupID' not in data.data[itemID] :
        return [ f'{name} 没有所属物品组！' ]
    marketGroupID = data.data[itemID]['marketGroupID']

    try:
        marketGroup_re = await client.get(url=f'https://esi.evetech.net/latest/markets/groups/{marketGroupID}/?datasource=tranquility&language=zh', headers=headers)
    except:
        return [ '连接服务器失败，请稍后尝试！' ]
    marketGroup_json = marketGroup_re.json()

    items = marketGroup_json['types']

    ret = []
    count = 0

    # msg = f'{name} 的查询结果：\n\n'
    msg = f'{item[1]} 的查询结果：\n\n'

    for itemID in items :
        name = data.data[itemID]['name']['zh'] + '/' + data.data[itemID]['name']['en']
        try:
            re = await client.get(url=f'https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&type_id={itemID}', headers=headers)
        except:
            return [ '连接服务器失败，请稍后尝试！' ]
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
        msg = msg + name + ' :\n' + '    sell: ' + f'{sell:,.2f}' + '\n' + '    buy : ' + f'{buy:,.2f}' + '\n'
        count = count + 1
        if count >= 10 :
            ret.append(msg)
            msg = ''
            count = 0
    if count != 0 :
        ret.append(msg)
    return ret
