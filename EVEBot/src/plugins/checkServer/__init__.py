from nonebot import require
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.plugin import require as pluginR
import nonebot
import json
import asyncio
import httpx
from datetime import datetime
from dateutil import tz

tool = pluginR('tool')
group_id = tool.group_id
group_ids = tool.group_ids

bot = None
init = True

flag = False

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

scheduler = require("nonebot_plugin_apscheduler").scheduler

client = httpx.AsyncClient()

async def check_server_every_1_time():
    global bot
    global flag

    if bot is None :
        bot = nonebot.get_bot()

    try:
        re = await client.get(url=f'https://esi.evetech.net/latest/status/?datasource=tranquility', headers=headers)
    except:
        return
    if re.status_code != 200 :
        return
    re_json = re.json()
    if 'start_time' in re_json :
        if flag :
            msg = '服务器已上线！\n服务器启动时间：'

            utc_zone = tz.tzutc()
            local_zone = tz.gettz('Asia/Shanghai')
            utc_time = datetime.strptime(re_json['start_time'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=utc_zone)
            local_time_str = utc_time.astimezone(local_zone).strftime('%Y-%m-%d %H:%M:%S')

            msg = msg + local_time_str

            for v in group_ids :
                await bot.send_msg(message_type='group', group_id=v, message=Message(msg))
            flag = False
            scheduler.remove_job('check_server_every_1_time')

@scheduler.scheduled_job('cron', hour=19, minute=0, second=30, id='check_server') # debug time
async def check_server():
    global bot
    global init
    global flag

    if bot is None :
        bot = nonebot.get_bot()

    flag = True

    scheduler.add_job(check_server_every_1_time, 'interval', seconds=10, id='check_server_every_1_time')

# scheduler.add_job(check_server, 'cron', hour=19, minute=0)
