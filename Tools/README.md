## `yaml_tool_*.py`

目录中所需的 `typeIDs.yaml` 为

<https://developers.eveonline.com/resource>

中 `sde-TRANQUILITY.zip` 解压后的 `\sde\fsd\typeIDs.yaml`

把 `typeIDs.yaml` 放到 `yaml_tool.py` 同目录下，并在此目录中运行：

```shell
python3 yaml_tool_zh.py
```

得到 `ID.yaml` 文件，把文件内容备份，再在相同目录运行：

```shell
x 1python3 yaml_tool_en.py
```

得到 `ID.yaml` 文件，把新文件的内容复制粘贴到之前得到的文件最后！再把合成的文件改名为 `ID.yaml` ，把 `ID.yaml` 文件放到 `EVEBot\src\plugins\data` 目录下。

## `pic_resize.py`

使用前需要安装 python 包

```shell
pip3 install pillow
```

把 ``pic_resize.py` 移动到  `EVEBot\src\plugins\tool\icon` 目录，如果没有 `icon` 目录请阅读 `EVEBot\src\plugins\tool\README.md`

在 `icon` 目录中运行：

```shell
python3 pic_resize.py
```

## `itemname_translate.py`

使用前需要安装 python 包：

```shell
pip3 install pandas openpyxl
```

解析 `typeIDs.yaml` 文件，导出到 `物品名中英对照表.xlsx` Excel 表格文件

因为数据量庞大，所以执行时间很长，需要5分钟左右

