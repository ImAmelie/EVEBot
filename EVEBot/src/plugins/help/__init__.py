from nonebot import on_regex
from nonebot.adapters.cqhttp import Event, Bot
from nonebot.plugin import require as pluginR

# on_command('help', aliases={'帮助'})

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

help = on_regex(r'^[\.。](help|帮助)\s*$')
@help.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return

    if await util.isPass() :
        return

    await help.finish(
        'EVEBot：\n'
        '.help / .帮助\n'
        '.a / .攻略 <关键字>\n'
        '.list # 列出所有攻略关键字\n'
        '.search / .搜索 <关键字>\n'
        '.jita / .吉他 / .jt\n'
        '.jita <物品名> # 吉他查价\n'
        '.jita <物品名> * 数量 # 吉他查价\n'
        '.suit <物品名> # 查询物品组中所有物品价格\n'
        '.tr / .tran / .翻译 <字符串> # 翻译\n'
        '.seat\n'
        '.mum / .妈宝\n'
        '.教程 / .教学 / .新人 / .新手\n'
        '.公司 / .军团\n'
        '.官网 / .EVE / .eve / .申诉 / .客服\n'
        '.zh / .汉化 / .中文\n'
        '.kb / .zkb <name> # 查询人物基础信息\n'
        '.tool / .工具 / .常用\n'
        '.考古\n'
        '.注册\n'
        '管理员命令：\n'
        '.bind <别名>,<物品名> \n'
        '.unbind <别名>\n'
        '.limit / .限制 <数字>\n'
        '.load # 载入攻略文件'
    )

seat = on_regex(r'^[\.。]seat\s*$')
@seat.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await seat.finish(
        'https://github.com/eveseat/seat'
    )

mumble = on_regex(r'^[\.。](mum|mumble|妈宝)\s*$')
@mumble.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await mumble.finish(
        'https://www.mumble.info/'
    )

tutor = on_regex(r'^[\.。](tutor|教程|教学|新手|新人)\s*$')
@tutor.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await tutor.finish(
        '新人教学'
    )

website = on_regex(r'^[\.。](website|公司|军团)\s*$')
@website.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await website.finish(
        '军团官网：https://example.com'
    )

EVEOnline = on_regex(r'^[\.。](EVEOnline|EVE|eve|官网|客服|申诉|网址|角色交易)\s*$')
@EVEOnline.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await EVEOnline.finish(
        'EVE Online 官网：\n'
        'https://www.eveonline.com/' '\n'
        'EVE Online 申诉页面：\n'
        'https://support.eveonline.com/hc/en-us' '\n'
        'EVE Online 官方论坛：\n'
        'https://forums.eveonline.com/' '\n'
        'EVE Online 官方角色交易论坛：\n'
        'https://forums.eveonline.com/c/marketplace/character-bazaar/60' '\n'
    )

zh = on_regex(r'^[\.。](zh|汉化|中文)\s*$')
@zh.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await zh.finish(
        'https://zhpatch2.evemodx.com/'
    )

tools = on_regex(r'^[\.。](tool|工具|常用)\s*$')
@tools.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await tools.finish(
        '常用工具：\n'
        'EVEMarketer(查价)：\n'
        'https://evemarketer.com/\n'
        'zKillboard(KM查询)：\n'
        'https://zkillboard.com/\n'
        'Battle Report Tool(战报分析)：\n'
        'https://br.evetools.org/recent-brs\n'
        'DOTLAN :: EveMaps(星图网站)：\n'
        'https://evemaps.dotlan.net/\n'
        'D-Scan Tool(定向扫描工具)：\n'
        'https://dscan.info/\n'
        '路径安全查询：\n'
        'https://eve-gatecheck.space/eve/\n'
        '合同估价：\n'
        'https://janice.e-351.com/\n'
        'Abyssal Market(深渊装备估价)：\n'
        'https://mutaplasmid.space/\n'
        'Sov.Space(势力分布图)：\n'
        'https://sov.space/\n'
        '虫洞查询：\n'
        'http://anoik.is/\n'
        '爱神虫洞：\n'
        'http://venus.wormholes.club/\n'
        '希拉虫洞查询：\n'
        'http://www.eve-scout.com/\n'
        'LP Store(LP查询)(英文)：\n'
        'https://www.fuzzwork.co.uk/lpstore/\n'
        'EVE-LP(LP查询)(中文)：\n'
        'https://eve-lp.com/#/\n'
        'Eve Who：\n'
        'https://evewho.com/\n'
        '主权时间查询：\n'
        'https://timerboard.net/'
    )

wafen = on_regex(r'^[\.。](挖坟|考古)\s*$')
@wafen.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await wafen.finish(
        '南北派专家组考古探险指南：\n'
        'https://notwojack.github.io/EVE-Exploration-Guide/#/'
    )

register = on_regex(r'^[\.。](注册)\s*$')
@register.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() :
        return
    await register.finish(
        '新人注册链接：\nhttps://example.com\n说明'
    )
