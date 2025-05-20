import xml.etree.ElementTree as ET
from csv import DictReader
from xml.etree.ElementTree import Element


def get_new_name_value(chosen, alt):
    match chosen:
        case "MR":
            return item['mr_' + ("alt_" if alt else "") + 'name']
        case "OSM":
            return item['osm_' + ("alt_" if alt else "") + 'name']
        case '?':
            proposal_text = ("alt_" if alt else "") + 'proposal'
            if item[proposal_text]:
                return item[proposal_text]
            else:
                raise Exception("no proposal")
    raise Exception("invalid chosen field")

def get_tag_to_update(country, tag_base_name):
    if country == '12':
        return tag_base_name
    else:
        return tag_base_name + ':hu'

def update_tag(node, country_code, alt: bool):
    key_base_name = 'name' if not alt else "alt_name"
    chosen_text = 'chosen' if not alt else 'alt_chosen'
    tag_to_update = get_tag_to_update(country_code, key_base_name)
    try:
        value_to_update = get_new_name_value(item[chosen_text], alt)
    except (Exception) as e:
        return None
    name_node_to_update = node.find(f"tag[@k='{tag_to_update}']")
    if name_node_to_update is not None:
        name_node_to_update.set('v', value_to_update)
    else:
        new_element = ET.Element("tag")
        new_element.set('k', tag_to_update)
        new_element.set('v', value_to_update)
        nwr.append(new_element)
        #Element.SubElement(nwr, 'tag', dict(k=tag_to_update, v=value_to_update))
    return None

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
            update_tag(nwr, item['country'], False)
            update_tag(nwr, item['country'], True)

tree.write('database/output.osm', encoding='utf-8', xml_declaration=True)
