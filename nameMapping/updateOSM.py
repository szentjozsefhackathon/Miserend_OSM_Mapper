import xml.etree.ElementTree as ET
from csv import DictReader


def get_new_value(chosen):
    match item['chosen']:
        case "MR":
            return item['mr_name']
        case "OSM":
            return item['osm_name']
        case '?':
            if item['proposal']:
                return item['proposal']
            else:
                raise Exception("no proposal")
    return Exception("invalid chosen field")

def tag_to_update(country):
    if country == '12':
        return 'name'
    else:
        return 'name:hu'


tree = ET.parse('database/url_miserend.osm')
root = tree.getroot()

for node in root.iter('node'):
    node.set('version', "1.0")
for way in root.iter('way'):
    way.set('version', "1.0")
for relation in root.iter('relation'):
    relation.set('version', "1.0")
print("After version update")
with open("database/nonmatching.csv", 'r') as f:
    dict_reader = DictReader(f, delimiter='#')
    nonmatchingDB = list(dict_reader)

for item in nonmatchingDB:
    osm_type = item['osm_type']

    for nwr in root.iter(osm_type):
        if nwr.get('id') == item['osm_id']:
            try:
                for elem in nwr.iter('tag'):
                    if elem.get('k') == tag_to_update(item['country']):
                        elem.set('v', get_new_value(item['chosen']))
            except Exception as e:
                continue

tree.write('database/nonmatching_output.osm', encoding='utf-8', xml_declaration=True)