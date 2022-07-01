import os
import re
import yaml
import nonebot
from nonebot import on_regex
from nonebot.plugin import export
from nonebot.plugin import require as pluginR
from nonebot.adapters.cqhttp import Event, Bot, Message

config = nonebot.get_driver().config

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

bind=export()

path = os.path.abspath(os.path.dirname(__file__))
file = open(path + '/' + 'bind.yaml', 'r', encoding='utf-8')
bind.bind = yaml.load(file.read(), Loader=yaml.FullLoader)
file.close()

if not bind.bind :
    bind.bind = {}

bind_function = on_regex(r'^[\.。](bind|绑定) \s*\S+')
@bind_function.handle()
async def _(bot: Bot, event: Event):
    global bind

    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() or await util.isBan(event.user_id) :
        return
    if not (str(event.user_id) in config.superusers) :
        await bind_function.finish(message=Message(
            f'[CQ:at,qq={event.user_id}]'
            ' 不是机器人管理员，无法使用此命令！'
        ))
        return
    tmp = re.split(r'[,，]', str(event.get_message()).split(' ', 1)[1], 1)
    key = tmp[0].strip().lower()
    value = tmp[1].strip().lower()
    bind.bind[key] = value

    with open(path + '/' + 'bind.yaml', 'w', encoding='utf-8') as file :
        yaml.dump(dict(bind.bind), file, allow_unicode=True, sort_keys=False)

    await bind_function.finish(message=Message('绑定成功'))

unbind_function = on_regex(r'^[\.。](unbind|解绑) \s*\S+')
@unbind_function.handle()
async def _(bot: Bot, event: Event):
    global bind

    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() or await util.isBan(event.user_id) :
        return
    if not (str(event.user_id) in config.superusers) :
        await unbind_function.finish(message=Message(
            f'[CQ:at,qq={event.user_id}]'
            ' 不是机器人管理员，无法使用此命令！'
        ))
        return
    key = str(event.get_message()).split(' ', 1)[1].strip()
    key = key.lower()
    if key in bind.bind :
        del bind.bind[key]

    with open(path + '/' + 'bind.yaml', 'w', encoding='utf-8') as file :
        yaml.dump(dict(bind.bind), file, allow_unicode=True, sort_keys=False)

    await unbind_function.finish(message=Message('解绑成功'))
