import xml.etree.ElementTree as ET
from csv import DictReader


def get_new_name_value(chosen, alt):
    match chosen:
        case "MR":
            return item['mr_' + ("" if alt else "alt_") + 'name']
        case "OSM":
            return item['osm_' + ("" if alt else "alt_") + 'name']
        case '?':
            if item[("" if alt else "alt_") + 'proposal']:
                return item['proposal']
            else:
                raise Exception("no proposal")
    raise Exception("invalid chosen field")

def get_tag_to_update(country, tag_base_name):
    if country == '12':
        return tag_base_name
    else:
        return tag_base_name + ':hu'



tree = ET.parse('database/url_miserend.osm')
root = tree.getroot()

for node in root.iter('node'):
    node.set('version', "1.0")
for way in root.iter('way'):
    way.set('version', "1.0")
for relation in root.iter('relation'):
    relation.set('version', "1.0")

with open("database/nonmatching.csv", 'r') as f:
    dict_reader = DictReader(f, delimiter='#')
    nonmatchingDB = list(dict_reader)

for item in nonmatchingDB:
    osm_type = item['osm_type']

    for nwr in root.iter(osm_type):
        if nwr.get('id') == item['osm_id']:
            try:
                for elem in nwr.iter('tag'):
                    if elem.get('k') == get_tag_to_update(item['country'], 'name'):
                        elem.set('v', get_new_name_value(item['chosen'], False))
                    elif elem.get('k') == get_tag_to_update(item['country'], 'alt_name'):
                        elem.set('v', get_new_name_value(item['alt_chosen'], True))
            except Exception as e:
                continue

tree.write('database/output.osm', encoding='utf-8', xml_declaration=True)
