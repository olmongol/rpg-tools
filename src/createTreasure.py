#!/usr/bin/env python
'''
\file createTreasure.py
\package rpg-tools
\brief This little command line tool creates random treasures

Using the MERP/MERS tables to create a random treasure


\date (C) 2016
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
\license GNU v3
'''
import argparse, locale
from rpgtoolbox.rpgtools import dice

lang = locale.getdefaultlocale()[0][:2]
supported = ('de', 'en')
if lang not in supported:
    lang = 'en'
    
helptext = {'description' : {'de' : 'Schatzgenerator',
                             'en' : 'Treasure Generator'},
            'type' : {'de': '1 sehr arm \n2 arm \n3 normal \n4 reich \n5 sehr reich',
                      'en': '1 very poor \n2 poor \n3 normal \4 rich \n5 very rich' 
                      },
            'language' : {'de' : 'Ausgabesprache',
                          'en' : 'Output language'
                          },
            'out' : {'de' : 'Name der Ausgabedatei',
                     'en' : 'Name of the output file'
                     },
            }


parser = argparse.ArgumentParser(description = helptext['description'][lang])
parser.add_argument('-t', '--type', type = int, default = 3, help = helptext['type'][lang])
parser.add_argument('-o', '--out', default = "Treasure.txt", help = helptext['out'][lang])
parser.add_argument('-l', '--language', default = "de", help = helptext['language'][lang])

args = parser.parse_args()
t = args.type
fn = args.out
lang = args.language

roll = dice(100, 1)[0]
nuor = 1

if 31 <= roll <= 55:
    nuor = 2
elif 56 <= roll <= 75:
    nuor = 3
elif 76 <= roll <= 90:
    nuor = 4
elif 90 < roll:
    nuor = 5
    


if __name__ == '__main__':
    print "Hello world"
    
    
