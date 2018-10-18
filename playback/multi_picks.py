import os, multiprocessing, sys
fo = sys.argv[1]

process = ["pick_b_Z -u playback -I %s -d mysql://sysop:sysop@localhost/seiscomp3 --playback --ep --debug>picks.xml"%fo,
"pick_b_N -u playback -I %s -d mysql://sysop:sysop@localhost/seiscomp3 --playback --ep --debug>picks1.xml"%fo,
"pick_b_E -u playback -I %s -d mysql://sysop:sysop@localhost/seiscomp3 --playback --ep --debug>picks2.xml"%fo,
"pick_s_Z -u playback -I %s -d mysql://sysop:sysop@localhost/seiscomp3 --playback --ep --debug>picks3.xml"%fo,
"pick_s_N -u playback -I %s -d mysql://sysop:sysop@localhost/seiscomp3 --playback --ep --debug>picks4.xml"%fo,
"pick_s_E -u playback -I %s -d mysql://sysop:sysop@localhost/seiscomp3 --playback --ep --debug>picks5.xml"%fo]


jobs = []
for p in process:
    print p
    q = multiprocessing.Process(target=os.system, args=(p,))
    jobs.append(q)
    print q


for j in jobs:
    j.start()
for j in jobs:
    j.join()
