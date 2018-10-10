"""
Daniel Siervo <dsiervo@sgc.gov.co>
"""

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.core.event import ResourceIdentifier
from datetime import timedelta
import numpy as np
import os

server_IP = 'http://10.100.100.232'
port_fdsn = "8091"
    

starttime = UTCDateTime("2018 02 25 00 38 07")    

endtime = UTCDateTime("2018 02 25 00 40")

client = Client(server_IP+":"+port_fdsn)

# catalogo de eventos correspondiente al select
cat = client.get_events(starttime=starttime, endtime=endtime)
                        #minlatitude=10, maxlatitude=14,
                        #minlongitude=-82, maxlongitude=-80)

print len(cat)

folder_name = "migracion_prueba_sfiles"
os.system("mkdir %s"%folder_name)
for event in cat:
    try:
        #print event
        time = event.preferred_origin().time - timedelta(hours=0, minutes=2)
        # la forma de onda empieza 2 min antes del sismo
        min_w = time.minute
        event_id = event.resource_id.resource_id.split('/')[2]
        print event_id
        #   "ARC PRV   HHZ CM 00 %s %s%s %s%s %s   300"
        w ="ARC                 %s %s%s %s%s %s   300"%(\
            str(time.year), str(time.month).rjust(2,"0"), str(time.day).rjust(2,"0"),
            str(time.hour).rjust(2,"0"), str(min_w).rjust(2,"0"), str(time.second).rjust(2,"0"))
        #print w
        name = str(time.day).rjust(2,"0")+"-"+str(time.hour).rjust(2,"0")+str(time.minute).rjust(2,"0")+\
        "-"+str(time.second).rjust(2,"0")+"L.S"+str(time.year)+str(time.month).rjust(2,"0")
        event.write(folder_name+"/"+name, format="NORDIC", userid="anls",
                   wavefiles=[w])
        print 'Output file name: ' +  name
    except Exception as e:
        print e
        print name
        continue
