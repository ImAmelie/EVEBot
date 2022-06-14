<div align="center">
  <h1>EVEBot</h1>
  <p>✨ EVE Online QQ机器人 ✨</p>
  <p>
    <a href="https://raw.githubusercontent.com/ImAmelie/EVEBot/master/LICENSE">
      <img alt="license" src="https://img.shields.io/github/license/ImAmelie/EVEBot?style=flat-square">
    </a>
  </p>
</div>

我并不会 Python ，赶鸭子上架才写的这个 Bot ，所以看了代码不要高血压，并在这里感谢所有提供帮助和指点的人！

感谢开源框架 [NoneBot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ，没有你们就没有这个 Bot 。

## 功能

```
### 基本命令
# 显示帮助
.help / .帮助
# 查攻略（攻略文件需提前编写）
.a / .攻略 <关键字>
# 列出匹配关键字的所有游戏内物品
.search / .搜索 <关键字>
# 吉他物价查询
.jita / .jt / .吉他 <物品名>
.jita / .jt / .吉他 <物品名>*<数量>
# 查询物品所属物品组中的所有物品价格
.suit <物品名>
# 得到匹配关键字物品名的中英文翻译
.tr / .tran / .翻译 <关键字>
# 从zkillboard网获得人物信息
.kb / .zkb <name>

### 管理员命令
# 绑定物品的别名，比如绑定MTU到移动式牵引装置，方便查价
.bind <别名>,<物品名>
# 解绑别名
.unbind <别名>
# 设置最低损失ISK，以方便km播报过滤价值过低的km
.limit <数字>
# 热加载攻略文件（EVEBot\src\plugins\cmd\cmd.json），文件更改时重新加载，所属命令(.攻略 <关键字>)
.load
```

以上只列出主要命令，要查询所有命令，请运行机器人并说 `.help` ，或者浏览所有插件（大部分杂项命令都在 `help` 插件中引入）

命令外功能：

- km播报
- 每日维护后服务器上线自动提醒
- 新人入群欢迎

## Linux 部署指南

### go-cqhttp

打开 `go-cqhttp/config.yml` ：

在 `account/uin` 中填入机器人QQ号，登录时会显示扫码登陆（提示：终端开大一点，防止二维码显示不全）

在 `servers/ws-reverse/universal` 中填入 `ws://127.0.0.1:8808/onebot/v11/ws/`

在 `go-cqhttp` 目录中执行：

```shell
chmod +x go-cqhttp
```

### NoneBot2

安装 NoneBot2 前需要在服务器上安装 openssl 和 python3

<details>
<summary>以 CentOS 7 为例，安装 openssl 和 python3</summary>

先安装 1.1.1 版本的 openssl ，过低版本导致 python3 使用不了 ssl 模块

不要安装 3.0 以上版本

<https://www.openssl.org/source/>

```shell
tar -zxf openssl-1.1.1o.tar.gz
cd openssl-1.1.1o
./config --prefix=/opt/openssl-1.1.1o --openssldir=/opt/openssl-1.1.1o/openssl
make
make install

echo "/opt/openssl-1.1.1o/lib" >> /etc/ld.so.conf
ldconfig -v
```

在你的 Linux 发行版中安装 python3 的最新版本

<https://www.python.org/downloads/>

```shell
# yum安装的python3版本过低，故不使用yum安装

yum groupinstall -y "Development tools"
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum install -y libffi-devel

wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz
tar -zxf Python-3.10.5.tgz
cd Python-3.10.5
```

修改 `Modules/Setup` ，取消以下内容的注释：

```
OPENSSL=/opt/openssl-1.1.1o
_ssl _ssl.c \
    -I$(OPENSSL)/include -L$(OPENSSL)/lib \
    -lssl -lcrypto
```

在 `Python-3.10.5` 中运行：

```shell
./configure
make && make install

# 不要创建python3到python的软链接，因为yum软件依赖python2
```

安装后更新 pip3 和更换 pip3 的软件源

```shell
python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```



</details>



安装 NoneBot2 ：

```shell
# pip3是python3的包管理工具，安装python3自带pip3
pip3 install requests
pip3 install httpx
pip3 install websockets
pip3 install nonebot2
pip3 install nonebot-adapter-onebot
pip3 install nonebot-adapter-cqhttp
pip3 install nonebot_plugin_apscheduler
```

修改 `\EVEBot\EVEBot\.env.prod` 中的 `SUPERUSERS` ，此为QQ机器人管理员账户

修改 `\EVEBot\EVEBot\src\plugins\tool\__init__.py` 中的监听群号和监听联盟ID

### `EVEBot\src\plugins\tool\icon` 文件夹不存在的问题

`icon` 文件夹为：

<https://developers.eveonline.com/resource>

中的 `Invasion_*_Renders.zip` 文件

解压该文件，把 `Renders` 重命名为 `icon`

**建议**把 `icon` 文件夹下所有图片都修改为 `128*128px` ，修改方法在 `Tools` 目录 [README.md](Tools/README.md) 中，或自行 Google 修改文件尺寸的方法，注：不修改文件尺寸也没问题，但是发送的带图聊天消息可能**看**起来很大

### Tools 工具目录

#### 获取 `ID.yaml` 文件

目录中所需的 `typeIDs.yaml` 为

<https://developers.eveonline.com/resource>

中 `sde-TRANQUILITY.zip` 解压后的 `\sde\fsd\typeIDs.yaml`

把 `typeIDs.yaml` 放到 `yaml_tool.py` 同目录下，并在此目录中运行：

```shell
python3 yaml_tool.py
```

得到 `ID.yaml` 文件，把 `ID.yaml` 文件放到 `EVEBot\src\plugins\data` 目录下。

## Linux 运行

建议使用 screen 软件分屏操作：

```shell
yum install -y screen
```

```shell
# screen 常用命令
screen -S <会话名> # 创建一个叫<会话名>的会话
# 离开会话 Ctrl+a d # 依次按 a d
screen -ls # 列出当前存在的会话
screen -r <会话ID/会话名> # 连接到<会话ID/会话名>
screen -S <会话ID/会话名> -X quit # 删除会话
```

### go-cqhttp

```shell
screen -S cq
```

进入 `go-cqhttp` 目录：

```shell
chmod +x go-cqhttp
./go-cqhttp
```

按 `Ctrl+a d` 切换到主界面

关闭：`screen -r cq` 切换回会话后，按 `Ctrl+c` 可以关闭程序

### NoneBot2

```shell
screen -S bot
```

进入 `EVEBot` 目录：

```shell
python3 bot.py
```

按 `Ctrl+a d` 切换到主界面

关闭：`screen -r bot` 切换回会话后，按 `Ctrl+c` 可以关闭程序

如果按 `Ctrl+c` 后没反应，可以根据画面中类似于以下的提示，`Ctrl+a d` 切回主界面执行 `kill -9 23333` 命令强行终止该进程

```
01-01 01:00:00 [INFO] uvicorn | Finished server process [23333]
```

## BUG



## 性能

启动速度慢是因为 `data` 插件要载入存储所有物品名的数据文件，吉他查价（`.jita`）和 `.search` 命令都依赖这个插件，如果关闭，请注释 `EVEBot\bot.py` 中的 `nonebot.load_plugin('src.plugins.data')` 并注释掉依赖于这个插件的所有插件。

关闭 NoneBot2 用时很长也与该插件的开启有关。

`data` 插件会占用约 390 MB 内存，其他插件占用约等于无。

