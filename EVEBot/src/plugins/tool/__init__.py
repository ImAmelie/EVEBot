import os
import yaml
from nonebot.plugin import export

tool=export()

'''
# tool.data
path = os.path.abspath(os.path.dirname(__file__))
file = open(path + '/' + 'ID.yaml', 'r', encoding='utf-8')
tool.data = yaml.load(file.read(), Loader=yaml.FullLoader)
file.close()
'''

tool.icon_path = 'file:///' + os.path.abspath(os.path.dirname(__file__)) + '/icon/'

tool.alliance_id = 99003581
tool.alliance_ids = [ 99003581, 99006406 ] # 关注的联盟ID
tool.corporationID = 98185110
tool.corporationIDs = [ 98185110, 98633272 ] # 关注的公司ID
tool.group_id = 12345 # QQ群ID
tool.group_ids = [ 12345, 67890 ] # QQ群ID
