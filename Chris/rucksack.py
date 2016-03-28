#!/usr/bin/env python
'''
\file rucksack.py
\brief Rucksackverwaltung

Rucksackverwaltung mit Shopsystem

\date (C) 2015
\author Christian Wunderlich
\email cw@almandor.de

\todo Modul: alles

'''
'''
Erst mal zum rumspielen
'''

import csv

with open('./Data/shop.csv', 'r') as csvfile:
    shopdir = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in shopdir:
        print(', '.join(row))
