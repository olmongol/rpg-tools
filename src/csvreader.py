#!/usr/bin/env python

import csv
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import sys

__pname__ = "csvreader"

inputfile = "test.cvs"
outputfile = "out.cvs"


parser = ArgumentParser(prog = __pname__,
                      formatter_class = RawDescriptionHelpFormatter,
                      description = "CSV READER")
parser.add_argument("-i", "--inputfile", help = "input file (CSV)", type = str)
parser.add_argument("-o", "--outputfile", help = "output file (CSV)", type = str)

parser.add_argument("-a","--avoidfile", help = "expressions to avoid in output (CSV)", type = str)

args = parser.parse_args()

fname="simple.csv"
inputfile = args.inputfile

with open(fname) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print type(row)
        for key in row.keys():
            print(key,row[key])
        if "CVE" in row.keys():
            if (row['Risk'] != 'None') and (row['Risk'] != 'Low'):
                for key in row.keys():
                    print(key,row[key])
