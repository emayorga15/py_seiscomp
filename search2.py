#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb


db = MySQLdb.connect(host="10.100.100.232",    # your host, usually localhost
                     user="consulta",         # your username
                     passwd="consulta",  # your password
                     db="seiscomp3")        # name of the data base
cur = db.cursor()

#cur.execute("show databases")

cur.execute("Select  POEv.publicID, Magnitude.magnitude_value,Origin.time_value, Origin.latitude_value,Origin.longitude_value,\
 Pick.waveformID_stationCode,Pick.waveformID_channelCode,Pick.waveformID_channelCode,\
Pick.phaseHint_code,Pick.phaseHint_used,Pick.evaluationMode,Pick.time_value, Pick.time_value_ms, Pick.filterID\
 from Event AS EvMF left join PublicObject AS POEv ON EvMF._oid = POEv._oid \
left join PublicObject as POOri ON EvMF.preferredOriginID=POOri.publicID \
left join Origin ON POOri._oid=Origin._oid left join PublicObject as POMag on EvMF.preferredMagnitudeID=POMag.publicID \
left join Magnitude ON Magnitude._oid = POMag._oid \
left join Arrival on Arrival._parent_oid=Origin._oid \
left join PublicObject as POOri1 on POOri1.publicID = Arrival.pickID \
left join Pick on Pick._oid= POOri1._oid \
where \
(Magnitude.magnitude_value>1.5 AND Origin.latitude_value between -3 and 5 AND Origin.longitude_value between -75 AND -73 ) \
and Origin.time_value between '2018-08-01 00:00:00' and '2018-09-31 23:15:21'")
i=0
contenido1 = ''

for fila in cur.fetchall():
	contenido1 += str(fila)+'\n'
	i+=1 
	#print fila

archivo1=open('sc_report.out',"w")
archivo1.write(contenido1.decode('iso-8859-1').encode('UTF-8', 'strict'))

cur.close()
db.close()








