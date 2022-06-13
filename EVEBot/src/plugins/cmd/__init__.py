import os
import json
import nonebot
from nonebot import on_regex
from nonebot.plugin import export
from nonebot.plugin import require as pluginR
from nonebot.adapters.cqhttp import Event, Bot, Message

config = nonebot.get_driver().config

tool = pluginR('tool')
group_ids = tool.group_ids

path = os.path.abspath(os.path.dirname(__file__))
file = open(path + '/' + 'cmd.json', 'r', encoding='utf-8')
content = json.loads(file.read())
file.close()

load = on_regex(r'^[\.。](load)\s*')
@load.handle()
async def _(bot: Bot, event: Event):
    global content
    
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if str(event.user_id) not in config.superusers :
        await load.finish(message=Message(
            f'[CQ:at,qq={event.user_id}]'
            ' 不是机器人管理员，无法使用此命令！'
        ))
        return
    content.clear()
    with open(path + '/' + 'cmd.json', 'r', encoding='utf-8') as file :
        content = json.loads(file.read())

cmd = on_regex(r'^[\.。](cmd|a|攻略)\s*\S+')
@cmd.handle()
async def _(bot: Bot, event: Event):
    global content

    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    
    s = str(event.get_message()).split(' ', 1)[1].strip()
    
    if s in content :
        msg = content[s]
        await cmd.finish(message=Message(msg))
    else:
        await cmd.finish(message=Message('标题不正确，请检查标题！'))