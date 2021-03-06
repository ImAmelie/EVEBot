import time
import asyncio
from nonebot.plugin import export
from nonebot.plugin import require as pluginR

util = export()

tool = pluginR('tool')
settings = pluginR('settings')

async def isPass():
    await tool.lock.acquire()
    cur_time = time.time()
    if cur_time - tool.time < tool.seconds :
        tool.lock.release()
        return True
    tool.time = cur_time
    tool.lock.release()
    return False

util.isPass = isPass

async def isBan(user_id: int):
    if user_id in settings.data['ban'] :
        return True
    else:
        return False

util.isBan = isBan