import asyncio
from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.plugin import require as pluginR

data = pluginR('data')

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

search = on_regex(r'^[\.。](search|搜索)\s*\S+')
@search.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    name = str(event.get_message()).split(' ', 1)[1].strip()
    name_en = name.lower()
    
    flag = False
    
    count = 0
    
    msg = name + ' 的搜索结果：\n'
    for k, v in data.data.items() :
        if (v['name']['en'].lower().find(name_en) != -1) or ('zh' in v['name'] and v['name']['zh'].find(name) != -1) :
            msg = msg + v['name']['zh'] + '/' + v['name']['en'] + '\n'
            flag = True
            count = count + 1
            if count >= 15 :
                await search.send(message=Message(msg))
                await asyncio.sleep(1)
                msg = ''
                count = 0
    if flag == True :
        if count != 0 :
            await search.send(message=Message(msg))
    else:
        await search.send(message=Message('数据库中没查到相关结果，请检查关键字是否输入正确！'))
