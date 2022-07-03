import re
import httpx
import urllib.parse
from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.plugin import require as pluginR

data = pluginR('data')

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

bind = pluginR('bind')

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

client = httpx.AsyncClient()

tr = on_regex(r'^[\.。](tr|tran|翻译) \s*\S+')
@tr.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() or await util.isBan(event.user_id) :
        return
    name = str(event.get_message()).split(' ', 1)[1].strip()

    if name.lower() in bind.bind :
        name = bind.bind[name.lower()]

    ret = await get_itemID(name)
    if ret[0] in [ -1 ] :
        await tr.finish(message=Message('翻译失败，请检查输入的关键字是否准确！'))
    elif ret[0] in [ -2 ] :
        await tr.finish(message=Message('连接服务器失败，请稍后尝试！'))
    else:
        await tr.finish(message=Message(ret[1]))

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
