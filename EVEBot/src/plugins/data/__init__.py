import os
import yaml
from nonebot.plugin import export

data = export()

path = os.path.abspath(os.path.dirname(__file__))
file = open(path + '/' + 'ID.yaml', 'r', encoding='utf-8')
data.data = yaml.load(file.read(), Loader=yaml.FullLoader)
file.close()
