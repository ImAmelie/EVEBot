from nonebot import require
from nonebot import get_driver
from nonebot.adapters.cqhttp import Event, Bot, Message
import nonebot
from nonebot.plugin import require as pluginR
import time
import json
import asyncio
import httpx
import websockets
import ssl
from pathlib import Path

driver=get_driver()

bot = None

tool = pluginR('tool')
# data = tool.data
icon_path = tool.icon_path

settings = pluginR('settings')

# alliance_id = tool.alliance_id
alliance_ids = tool.alliance_ids
corporationID = tool.corporationID
corporationIDs = tool.corporationIDs
group_id = tool.group_id
group_ids = tool.group_ids

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

old_time = 0
seconds_one_time = 60 # 每seconds_one_time秒只能发送sends_per_time条消息
send_num = 0
sends_per_time = 10 # 每seconds_one_time秒只能发送sends_per_time条消息

km_pool = []
km_pool_time = 0
km_pool_expire = 5 * 60 # km池过期时间

client = httpx.AsyncClient()

sslContext = ssl.SSLContext()

@driver.on_bot_connect
async def km():
    global bot
    global old_time
    global seconds_one_time
    global send_num
    global sends_per_time
    global km_pool
    global km_pool_time
    global km_pool_expire

    if bot is None :
        bot = nonebot.get_bot()

    bot = nonebot.get_bot()

    flag = False

    while True:
        try:
            async with websockets.connect('wss://zkillboard.com/websocket/', ssl=sslContext) as websocket:
                for v in alliance_ids :
                    sub_msg = '{' + f'"action":"sub","channel":"alliance:{v}"' + '}'
                    await websocket.send(sub_msg)
                while True:
                    try:
                        re = await websocket.recv()
                    except:
                        break

                    new_time = time.time()
                    if new_time - old_time >= seconds_one_time :
                        old_time = new_time
                        send_num = 0

                    if new_time - km_pool_time >= km_pool_expire :
                        km_pool_time = new_time
                        km_pool.clear()

                    if send_num >= sends_per_time :
                        continue

                    re_json = json.loads(re)

                    killID = re_json['killID']

                    if killID in km_pool :
                        continue
                    else:
                        km_pool.append(killID)

                    try:
                        zkb_re = await client.get(url=f'https://zkillboard.com/api/killID/{killID}/')
                    except:
                        continue
                    if zkb_re.status_code != 200 :
                        continue
                    zkb_json = zkb_re.json()

                    loss = zkb_json[0]['zkb']['totalValue']

                    # 过滤小于指定损失(isk)的km
                    if loss < settings.limit : # debug
                        continue

                    killHash = re_json['hash']
                    try:
                        esi_re = await client.get(url=f'https://esi.evetech.net/latest/killmails/{killID}/{killHash}/?datasource=tranquility')
                    except:
                        continue
                    if esi_re.status_code != 200 :
                        continue
                    esi_json = esi_re.json()

                    # 过滤本联盟被击杀的km
                    if ('alliance_id' in esi_json['victim']) and (esi_json['victim']['alliance_id'] in alliance_ids) : # debug
                        continue

                    msg = ''

                    ship_type_id = re_json['ship_type_id']
                    if tool.esi_image_server or (not Path(f'{icon_path}{ship_type_id}.png'[7:]).exists()):
                        msg = msg + f'[CQ:image,file=https://images.evetech.net/types/{ship_type_id}/render?size=128]' + '\n'
                    else:
                        msg = msg + f'[CQ:image,file={icon_path}{ship_type_id}.png]' + '\n'

                    try:
                        ship_re = await client.get(url=f'https://esi.evetech.net/latest/universe/types/{ship_type_id}/?datasource=tranquility&language=zh', headers=headers)
                    except:
                        continue
                    if ship_re.status_code != 200 :
                        continue
                    ship_json = ship_re.json()
                    ship_name = ship_json['name']
                    msg = msg + f'{ship_name}\n'

                    dead_corporation_ticker = ''
                    dead_alliance_ticker = ''

                    if 'character_id' in esi_json['victim'] :
                        dead_id = esi_json['victim']['character_id']
                        try:
                            dead_re = await client.get(url=f'https://esi.evetech.net/latest/characters/{dead_id}/?datasource=tranquility', headers=headers)
                        except:
                            continue
                        if dead_re.status_code != 200 :
                            continue
                        dead_json = dead_re.json()
                        dead_name = dead_json['name']
                        if 'corporation_id' in dead_json :
                            try:
                                dead_corporation_re = await client.get(url=f'https://esi.evetech.net/latest/corporations/{dead_json["corporation_id"]}/?datasource=tranquility', headers=headers)
                            except:
                                continue
                            if dead_corporation_re.status_code != 200 :
                                continue
                            dead_corporation_json = dead_corporation_re.json()
                            dead_corporation_ticker = '[' + dead_corporation_json['ticker'] + ']'
                        if 'alliance_id' in dead_json :
                            try:
                                dead_alliance_re = await client.get(url=f'https://esi.evetech.net/latest/alliances/{dead_json["alliance_id"]}/?datasource=tranquility', headers=headers)
                            except:
                                continue
                            if dead_alliance_re.status_code != 200 :
                                continue
                            dead_alliance_json = dead_alliance_re.json()
                            dead_alliance_ticker = '<' + dead_alliance_json['ticker'] + '>'
                    else:
                        dead_name = 'NPC'
                    msg = msg + f'被杀者: {dead_name} {dead_corporation_ticker}{dead_alliance_ticker}\n'

                    killer_corporation_ticker = ''
                    killer_alliance_ticker = ''

                    if zkb_json[0]['zkb']['npc'] == True :
                        killer_name = 'NPC'
                        continue # 过滤NPC击杀
                    else:
                        for i in range(len(esi_json['attackers'])) :
                            if esi_json['attackers'][i]['final_blow'] == True :
                                killer_id = esi_json['attackers'][i]['character_id']
                                break
                        try:
                            killer_re = await client.get(url=f'https://esi.evetech.net/latest/characters/{killer_id}/?datasource=tranquility', headers=headers)
                        except:
                            continue
                        if killer_re.status_code != 200 :
                            continue
                        killer_json = killer_re.json()
                        killer_name = killer_json['name']
                        if 'corporation_id' in killer_json :
                            try:
                                killer_corporation_re = await client.get(url=f'https://esi.evetech.net/latest/corporations/{killer_json["corporation_id"]}/?datasource=tranquility', headers=headers)
                            except:
                                continue
                            if killer_corporation_re.status_code != 200 :
                                continue
                            killer_corporation_json = killer_corporation_re.json()
                            killer_corporation_ticker = '[' + killer_corporation_json['ticker'] + ']'
                        if 'alliance_id' in killer_json :
                            if killer_json['alliance_id'] not in alliance_ids :
                                continue # 过滤非关注联盟击杀
                            try:
                                killer_alliance_re = await client.get(url=f'https://esi.evetech.net/latest/alliances/{killer_json["alliance_id"]}/?datasource=tranquility', headers=headers)
                            except:
                                continue
                            if killer_alliance_re.status_code != 200 :
                                continue
                            killer_alliance_json = killer_alliance_re.json()
                            killer_alliance_ticker = '<' + killer_alliance_json['ticker'] + '>'
                        else:
                            continue # 过滤非关注联盟击杀
                    msg = msg + f'击杀者: {killer_name} {killer_corporation_ticker}{killer_alliance_ticker}\n'

                    msg = msg + '损失: ' + f'{loss:,.2f}' + '\n'

                    try:
                        system_id = esi_json['solar_system_id']
                        system_re = await client.get(url=f'https://esi.evetech.net/latest/universe/systems/{system_id}/?datasource=tranquility&language=zh', headers=headers)
                        system_json = system_re.json()
                        system_name = system_json['name']
                        constellation_id = system_json['constellation_id']
                        constellation_re = await client.get(url=f'https://esi.evetech.net/latest/universe/constellations/{constellation_id}/?datasource=tranquility&language=zh', headers=headers)
                        constellation_json = constellation_re.json()
                        constellation_name = constellation_json['name']
                        region_id = constellation_json['region_id']
                        region_re = await client.get(url=f'https://esi.evetech.net/latest/universe/regions/{region_id}/?datasource=tranquility&language=zh', headers=headers)
                        region_json = region_re.json()
                        region_name = region_json['name']
                        msg = msg + f'位置: {system_name} / {constellation_name} / {region_name}\n'
                    except:
                        pass

                    if zkb_json[0]['zkb']['solo'] == True :
                        msg = msg + 'SOLO\n'

                    msg = msg + '\n'

                    km_time = esi_json['killmail_time'][0:-1].split('T')
                    km_time = km_time[0] + ' ' + km_time[1]
                    msg = msg + km_time + '\n'

                    msg = msg + f'https://zkillboard.com/kill/{killID}/'

                    for v in group_ids :
                        await bot.send_msg(message_type='group', group_id=v, message=Message(msg))

                    send_num = send_num + 1
        except:
            pass
