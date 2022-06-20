from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.plugin import require as pluginR

from .get_data import get_price

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

bind = pluginR('bind')

jita = on_regex(r'^[\.。](jita|吉他|jt)\s*\S+')
@jita.handle()
async def _(bot: Bot, event: Event):
    global bind

    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return

    if await util.isPass() or await util.isBan(event.user_id) :
        return

    name = str(event.get_message()).split(' ', 1)[1].strip()

    num = 1
    if name.find('*') != -1 :
        s = name.split('*', 1)
        name = s[0].strip()
        if s[1].strip().isdigit() :
            num = int(s[1].strip())

    if name in bind.bind :
        name = bind.bind[name]

    if name != '' :
        re = await get_price(name, num)
        await jita.finish(message=Message(re))
    else:
        await jita.finish(message=Message('输入不正确，请重新输入！'))
