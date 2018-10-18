#!/usr/bin/env python

import sys, seiscomp3.Client, seiscomp3.DataModel

class InvApp(seiscomp3.Client.Application):
    def __init__(self, argc, argv):
        seiscomp3.Client.Application.__init__(self, argc, argv)
        self.setMessagingEnabled(False)
        self.setDatabaseEnabled(True, True)
        self.setLoggingToStdErr(True)

    def validateParameters(self):
        try:
            if seiscomp3.Client.Application.validateParameters(self) == False:
                return False

            return True

        except:
            info = traceback.format_exception(*sys.exc_info())
            for i in info: sys.stderr.write(i)
            sys.exit(-1)

    def run(self):
		now = seiscomp3.Core.Time.GMT()

		lines = []
		dbr = seiscomp3.DataModel.DatabaseReader(self.database())
		inv = seiscomp3.DataModel.Inventory()
		dbr.loadNetworks(inv)
		nnet = inv.networkCount()
		for inet in xrange(nnet):
			net = inv.network(inet)
			dbr.load(net);
			nsta = net.stationCount()
			for ista in xrange(nsta):
				sta = net.station(ista)
				nloc = sta.sensorLocationCount()
				for iloc in xrange(nloc):
					loc = sta.sensorLocation(iloc)
					line = "%-2s, %-5s, %9.4f, %9.4f, %6.1f, %s, %-5s" % (net.code(),
					sta.code(), sta.latitude(), sta.longitude(),
					sta.elevation(), loc.code(), sta.country()) #sta.archiveNetworkCode(), sta.affiliation()
					lines.append(line)

		lines.sort()
		f = open("stations.csv", "w")
		for line in lines:
			print >>f, line
		
		f.close()
		return True


def main():
    app = InvApp(len(sys.argv), sys.argv)
    return app()

# python station-coordinates.py -d mysql://sysop:sysop@10.100.100.232/seiscomp3
if __name__ == "__main__":
    sys.exit(main())
