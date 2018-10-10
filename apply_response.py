#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
v(1) 2018-10-09
autor: Daniel Siervo
e-mail: dsiervo@sgc.gov.co

Requiere archivos instrumentales en formato xml-seed.
Si se tiene dataless puede usarse el script de obspy obspy-dataless2xseed
"""

from obspy import read, read_inventory
from obspy.io.xseed import Parser
import pylab as pl
import click
import os

@click.command()
@click.option('-w', "--waveform", required=True, prompt=True, help='Waveform file name')
@click.option('-d', "--dataless", required=True, prompt=True, help='Dataless file name')
@click.option('-u', "--units", default="VEL", help='units to convert. Can be: DIS, VEL, ACC')
@click.option('-p', "--plot", default=False, type=bool, help='Define if waveform is plotted')
@click.option('-f', "--filt", default=True, type=bool, help='Define if waveform is filtered')

def main(waveform, dataless, units, plot, filt):
    # if it is a file
    if os.path.isfile(waveform):
        apply_response(waveform, dataless, units, plot, filt)
    # if it is not
    else:
        print "Creando carpeta: %s_files"%units
        os.system("mkdir %s_files"%units)
        for f in os.listdir(waveform):
            apply_response(f, dataless, units, plot, filt, path="%s_files/"%units)


def apply_response(foname, dtless_name, units="VEL", plot=False, filt=True, path="./"):
    """Create xml seed response file and apply response from dataless
    :type foname: str
    :param foname: String containing a waveform file name
    :type dtless_name: str
    :param dtless_name: String containg a dataless file name
    :type units: str
    :param units: String containg units. Can be: DIS, VEL, ACC
    :type plot: boolean
    :param plot: Define if waveform is plotted
    :type filt: boolean
    :param filt: Define if waveform is filtered
    """
    print "Opciones seleccionadas fueron:"
    print foname, dtless_name, units, plot, filt, path
    st = read(foname)
    parser = Parser(dtless_name)
    xml_name = dtless_name+".xml"
    parser.write_xseed(xml_name)
    inv = read_inventory(xml_name)

    pre_filt = (0.005, 0.006, 30.0, 35.0)
    if not filt: pre_filt = None

    print "Pasando de cuentas a: "+units
    st.remove_response(inventory=inv, output=units, pre_filt=pre_filt, plot=plot)
    if plot: pl.show()

    st.write(path+foname+"_"+units, format="mseed")
    print "\n\n\tArchivo de salida: "+foname+"_"+units+"\n"

if __name__ == '__main__':
    main()


