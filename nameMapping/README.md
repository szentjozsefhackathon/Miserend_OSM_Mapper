1. Export Miserend DB => templomok.csv
1. Export OSM nodes/ways/relations where miserend tag is present to csv with filtered columns. Overpass turbo query (https://overpass-turbo.eu/):
`[out:csv(::type, ::id, ::lat, ::lon, name, "name:hu", alt_name, "alt_name:hu", old_name, "old_name:hu", "url:miserend"; true; ",")];
nwr["url:miserend"];
out body;` => database/osmDB.csv
1. Export OSM nodes/ways/relations where miserend tag is present to osm format. Overpass turbo query (https://overpass-turbo.eu/):
    `[out:xml];
    nwr["url:miserend"];
    out body;`
Save the output to database/url_miserend.osm
1. Reduce columns o=> id, nev, ismertnev, osmid, osmtype, lat, lon => database/miserendDB.csv
1. execute mergeNames.py (joins the two databases (osmDB, miserendDB) by osm_type and osm_id, then filters the items where the name(:hu) and 'nev' fields does not match) => stdout => save them to database/nonmatching.csv 
1. Manual work: decide the right values. 
   1. Open the nonmatching.csv file in excel
   2. Mark the correct value in the column ‘chosen’ – if miserend holds the correct value enter ‘MR’ if OSM → ‘OSM’. If neither is correct or you cannot decide enter ‘?’. If you have a proposal for a better name add it to the ‘proposal’ column (the ‘?’ still shall be in the ‘chosen’). If there is a ‘?’, but no proposal, the record will be omitted.
1. Save the nonmatching file in cvs format (separator shall be '#')
1. Execute updateOSM.py => will generate database/nonmatching_output.osm
1. Start josm tool
1. Open database/nonmatching_output.osm 
1. File / Upload data, login
1. You are finished the update process. Next step to get rid of 'nev' and 'ismertnev' fields from miserend database.
