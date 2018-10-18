python multi_picks.py $1
mkdir picks
mv pick*xml picks
python merge_xml_picks.py
scautoloc -u playback --ep picks_final.xml -d mysql://sysop:sysop@localhost/seiscomp3 --debug > origins2.xml
scanloc -u playback --ep origins2.xml -d mysql://sysop:sysop@localhost/seiscomp3 --debug > origins.xml
scamp -u playback --ep origins.xml -I $1 -d mysql://sysop:sysop@localhost/seiscomp3 --debug > amp.xml
scmag -u playback --ep amp.xml -d mysql://sysop:sysop@localhost/seiscomp3 --debug > mag.xml
scevent -u playback --ep mag.xml -d mysql://sysop:sysop@localhost/seiscomp3 --debug > events.xml
#scdb -i events.xml -d mysql://sysop:sysop@localhost/seiscomp3
