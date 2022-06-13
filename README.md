<div align="center">
  <h1>EVEBot</h1>
  <p>✨ EVE Online QQ机器人 ✨</p>
  <p>
    <a href="https://raw.githubusercontent.com/ImAmelie/EVEBot/master/LICENSE">
      <img alt="license" src="https://img.shields.io/github/license/ImAmelie/EVEBot?style=flat-square">
    </a>
  </p>
</div>

我并不会 Python ，赶鸭子上架才写的这个 Bot ，所以看了代码不要高血压，并在这里感谢提供帮助和指点的人！

感谢开源框架 [NoneBo2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ，没有你们就没有这个 Bot 。

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

这里以 CentOS 7 为例

先安装 1.1.1 版本的 openssl ，过低版本导致 python3 使用不了 ssl 模块

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
./configure
make && make install

# 不要创建软链接，因为yum需要python2
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

# 不要创建软链接，因为yum需要python2
```

安装后自行更新 pip3 和更换 pip3 的软件源

```shell
python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

安装 NoneBot ：

```shell
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

**建议**把 `icon` 文件夹下所有图片都修改为 `128*128px` ，批量改图片大小的方法请自行 Google

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

### NoneBot2

```shell
screen -S bot
```

进入 `EVEBot` 目录：

```shell
python3 bot.py
```

## BUG

`.suit` 和 `.search` 命令返回过长时，会被截断。

建议关闭这两个功能，因为有被腾讯风控的风险。

