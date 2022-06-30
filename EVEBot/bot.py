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

nonebot.load_plugin('src.plugins.tool') # 提供一些设置(写死在程序中)
nonebot.load_plugin('src.plugins.settings') # 提供一些设置(来自配置文件)
nonebot.load_plugin('src.plugins.util') # 提供一些功能函数，下列的所有插件都依赖util插件，util插件依赖于 tool settings
nonebot.load_plugin('src.plugins.bind')
nonebot.load_plugin('src.plugins.data')
nonebot.load_plugin('src.plugins.help')
nonebot.load_plugin('src.plugins.welcome')
nonebot.load_plugin('src.plugins.cmd')
nonebot.load_plugin('src.plugins.jita') # 依赖 bind data
nonebot.load_plugin('src.plugins.suit') # 依赖 bind data
nonebot.load_plugin('src.plugins.translate') # 依赖 bind data
nonebot.load_plugin('src.plugins.search') # 依赖 data
nonebot.load_plugin('src.plugins.km')
nonebot.load_plugin('src.plugins.kb')
nonebot.load_plugin('src.plugins.checkServer')
nonebot.load_plugin('src.plugins.map') # 依赖 bind
nonebot.load_plugin('src.plugins.price_history') # 依赖 bind data
nonebot.load_plugin('src.plugins.test')

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
