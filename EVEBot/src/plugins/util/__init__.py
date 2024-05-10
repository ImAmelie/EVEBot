import time
import asyncio
from nonebot import require

from types import SimpleNamespace
util = SimpleNamespace()

require('tool')
from src.plugins.tool import tool

require('settings')
from src.plugins.settings import settings

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
