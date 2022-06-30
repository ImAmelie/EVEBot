import yaml

old_file = open('typeIDs.yaml', 'r', encoding='utf-8')
old_data = yaml.load(old_file.read(), Loader=yaml.FullLoader)
old_file.close()

new_data = {}

for k, v in old_data.items() :
    if 'factionID' in v :
        v.pop('factionID')
    if 'graphicID' in v :
        v.pop('graphicID')
    if 'iconID' in v :
        v.pop('iconID')
    if 'variationParentTypeID' in v :
        v.pop('variationParentTypeID')
    if 'traits' in v :
        v.pop('traits')
    if 'masteries' in v :
        v.pop('masteries')
    if 'capacity' in v :
        v.pop('capacity')
    if 'metaGroupID' in v :
        v.pop('metaGroupID')
    # if 'marketGroupID' in v :
        # v.pop('marketGroupID')
    if 'basePrice' in v :
        v.pop('basePrice')
    if 'raceID' in v :
        v.pop('raceID')
    if 'sofFactionName' in v :
        v.pop('sofFactionName')
    if 'soundID' in v :
        v.pop('soundID')
    if 'radius' in v :
        v.pop('radius')
    if 'volume' in v :
        v.pop('volume')
    if 'description' in v :
        v.pop('description')
    if 'groupID' in v :
        v.pop('groupID')
    if 'mass' in v :
        v.pop('mass')
    if 'portionSize' in v :
        v.pop('portionSize')
    if 'published' in v :
        v.pop('published')
    if 'de' in v['name'] :
        v['name'].pop('de')
    if 'fr' in v['name'] :
        v['name'].pop('fr')
    if 'ja' in v['name'] :
        v['name'].pop('ja')
    if 'ru' in v['name'] :
        v['name'].pop('ru')
    if 'es' in v['name'] :
        v['name'].pop('es')
    if 'it' in v['name'] :
        v['name'].pop('it')
    new_data[k] = v

del_items = []

for k, v in new_data.items() :
    if 'zh' in v['name'] :
        del_items.append(k)

for k in del_items :
    del new_data[k]

new_data = dict(sorted(new_data.items(), key=lambda i: (len(i[1]['name']['en']), i[1]['name']['en'])))

new_file = open('ID.yaml', 'w', encoding='utf-8')
yaml.dump(new_data, new_file, allow_unicode=True, sort_keys=False)
new_file.close()
