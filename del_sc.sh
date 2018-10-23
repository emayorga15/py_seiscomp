#!/bin/bash

scxmldump -fPAMF -E $1 -o $1.xml -d mysql://sysop:sysop@10.100.100.$2/seiscomp3
scdispatch -i $1.xml -O remove
rm -f $1.xml
