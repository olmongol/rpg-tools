#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
\package rpgtoolbox.lang
\file lang.py

\brief multi language support module for rpg-tools 

Here are all the things implemented that are needed for the switching of 
language in the rpg-tools. So this file consists mainly 
of dictionary structures.
Currently supported languages are:
\li English
\li Deutsch

\attention At the moment just Linux/Unix is supported!

\author Marcus Schwamberger
\email marcus@lederzeug.de
\date (c) 2015-2017
\version 0.4
\license GNU V3.0

\todo clean up the code!!!
'''
## \var supportedrpg
# Supported RPG systems
supportedrpg = {'de' : ("MERS", "RoleMaster"),
                'en' : ('MERP', 'RoleMaster')
                }

## \var screenmesg
#This holds general screen messages.
screenmesg = {'welcome'     : {'de' : "Willkommen bei den RPG-Tools",
                               'en' : "Welcome at the RPG tools",
                               },
              'wrongver'    : {'de' : 'Falsche Python-Version!!',
                               'en' : 'Wrong Python version!!',
                               },
              'ossupport'   : {'de' : 'Das Betriebsystem wird unterst\xc3\xbctzt.',
                               'en' : 'The operating system is supported.',
                               },
              'osnosupport' : {'de' : 'Das Betriebssystem wird leider' \
                                      'nicht unterst\xc3\xbctzt',
                               'en' : ' Sorry, OS not supported!',
                               },
              'file_saved'  : {'de' : 'Datei wurde gespeichert.',
                               'en' : 'File was saved.'},
              'no_data_sv'  : {'de' : 'Es gibt leider noch keine Daten zu speichern...',
                               'en' : 'There are no data to save...'
                               },
              'loop'       : {'de' : 'Es wurden folgende Schleifen in der '\
                                      'Konfiguration gefunden. Diese bitte '\
                                      'erst einmal beseitigen, damit ge'\
                                      'speichert werden kann!',
                               'en' : 'Found the following loops in your '\
                                      'configuration. Please remove them '\
                                      'first that the structure can be stored!'
                               },
              }

## \var txtbutton
#This holds the texts written on buttons.
txtbutton = {'but_ok'   : {'de' : 'OK',
                           'en' : 'ok',
                           },
             'but_sav'  : {'de' : 'Speichern',
                           'en' : 'save',
                           },
             'but_quit' : {'de' : 'Beenden',
                          'en'  : 'quit',
                          },
             'but_clos' : {'de' : 'Schliessen',
                           'en' : 'close',
                           },
             'but_add'  : {'de' : 'hinzuf\xc3\xbcgen',
                           'en' : 'add',
                           },
             'but_del'  : {'de' : 'entfernen',
                           'en' : 'delete',
                           },
             'but_right': {'de' : '--->>',
                           'en' : '--->>',
                           },
             'but_left' : {'de' : '<<---',
                           'en' : '<<---',
                           },
             'but_next' :{'de' : 'Weiter',
                          'en' : 'next',
                          },
             'but_back' : {'de' : 'Zur\xc3\xbcck',
                           'en' : 'back',
                           },
             'but_prev' : {'de' : 'Zur\xc3\xbcck',
                           'en' : 'back'
                           },
             'but_refr' : {'de' : 'zeigen/auffrischen',
                           'en' : 'show/refresh'
                           },
             'but_take' : {'de' : '\xc3\x9cbernehmen',
                           'en' : 'take over'
                           },
             'but_roll' :{'de' : 'W\xc3\xbcrfeln',
                          'en' : 'roll dice'
                          },
             'but_calc' :{'de' : "Berechnen",
                          'en' : 'calculate'
                          },
             }

## \var txtmenu
#This holds the texts of the main menu bar mixed up with button labels
#\todo it has to be clearly seperated menu and buttons
txtmenu = {'menu_help'     : {'de' : 'Hilfe',
                              'en' : 'Help',
                              },
           'help'          : {'de' : 'Hilfe',
                              'en' : 'Help',
                              },
           'hlp_about'     : {'de' : '\xc3\xbcber',
                              'en' : 'About',
                              },
           'hlp_first'     : {'de' : 'Erste Schritte',
                              'en' : 'First Steps',
                              },
           'hlp_context'   : {'de' : 'Kontexthilfe',
                              'en' : 'Context Help',
                              },
           'but_ok'        : {'de' : 'OK',
                              'en' : 'OK',
                              },
           'but_quit'      : {'de' : 'Schliessen',
                              'en' : 'Quit',
                              },
           'menu_edit'     : {'de' : 'Bearbeiten',
                              'en' : 'Edit',
                              },
           'menu_file'     : {'de' : 'Datei',
                              'en' : 'File',
                              },
           'menu_opt'      : {'de' : 'Optionen',
                              'en' : 'Options',
                              },
           'menu_gm'       : {'de' : 'Spieleiterwerkzeug',
                              'en' : "Gamemaster's Tools"
                              },
           'menu_grp'      : {'de' : 'Charaktergruppe',
                              'en' : 'Character Party' 
                              },
          }

## \var submenu
#This holds the texts of the submenu cascades.
submenu = {'file' :{'de':{'open'  : 'Datei \xc3\xb6ffnen',
                          'close' : 'Datei schliessen',
                          'new'   : 'Neue Datei',
                          'save'  : 'Datei speichern',
                          'sv_as' : 'Datei speichern unter...',
                          'quit'  : 'Beenden',
                          'export' : 'Exportieren',
                          'new_char': 'Neuer Charakter',
                          'new_grp' : 'Neue Charaktergruppe'
                          },
                    'en':{'open'  : 'Open file',
                          'close' : 'Close file',
                          'new'   : 'New file',
                          'save'  : 'Save file',
                          'sv_as' : 'Save as',
                          'quit'  : 'Quit',
                          'export' : 'Export',
                          'new_char' : "New character",
                          'new_grp' : "New characer party"
                          },
                    },
           'opts'  :{'de' : {'lang' : 'Einstellungen',
                             },
                     'en' : {'lang' : 'Preferences',
                             }
                     },
           'help'  :{'de' : {'about' : '\xc3\x9cber rpg-tools',
                             'page'  : '\xc3\x9cber diese Seite',
                             'win'   : '\xc3\x9cber dieses Fenster',
                             'global' : 'Handbuch',
                             },
                     'en' : {'about' : 'About rpg-tools',
                             'page'  : 'About this page',
                             'win'   : 'About this window',
                             'global' : 'Handbook',
                             },
                     },
           'edit'  : {'de' : {'ed_char'  : 'Charakter bearbeiten/steigern',
                              'ed_grp'   : 'Gruppe bearbeiten',
                              'ed_fight' : 'Kampf-EPs',
                              'ed_other' : 'EPs Zauber,Reisen, Man\xc3\xb6ver',
                              'ed_indiv' : 'Ideen-EPs',
                              'ed_calc'  : 'Zusammenrechnen',
                              'ed_sim'   : 'Kampfsimulation (EP)',
                              'ed_equip' : 'Ausr\xc3\x9cstung verwalten'
                              },
                      'en'  :{'ed_char'  : 'Edit/improve Character',
                              'ed_grp'   : 'Edit Group',
                              'ed_fight' : 'Fight EPs',
                              'ed_other' : 'EPs for Spells,Travel,Maneuver',
                              'ed_indiv' : 'EPs for ideas',
                              'ed_calc'  : 'Calculate all',
                              'ed_sim'   : 'EPs for fight simulation',
                              'ed_equip' : 'Edit equipment'
                               },
            
                      },
           'items' : {'de' : {'treasure': "Schatz generieren",
                              'magical' : "Magische Gegenst\xc3\xa4nde erzeugen",
                              'itemgen'    : " [Gegenstandsliste wird auf knopfdruck erzeugt] ",
                              'magicgen'    : " [Magischer Gegenstand wird auf Knopfdruck erzeugt] ",
                              },
                      'en' : {'treasure': "Create treasure",
                              'magical' : "Create magic items",
                              'itemgen'    : " [List of items will be generated when button is pressed] ",
                              'magicgen'    : " [Magic item will be generated when button is pressed] ",
                              },
                      },
           'group' : {'de' : {'add/rem' : "Charakter hinzuf\xc3\xbcgen/entfernen",
                              'new'     : "Neue Charaktergruppe",
                              'gmview'  : "Spielleiter\xc3\xbcbersicht",
                              },
                      'en' : {'add/rem' : "Add/remove characters",
                              'new'     : "New party",
                              'gmview'  : "Gamemaster's overview",
                              },
                      }
           }

## \var txtwin
#This holds the content of selectable  file types while open/close files.
txtwin = {'all_files' : {'de' : ("alle Dateien", '.*'),
                         'en' : ("all files", '.*'),
                         },
         'exp_files'  : {'de' : ('EXP-Dateien', '.exp'),
                         'en' : ('EXP files', '.exp'),
                         },
          'txt_files' : {'de' : ('Text-Dateien', '.txt'),
                         'en' : ('Text files', '.txt')
                         },
          'csv_files' : {'de' : ('CSV Dateien', '.csv'),
                         'en' : ('CSV files', 'csv')
                         },
          'json_files': {'de' : ('Charakter Dateien', '.json'),
                         'en' : ('Character files', '.json')
                         },
          'grp_files' : {'de' : ('Gruppen Dateien', '.grp'),
                         'en' : ('Group files', '.grp')
                         }
          }

## \var processing
#some processing messages
processing = {'saved' : {'de' : 'Gespeichert...',
                         'en' : 'Saved...',
                         },
              'exported' : {'de' : 'Export abgeschlossen.',
                            'en' : 'Export finished.'
                            }
            }

## \var shortcut
#language shortcuts / supported languages
shortcut = {'de' : 'Deutsch',
            'en' : 'English',
            }

##\var wintitle
#these are the titles of the windows
wintitle = {'opt_lang' : {'de' : 'Spracheinstellungen',
                          'en' : 'Language Settings',
                          },
            'main'     : {'de' : 'Rollenspiel Werkzeuge',
                          'en' : 'RPG Tools',
                          },
            'edit'     : {'de' : 'Charakter-Editor',
                          'en' : 'Character Editor',
                          },
            'backpack' : {'de' : 'Rucksack',
                          'en' : 'Backpack'
                          },
            'item_store' : {'de' : 'Kramladen',
                            'en' : 'Item Store'
                            },
            'calc_exp' : {'de' : 'EP Rechner',
                          'en' : 'EP Calculator'
                          },
            'rm_charg' : {'de' : 'RM Charaktergenerator',
                          'en' : 'RM Character Generator'
                          },
            'mers_charg' : {'de' : 'MERS Charaktergenerator',
                            'en' : 'MERP Character Generator'
                           },
            'rm_create' : {'de' : "RM Charaktergenerierung",
                           'en' : 'RM Character Builder'
                           },
            }

## \var labels
#labels for window elements (labels, listboxes etc.)
#\todo clean up!!
labels = {'cfg_path' : {'de' : 'Speicherpfad f\xc3\xbcr die Konfigurationsdatei',
                        'en' : 'Path where to store the config file',
                        },
          'log_path' : {'de' : 'Pfad zu den Log-Dateien',
                        'en' : 'Path of the log files',
                        },
          'db_type'  : {'de' : 'Datenbanktyp',
                         'en' : 'Type of data base',
                         },
          'db_host'  : {'de' : 'DB Host',
                        'en' : 'DB host',
                        },
          'db_port'  : {'de' : 'DB Port',
                        'en' : 'DB port'
                        },
          'db_name'  : {'de' : 'DB Benutzer',
                        'en' : 'DB user'
                        },
          'db_pass'  : {'de' : 'DB Passwort',
                        'en' : 'DB password'
                        },
          'add_elem' : {'de' :'Zus\xc3\xa4tzliche Elemente (Komma getrennte Liste)',
                       'en' : 'Additional elements (comma separated list)',
                       },
          'connect'  : {'de' : 'Verbinden',
                       'en' : 'Connect',
                       },
          'update'   : {'de' : 'aktualisieren',
                       'en' : 'Update',
                       },
          'cancel'   : {'de' : 'Abbrechen',
                        'en' : 'Cancel',
                      },
          'preview' : {'de' : 'Vorschau',
                       'en' : 'Preview',
                       },
          }


##\var errmsg
#Error messages for all opportunities 
errmsg = {'no_file' : {'de' : 'Datei existiert nicht!',
                       'en' : 'File does not exists!',
                       },
          'wrong_type' :{'de' : 'Falscher Dateityp!',
                         'en' : 'Wrong file type!'
                         },
          'no_name' : {'de' : 'Kein Dateiname angegeben!',
                       'en' : 'No file name given!',
                       },
          'no_read' : {'de' : 'Datei ist nicht lesbar!',
                       'en' : 'File is not readable!',
                       },
          'no_data' : {'de' : 'Es wurden keine Daten eingelesen!',
                       'en' : 'There were no data read!'
                       },
          'wr_handle' : {'de' : 'Falsche Dateizugriffsmethode',
                         'en' : 'Wrong file handler',
                         },
          'wr_cfg' : {'de' : 'Folgende falsche Parameter gefunden:',
                      'en' : 'Found the following wrong parameters:',
                      },
          'mis_cfg' : {'de' : 'Folgende Parameter sind noch nicht konfiguriert:',
                       'en' : 'The following parameters are not configured yet:'
                       },
          'fine_cfg' : {'de' : 'Konfiguration ist sauber! :-)',
                        'en' : 'Configuration is clean! :-)',
                        },
          'ld_struc' : {'de' : 'Die zugeh\xc3\xb6rige Struktur-Datei muss\n'\
                               'erst mal geladen sein!',
                        'en' : 'The belonging stucture file has to be\n'\
                                'loaded first!',
                        },
          'wrong_stat' : {'de' : 'Falscher Attributswert: \n\n'\
                                 'er muss mindestens 20 bei normalen und 90 bei \n'\
                                 'prim\xc3\xa4ren Attributen (+) betragen!',
                          'en' : 'Wrong attibute value:\n\n'\
                                 'it must have a min of 20 concerning standard and\n'\
                                 '90 concerning primary attributes (+)!'
                          },
          'too_much_stats':{'de' : 'Die vorhandenen Punkte f\xc3\xbcr Attribute wurden \xc3\xbcberschritten.\n'\
                                 'Bitte die Temp. Werte reduzieren!',
                          'en' : 'Used too much points for attributes. Plese reduce values of\n'\
                                 'Temp. Stats!'
                          },
          'stats_dp' : {'de' : 'Der Entwicklungspunktestand f\xc3\xbcr die Attribute ist nicht Null!\n'\
                                'Bringe ihn auf Null und dann geht es hier weiter.',
                        'en' : 'The developing points for the attributes are not zero!\n'\
                               'Correct that and it goes on.'
                        },
          'player' : {'de' : "Bitte Spielernamen eingeben",
                     'en' : "Please enter player's name",
                     },
          'name' : {'de' : "Bitte einen Charakternamen eingeben",
                    'en' : "Please enter a character name"
                    },
          'double' : {'de' : "Bitte nochmal kontrollieren: eine Auswahl ist doppelt!",
                      'en' : "Please check it again: one of your choices is double!",
                      },
          'no_race' : {'de' : "Bitte erst ein Volk ausw\xc3\xa4hlen!",
                       'en' : "Please chose a race first!"
                       },

          }


##\var infomsg
#Simply some info messages for the help window
infomsg = {'help_info' : {'de' : 'F\xc3\xbcr eine genauere Information '\
                                 '\xc3\xbcber die '\
                                 'einzelnen Standardelemente bitte auf das '\
                                 'Hilfe-Men\xc3\xbc klicken.',
                          'en' : 'For a more detailed information about the '\
                                 'default elements please click the help menu.',
                         }
           }


##\var s_elem_def
#Descriptions of the default elements for calculating EPs from.
s_elem_def = {'CRITICAL' : {'de' : 'Ausgeteilte kritische Treffer',
                            'en' : 'Made critical hits',
                           },
              'HITS'     : {'de' : 'Erhaltene Trefferpunkte',
                            'en' : 'Gained hit points.',
                            },
              'H_CRITS'  : {'de' : 'Erhaltene kritische Treffer',
                            'en': 'Gained criticals',
                           },
              'SPELL'    : {'de' : 'Stufe angewendeter Zauber',
                            'en' : 'Level of used spell',
                           },
              'MANEUVER' : {'de' : 'Erfolgreiche Man\xc3\xb6ver',
                           'en' : 'Successful maneuver.',
                           },
              'TRAVEL'   : {'de' : 'Reisestrecke',
                           'en' : 'Traveled distance',
                            },
              'KILLED'   : {'de' : 'Get\xc3\xb6tete Gegner',
                            'en' : 'Killed enemies/monster',
                            },
              'INDIVIDUAL' : {'de' : 'Individuelle Punkte.',
                              'en' : 'Individual EPs.',
                             },
              }


##\var csvlabels 
# Contains some values for characters
# \deprecated contains some values for characters (not needed yet)
csvlabels = {'Name' : {'de' : "Charaktername",
                       'en' : "character name"
                       },
             'Gender' : {'de' : "Geschlecht",
                         'en' : "gender"
                         },
             'female' : {'de' : 'weiblich',
                         'en' : 'female'
                         },
             'male' : {'de' : 'm\xc3\xa4nnlich',
                       'en' : 'male'
                       },
             'EP' :{'de' : 'Erfahrungspunkte',
                    'en' : 'experience points'
                    },
             'Player' : {'de' : 'Spieler',
                         'en' : 'player'
                         },
             'Date' : {'de' : 'Datum',
                       'en' : 'date'
                       },
             'Profession' : {'de' : 'Beruf',
                             'en' : 'profession'
                             },
             'Race' : {'de' : 'Rasse',
                       'en' : 'race'
                       },
             'Culture' : {'de' : 'Volk',
                          'en' : 'culture'
                          },
             'Group' : {'de' : 'Gruppe',
                        'en' : 'group'
                        },
             
             }

##\var trhelptext 
# Contains help text for class treasure
trhelptext = {'description' : {'de' : 'Schatzgenerator:\nErzeugt einen Text, der den Inhalt eines Schatzes beschreibt.\nParameter der Funktion findTreasure:\n',
                             'en' : 'Treasure Generator:\nCreates a text describing the content of a treasure.\nParameters of the function findTreasure:\n'
                            },
            'ttype' : {'de': 'Nummer oder Sch\xc3\xbcsselwort einer der folgenden Kategorien\n   1 sehr arm, 2 arm, 3 normal, 4 reich, 5 sehr reich\n',
                       'en': 'Number or keyword of one of the following categores\n   1 very poor, 2 poor, 3 normal, 4 rich, 5 very rich\n' 
                       },
            'output' : {'de' : 'Drei Optionen\n  \"screen\" --> Ausgabe auf den Bildschirm.\n  <string> --> Name der Ausgabedatei in die ausgegeben werden soll.\n  \"\" --> Es wird keine Datei erstellt, wenn der Parameter nicht gesetzt ist.',
                        'en' : 'Three options\n  \"screen\" --> Output on the screen.\n  <string> --> Name of the file which will be used for output.\n  \"\" --> No file is created if the parameter is not set.'
                            }
            }

##\var trtypelist
# Contains categories of richness of a treasure
trtypelist = {'de': ('sehr arm', 'arm', 'normal', 'reich', 'sehr reich'),
              'en': ('very poor', 'poor', 'normal', 'rich', 'very rich'),
              'num': (1, 2, 3, 4, 5)
              }

##\var trheader
# Contains header for treasure description
trheader = {'de' : "Schatzinhalt",
            'en' : "Content of Treasure"
            }

##\var valueTranslation
# Contains descriptions of money units
valueTranslation = {"ZS": {"de": "Zinnst\xc3\xbccke",
                           "en": "tin pieces"
                            },
                    "KS": {"de": "Kupferst\xc3\xbccke",
                           "en": "copper pieces"
                           },
                    "BS": {"de": "Bronzest\xc3\xbccke",
                           "en": "bronze pieces"
                           },
                    "SS": {"de": "Silberst\xc3\xbccke",
                           "en": "silver pieces"
                           },
                    "GS": {"de": "Goldst\xc3\xbccke",
                           "en": "gold pieces"
                           },
                    "MS": {"de": "Mithrilst\xc3\xbccke",
                           "en": "mithril pieces"
                           },
                    "Ed": {"de": "Edelsteine",
                           "en": "gems"
                           },
                    "Sch": {"de": "Schmuckst\xc3\xbccke",
                            "en": "jewelry"
                            }
                    }

##\var itemTranslation
# Contains description of items in a treasure
itemTranslation =   {"normal": {"de": "normaler Gegenstand",
                                "en": "normal item"
                                },
                     "Gew80": {"de": "guter Gegenstand (80% Gewicht)",
                               "en": "high quality item (80% weight)"
                               },
                     "Gew60": {"de": "guter Gegenstand (60% Gewicht)",
                               "en": "high quality item (60% weight)"
                               },
                     "Gew40": {"de": "guter Gegenstand (40% Gewicht)",
                               "en": "high quality item (40% weight)"
                               },
                     "Bonus5": {"de": "magisch verbesserter Gegenstand (Bonus +5)",
                                "en": "magical enhanced item (bouns +5)"
                                },
                     "Bonus10": {"de": "magisch verbesserter Gegenstand (Bonus +10)",
                                 "en": "magical enhanced item (bonus +10)"
                                 },
                     "Bonus15": {"de": "magisch verbesserter Gegenstand (Bonus +15)",
                                 "en": "magical enhanced item (bonus +15)"
                                 },
                     "Bonus20": {"de": "magisch verbesserter Gegenstand (Bonus +20)",
                                 "en": "magical enhanced item (bonus +20)"
                                 },
                     "Spruch": {"de": "Gegenstand mit eingebettetem Zauberspruch",
                                "en": "item with embedded spell"
                                },
                     "SV1": {"de": "Spruchvermehrer +1",
                             "en": "spell adder +1"
                             },
                     "SV2": {"de": "Spruchvermehrer +2",
                             "en": "spell adder +2"
                             },
                     "SV3": {"de": "Spruchvermehrer +3",
                             "en": "spell adder +3"
                             },
                     "MV2": {"de": "Magiepunktevermehrer x2",
                             "en": "power point multiplier x2"
                             },
                     "MV3": {"de": "Magiepunktevermehrer x3",
                             "en": "power point multiplier x3"
                             },
                     "bes": {"de": "besonderer Gegenstand",
                             "en": "special item"
                             }
                     }


##\var itemTypes
# This holds the type of the magical item   
itemTypes = {'1-40': {'de': 'Runenpapier',
                      'en': 'Rune Paper'
                      },
             '41-65': {'de': 'Trank',
                       'en': 'Potion'
                       },
             '66-70': {'de': 'Schmuckst\xc3\xbcck: T\xc3\xa4glich I',
                       'en': 'jewelry: Daily I'
                       },
             '71-75': {'de': 'Schmuckst\xc3\xbcck: T\xc3\xa4glich II',
                       'en': 'jewelry: Daily II'
                       },
             '76-80': {'de': 'Schmuckst\xc3\xbcck: T\xc3\xa4glich III',
                       'en': 'jewelry: Daily III'
                       },
             '81-85': {'de': 'Schmuckst\xc3\xbcck: T\xc3\xa4glich IV',
                       'en': 'jewelry: Daily IV'
                       },
             '86-94': {'de': 'Stab',
                       'en': 'Wand'
                       },
             '95-98': {'de': 'Rute',
                       'en': 'Rod'
                       },
             '99-100': {'de': 'Stecken',
                        'en': 'Pole'
                        } 
             }


##\var spellRealms
# This holds the realm of the spells   
spellRealms = {'1-30': {'de': 'Offene Essenz',
                         'en': 'Open Essence'
                         },
               '31-60': {'de': 'Magier',
                         'en': 'Magician'
                         },
               '61-75': {'de': 'Leitmagie',
                         'en': 'Channeling',
                         },
               '76-90': {'de': 'Animisten',
                         'en': 'Animist'
                         },
               '91-100': {'de': 'Barde/Waldl\xc3\xa4ufer',
                          'en': 'Bard/Hunter'
                          },
               }

##\var spellList
# This holds the spell list
spellLists = {'1-2' : {'Open Essence': {'de': 'Fluch',
                                        'en': 'Curse'
                                        },
                       'Magician': {'de': 'Fluch',
                                    'en': 'Curse'
                                    },
                       'Channeling': {'de': 'Fluch',
                                      'en': 'Curse'
                                      },
                       'Animist': {'de': 'Fluch',
                                   'en': 'Curse'
                                   },
                       'Bard/Hunter': {'de': 'Fluch',
                                       'en': 'Curse'
                                       },
                       },
              '3-14': {'Open Essence': {'de': 'Herrschaft \xc3\xbcber den K\xc3\xb6rper',
                                        'en': 'Reign over the body'
                                        },
                       'Magician': {'de': 'Gesetz des Feuers',
                                    'en': 'Fire Law'
                                    },
                       'Channeling': {'de': 'Naturkunde',
                                      'en': 'Natures law'
                                      },
                       'Animist': {'de': 'Seelenkunde',
                                   'en': 'Souls law'
                                   },
                       'Bard/Hunter' : {'de': 'Wege des Lernens',
                                        'en': 'Ways of learning'
                                        },
                       },
              '15-26': {'Open Essence': {'de': 'Verborgenes Verstehen',
                                         'en': 'Hiden understanding'
                                         },
                        'Magician': {'de': 'Gesetz des Eises',
                                     'en': 'Ice law'
                                     },
                        'Channeling': {'de': 'Wege des Wandelns',
                                       'en': 'Ways of changing'
                                       },
                        'Animist': {'de': 'Wesen des Blutes',
                                    'en': 'Nature of blood'
                                    },
                        'Bard/Hunter': {'de': 'Lieder der Macht',
                                        'en': 'Songs of power'
                                        },
                        },
              '27-38': {'Open Essence': {'de': 'Wege des Öffnens',
                                         'en': 'Ways of Opening'
                                         },
                        'Magician': {'de': 'Gesetz der Erde',
                                     'en': 'Earth law'
                                     },
                        'Channeling': {'de': 'Abwehr von Zaubern',
                                       'en': 'Defense of Spells'
                                       },
                        'Animist': {'de': 'Wesen der Knochen und Muskeln',
                                    'en': 'Nature of bones and muscles'
                                    },
                        'Bard/Hunter': {'de': 'Ger\xc3\xa4uschkontrolle',
                                        'en': 'Sound control'
                                        },
                        },
              '39-50': {'Open Essence': {'de': 'Hand der Essenz',
                                         'en': 'Hand of essence'
                                         },
                        'Magician': {'de': 'Gesetz des Lichts',
                                     'en': 'Light law'
                                     },
                        'Channeling': {'de': 'Wege der Heilung',
                                       'en': 'Ways of healing'
                                       },
                        'Animist': {'de': 'Wesen der Organe',
                                    'en': 'Nature of organs'
                                    },
                        'Bard/Hunter': {'de': 'Gegenstandskunde',
                                        'en': 'Item lore'
                                        },
                        },
              '51-62': {'Open Essence': {'de': 'Spruchkunde',
                                         'en': 'Spell lore'
                                         },
                        'Magician': {'de': 'Gesetz des Windes',
                                     'en': 'Wind law'
                                     },
                        'Channeling': {'de': 'Schutz',
                                       'en': 'Protection'
                                       },
                        'Animist': {'de': 'Beherrschung der Tiere',
                                    'en': 'Animal control'
                                    },
                        'Bard/Hunter': {'de':'Wesen der Wege',
                                        'en': 'Nature of paths'
                                        },
                        },
              '63-74': {'Open Essence': {'de': 'Wege der Wahrnehmung',
                                         'en': 'Ways of perception'
                                         },
                        'Magician': {'de': 'Gesetz des Wassers',
                                     'en': 'Water law'
                                     },
                        'Channeling': {'de': 'Verborgenes Entdecken',
                                       'en': 'Discover hidden'
                                       },
                        'Animist': {'de': 'Beherrschung der Pflanzen',
                                    'en': 'Plant control'
                                    },
                        'Bard/Hunter': {'de': 'Wege des Wanderns',
                                        'en': 'Ways of wandering'
                                        },
                        },
              '75-86': {'Open Essence': {'de': 'Illusionen',
                                         'en': 'Illusions'
                                         },
                        'Magician': {'de': 'Entfernungen Überbr\xc3\xbccken',
                                     'en': 'Distance law'
                                     },
                        'Channeling': {'de': 'Wege von Ger\xc3\xa4usch und Licht',
                                       'en': 'Ways of sound and light'
                                       },
                        'Animist': {'de': 'Heilkunde',
                                    'en': 'Healing'
                                    },
                        'Bard/Hunter': {'de': 'Wege der Tarnung',
                                        'en': 'Ways of Camouflage'
                                        },
                        },
              '87-98': {'Open Essence': {'de': 'Herrschaft \xc3\xbcber den Geist',
                                         'en': 'Reign over the mind',
                                         },
                        'Magician': {'de': 'K\xc3\xb6rperkontrolle',
                                     'en': 'Body control'
                                     },
                        'Channeling': {'de':'Wege der Beruhigung',
                                       'en': 'Ways of sedation',
                                       },
                        'Animist': {'de': 'Nahrung und Schutz',
                                    'en': 'Food and Protection'
                                    },
                        'Bard/Hunter': {'de': 'Wesen der Natur',
                                        'en': 'Ways of Nature'
                                        },
                        },
              '99-100': {'Open Essence': {'de':'Besonderheit',
                                          'en':'Special'
                                          },
                         'Magician': {'de': 'Besonderheit',
                                      'en': 'Special'
                                      },
                         'Channeling': {'de': 'Besonderheit',
                                        'en': 'Special'
                                        },
                         'Animist': {'de': 'Besonderheit',
                                     'en': 'Special'
                                     },
                         'Bard/Hunter': {'de': 'Besonderheit',
                                         'en': 'Special' 
                                         },
                         }
              }

