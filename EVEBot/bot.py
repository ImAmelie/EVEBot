#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.log import logger, default_format

logger.add("error.log", level="ERROR", format=default_format, rotation="1 week")

nonebot.init(apscheduler_autostart=True, apscheduler_config={"apscheduler.timezone": "Asia/Shanghai"})
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# nonebot.load_builtin_plugins("echo") # 加载内置插件
# nonebot.load_plugins("src/plugins")

nonebot.load_plugin('src.plugins.tool')
nonebot.load_plugin('src.plugins.bind')
nonebot.load_plugin('src.plugins.settings')
nonebot.load_plugin('src.plugins.data')
nonebot.load_plugin('src.plugins.help')
nonebot.load_plugin('src.plugins.welcome')
nonebot.load_plugin('src.plugins.cmd')
nonebot.load_plugin('src.plugins.jita') # 依赖 bind data
nonebot.load_plugin('src.plugins.translate') # 依赖 data
nonebot.load_plugin('src.plugins.search') # 依赖 data
nonebot.load_plugin('src.plugins.km')
nonebot.load_plugin('src.plugins.kb')
nonebot.load_plugin('src.plugins.checkServer')

# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
# nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
