import os
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

settings = export()

path = os.path.abspath(os.path.dirname(__file__))
file = open(path + '/' + 'settings.yaml', 'r', encoding='utf-8')
settings.data = yaml.load(file.read(), Loader=yaml.FullLoader)
file.close()

if settings.data and ('limit' in settings.data) :
    settings.limit = settings.data['limit']
else:
    settings.limit = 100000000

limit = on_regex(r'^[\.。](limit)\s*\S+')
@limit.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    if not (str(event.user_id) in config.superusers) :
        await limit.finish(message=Message(
            f'[CQ:at,qq={event.user_id}]'
            ' 不是机器人管理员，无法使用此命令！'
        ))
        return
    num = str(event.get_message()).split(' ', 1)[1].strip()
    if num.isdigit() :
        num = float(num)
    else:
        await limit.finish(message=Message('请输入正确的数字！'))
        return
    settings.limit = num
    
    if not settings.data :
        settings.data = {}
    
    settings.data['limit'] = num
    
    with open(path + '/' + 'settings.yaml', 'w', encoding='utf-8') as file :
        yaml.dump(dict(settings.data), file, allow_unicode=True, sort_keys=False)
    
    await limit.finish(message=Message('设置成功！'))
