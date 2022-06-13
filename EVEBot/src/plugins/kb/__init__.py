from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot, Message
import urllib.parse
from nonebot.plugin import require as pluginR
import requests
import json
import asyncio
import httpx

tool = pluginR('tool')
group_ids = tool.group_ids

headers = {"accept": "application/json", "Cache-Control": "no-cache"}

client = httpx.AsyncClient()

kb = on_regex(r'^[\.。](kb|zkb)\s*\S+')
@kb.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    name = str(event.get_message()).split(' ', 1)[1].strip()
    name_urlcode = urllib.parse.quote(name)
    try:
        name_re =  await client.get(url=f'https://esi.evetech.net/latest/search/?categories=character&datasource=tranquility&language=en&search={name_urlcode}&strict=true', headers=headers)
    except httpx.ConnectTimeout:
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
    except httpx.ConnectTimeout:
        await kb.finish(message=Message('zkb网连接失败，请稍后进行查询！'))
        return
    if zkb_re.status_code != 200 :
        await kb.finish(message=Message('zkb网连接失败，请稍后进行查询！'))
        return
    zkb_json = zkb_re.json()
    
    if zkb_json['info'] is None :
        await kb.finish(message=Message(f'zkb网没有收录 {name} 的km信息，该玩家目前没有PVP记录！'))
        return
    
    msg = ''
    msg =  msg + f'[CQ:image,file=https://images.evetech.net/characters/{character_id}/portrait?size=128]' + '\n'
    msg =  msg + f'角色名: {name}\n'

    # if 'title' in zkb_json['info'] :
        # title = zkb_json['info']['title']
        # msg = msg + f'title: {title}\n'

    birthday = zkb_json['info']['birthday'].split('T')[0]
    msg = msg + f'创建日期: {birthday}\n'
    corporation_str = None
    alliance_str = None
    count = len(zkb_json['topLists'])
    i = 0
    while i < count :
        if zkb_json['topLists'][i]['type'] == 'corporation' and len(zkb_json['topLists'][i]['values']) != 0 :
            corporation_str = zkb_json['topLists'][i]['values'][0]['corporationName'] + ' [' + zkb_json['topLists'][i]['values'][0]['cticker'] + ']'
        if zkb_json['topLists'][i]['type'] == 'alliance' and len(zkb_json['topLists'][i]['values']) != 0 :
            alliance_str = zkb_json['topLists'][i]['values'][0]['allianceName'] + ' <' + zkb_json['topLists'][i]['values'][0]['aticker'] + '>'
        i = i + 1
    if corporation_str is not None :
        msg = msg + f'公司: {corporation_str}\n'
    if alliance_str is not None :
        msg = msg + f'联盟: {alliance_str}\n'
    dangerRatio = zkb_json['dangerRatio']
    secStatus = zkb_json['info']['secStatus']
    msg = msg + f'威胁: {dangerRatio}% | 安等: {secStatus:.1f}\n'
    shipsDestroyed = zkb_json['shipsDestroyed']
    pointsDestroyed = zkb_json['pointsDestroyed']
    msg = msg + f'击杀: {shipsDestroyed} | Points: {pointsDestroyed}\n'
    shipsLost = zkb_json['shipsLost']
    pointsLost = zkb_json['pointsLost']
    msg = msg + f'损失: {shipsLost} | Points: {pointsLost}\n'
    soloKills = zkb_json['soloKills']
    msg = msg + f'SOLO: {soloKills}\n'
    msg = msg + f'https://zkillboard.com/character/{character_id}/'
    
    await kb.finish(message=Message(msg))