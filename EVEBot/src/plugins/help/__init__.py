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

    if await util.isPass() or await util.isBan(event.user_id) :
        return

    await help.finish(
        'EVEBot：\n'
        '.help / .帮助\n'
        '.a / .gl / .攻略 <关键字>\n'
        '.list # 列出所有攻略关键字\n'
        '.gl list # 列出所有攻略关键字\n'
        '.search / .搜索 <关键字>\n'
        '.jita / .吉他 / .jt\n'
        '.jita <物品名> # 吉他查价\n'
        '.jita <物品名> * 数量 # 吉他查价\n'
        '.suit <物品名> # 查询物品组中所有物品价格\n'
        '.tr / .tran / .翻译 <字符串> # 翻译\n'
        '.kb / .zkb <name> # 查询人物基础信息\n'
        '.tool / .工具 / .常用 # 常用工具网址\n'
        '.map / .地图 # 翻译地图名称\n'
        '管理员命令：\n'
        '.bind / .绑定 <别名>,<物品名> \n'
        '.unbind / .解绑 <别名>\n'
        '.limit / .限制 <数字>\n'
        '.load / .加载 # 载入攻略文件'
    )

tools = on_regex(r'^[\.。](tool|工具|常用)\s*$')
@tools.handle()
async def _(bot: Bot, event: Event):
    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() or await util.isBan(event.user_id) :
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
