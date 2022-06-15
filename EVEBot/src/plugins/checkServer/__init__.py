from nonebot import require
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.plugin import require as pluginR
import nonebot
import json
import asyncio
import httpx

tool = pluginR('tool')
group_id = tool.group_id
group_ids = tool.group_ids

bot = None
init = True

flag = False

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

scheduler = require("nonebot_plugin_apscheduler").scheduler

client = httpx.AsyncClient()

async def check_server_every_1_min():
    global bot
    global flag
    
    print('================================================') # debug
    
    if bot is None :
        bot = nonebot.get_bot()

    try:
        re = await client.get(url=f'https://esi.evetech.net/latest/status/?datasource=tranquility', headers=headers)
    except:
        return
    if re.status_code != 200 :
        return
    re_json = re.json()
    if 'players' in re_json :
        if re_json['players'] > 0 :
            if flag :
                for v in group_ids :
                    await bot.send_msg(message_type='group', group_id=v, message=Message('服务器已上线'))
                flag = False
                scheduler.remove_job('check_server_every_1_min')

@scheduler.scheduled_job('cron', hour=19, minute=0, id='check_server') # debug time
async def check_server():
    global bot
    global init
    global flag

    if bot is None :
        bot = nonebot.get_bot()
    
    flag = True
    
    scheduler.add_job(check_server_every_1_min, 'interval', minutes=1, id='check_server_every_1_min')

# scheduler.add_job(check_server, 'cron', hour=19, minute=0)
