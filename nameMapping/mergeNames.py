from csv import DictReader
import re

with open("database/miserendDB.csv", 'r') as f:
    dict_reader = DictReader(f)
    miserendDB = list(dict_reader)

with open("database/osmDB.csv", 'r') as f:
    dict_reader = DictReader(f)
    osmDB = list(dict_reader)

counter = 0
print("mr_id#osm_type#osm_id#mr_name#mr_alt_name#osm_name#osm_alt_name#country#chosen#proposal")
for miserendItem in miserendDB:
    miserendId = miserendItem['id']
    for osmItem in osmDB:
        try:
            osmMiserendId = osmItem['url:miserend']
            osmMiserendId = re.search("^.*[=\/](\d{1,4})$", osmMiserendId)[1]
        except:
            continue #skip empty lines
        if osmMiserendId == miserendId:
            if miserendItem['orszag'] == '12':
                if osmItem['name'] != miserendItem['nev']:
                    counter+=1
                    print(f"{miserendItem['id']}#{osmItem['@type']}#{osmItem['@id']}#{miserendItem['nev']}#miserend['ismertnev']#{osmItem['name']}#{osmItem['alt_name']}#{miserendItem['orszag']}")
            else:
                if osmItem['name:hu'] != miserendItem['nev']:
                    counter+=1
                    print(f"{miserendItem['id']}#{osmItem['@type']}#{osmItem['@id']}#{miserendItem['nev']}#miserend['ismertnev']#{osmItem['name:hu']}#{osmItem['alt_name:hu']}#{miserendItem['orszag']}")
