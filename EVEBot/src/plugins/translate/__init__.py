from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.plugin import require as pluginR

data = pluginR('data')

tool = pluginR('tool')
group_ids = tool.group_ids

tr = on_regex(r'^[\.。](tr|tran|翻译)\s*\S+')
@tr.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    name = str(event.get_message()).split(' ', 1)[1].strip()
    ret = await get_itemID(name)
    if ret[0] in [ -1 ] :
        await tr.finish(message=Message('翻译失败，请检查输入的关键字是否准确！'))
    else:
        await tr.finish(message=Message(ret[1]))
    
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