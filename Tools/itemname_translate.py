import pandas as pd
import yaml

old_file = open('typeIDs.yaml', 'r', encoding='utf-8')
old_data = yaml.load(old_file.read(), Loader=yaml.FullLoader)
old_file.close()

new_data = []

for k, v in old_data.items() :
    node = { 'id': k, 'en': v['name']['en'] }
    if 'zh' in v['name'] :
        node['zh'] = v['name']['zh']
    new_data.append(node)

out = pd.DataFrame(new_data)
out.to_excel('物品名中英对照表.xlsx', encoding='utf-8', index=False)