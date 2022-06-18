from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot, Message
import urllib.parse
from nonebot.plugin import require as pluginR
import requests
import json
import asyncio
import httpx
import re
import html

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

client = httpx.AsyncClient()

kb = on_regex(r'^[\.。](kb|zkb) \s*\S+')
@kb.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    name = str(event.get_message()).split(' ', 1)[1].strip()
    name_urlcode = urllib.parse.quote(name)
    try:
        name_re =  await client.get(url=f'https://esi.evetech.net/latest/search/?categories=character&datasource=tranquility&language=en&search={name_urlcode}&strict=true', headers=headers)
    except:
        await kb.finish(message=Message('当前网络连接错误，请稍后进行查询！'))
        return
    if name_re.status_code != 200 :
        await kb.finish(message=Message('当前网络连接错误，请稍后进行查询！'))
        return
    name_json = name_re.json()

    if 'character' in name_json :
        character_id = name_json['character'][0]
    else:
        await kb.finish(message=Message('名字有误，请检查名字是否正确！'))
        return

    try:
        zkb_re = await client.get(url=f'https://zkillboard.com/api/stats/characterID/{character_id}/')
    except:
        await kb.finish(message=Message('zkb网连接失败，请稍后进行查询！'))
        return
    if zkb_re.status_code != 200 :
        await kb.finish(message=Message('zkb网连接失败，请稍后进行查询！'))
        return
    zkb_json = zkb_re.json()

    if zkb_json['info'] is None :
        await kb.finish(message=Message(f'zkb网没有收录 {name} 的km信息，该玩家目前没有被收录的km记录！'))
        return

    msg = ''
    msg =  msg + f'[CQ:image,file=https://images.evetech.net/characters/{character_id}/portrait?size=128]' + '\n'
    msg =  msg + f'角色名: {name}\n'

    if 'birthday' in zkb_json['info'] :
        birthday = zkb_json['info']['birthday'].split('T')[0]
        msg = msg + f'创建日期: {birthday}\n'

    if 'title' in zkb_json['info'] :
        title = re.sub(r'<[^>]*>', '', zkb_json['info']['title'])
        title = html.unescape(title)
        msg = msg + f'头衔: {title}\n'

    corporation_str = None
    alliance_str = None
    for i in range(len(zkb_json['topLists'])) :
        if zkb_json['topLists'][i]['type'] == 'corporation' and len(zkb_json['topLists'][i]['values']) != 0 :
            corporation_str = zkb_json['topLists'][i]['values'][0]['corporationName'] + ' [' + zkb_json['topLists'][i]['values'][0]['cticker'] + ']'
        if zkb_json['topLists'][i]['type'] == 'alliance' and len(zkb_json['topLists'][i]['values']) != 0 :
            alliance_str = zkb_json['topLists'][i]['values'][0]['allianceName'] + ' <' + zkb_json['topLists'][i]['values'][0]['aticker'] + '>'
    if corporation_str is None and 'corporationID' in zkb_json['info'] :
        try:
            corporation_re = await client.get(url=f"https://esi.evetech.net/latest/corporations/{zkb_json['info']['corporationID']}/?datasource=tranquility", headers=headers)
            if corporation_re.status_code == 200 :
                corporation_json = corporation_re.json()
                corporation_str = corporation_json['name'] + ' [' + corporation_json['ticker'] + ']'
        except:
            pass
    if alliance_str is None and 'allianceID' in zkb_json['info'] :
        try:
            alliance_re = await client.get(url=f"https://esi.evetech.net/latest/alliances/{zkb_json['info']['allianceID']}/?datasource=tranquility", headers=headers)
            if alliance_re.status_code == 200 :
                alliance_json = alliance_re.json()
                alliance_str = alliance_json['name'] + ' <' + alliance_json['ticker'] + '>'
        except:
            pass
    if corporation_str is not None :
        msg = msg + f'公司: {corporation_str}\n'
    if alliance_str is not None :
        msg = msg + f'联盟: {alliance_str}\n'
    if 'dangerRatio' in zkb_json :
        dangerRatio = zkb_json['dangerRatio']
    else:
        dangerRatio = 0
    msg = msg + f'威胁: {dangerRatio}%'
    if 'secStatus' in zkb_json['info'] :
        secStatus = f"{zkb_json['info']['secStatus']:.1f}"
        if secStatus == '-0.0' :
            secStatus = '0.0'
    else:
        secStatus = None
    if secStatus is not None:
        msg = msg + f' | 安等: {secStatus}\n'
    else:
        msg = msg + '\n'
    if 'shipsDestroyed' in zkb_json :
        shipsDestroyed = zkb_json['shipsDestroyed']
    else:
        shipsDestroyed = 0
    if 'iskDestroyed' in zkb_json :
        iskDestroyed = zkb_json['iskDestroyed']
    else:
        iskDestroyed = 0
    msg = msg + f'击杀: {shipsDestroyed} | 价值: {iskDestroyed:,.0f}\n'
    if 'shipsLost' in zkb_json :
        shipsLost = zkb_json['shipsLost']
    else:
        shipsLost = 0
    if 'iskLost' in zkb_json :
        iskLost = zkb_json['iskLost']
    else:
        iskLost = 0
    msg = msg + f'损失: {shipsLost} | 价值: {iskLost:,.0f}\n'
    if 'soloKills' in zkb_json :
        soloKills = zkb_json['soloKills']
    else:
        soloKills = 0
    msg = msg + f'SOLO: {soloKills}\n'
    msg = msg + f'https://zkillboard.com/character/{character_id}/'

    await kb.finish(message=Message(msg))
