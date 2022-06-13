from nonebot import on_notice
from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent
from nonebot.plugin import require as pluginR

tool = pluginR('tool')
group_ids = tool.group_ids

welcome = on_notice()

# 群友入群
@welcome.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State): # event: GroupIncreaseNoticeEvent 群成员增加事件
    # user = event.get_user_id() # 获取新成员的id(str)
    if event.group_id in group_ids:
        data = await bot.call_api('get_group_member_info', **{
            'group_id': event.group_id,
            'user_id': event.user_id
        })
        nickname = data['nickname']
        await welcome.finish(message=Message(
            f'欢迎 {nickname} 加入 EVE(欧服) 新人群\n'
            '\n'
            '游戏下载：https://www.eveonline.com/download\n'
            '游戏汉化：https://zhpatch2.evemodx.com/'
        ))

'''
# 群友退群
@welcome.handle()
async def h_r(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):  # event: GroupDecreaseNoticeEvent  群成员减少事件
    user = event.get_user_id()  # 获取新成员的id
    at_ = "[CQ:at,qq={}]".format(user)
    msg = at_ + '勇士离开了本群，大家快出来送别它吧！'
    msg = Message(msg)
    print(at_)

    if event.group_id == QQ群号:
        await welcome.finish(message=Message(f'{msg}'))  # 发送消息
'''

'''
reply = on_message()
# 群消息
@reply.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.group_id == 361638433 :
        data = await bot.call_api('get_group_member_info', **{
            'group_id': event.group_id,
            'user_id': event.user_id
        })
        nickname = data['nickname']
        await reply.finish(message=Message(
            f'欢迎 {nickname} 加入 伏羲 EVE(欧服) 新人群\n'
            '\n'
            '新手教程：https://docs.qq.com/doc/DQmhZc3lvc09raFFV\n'
            '伏羲官网：https://www.fuxilegion.com/\n'
            '游戏下载：https://www.eveonline.com/download\n'
            '游戏汉化：https://zhpatch2.evemodx.com/'
        ))
        print('finish')
'''
