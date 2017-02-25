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
\version 0.3 
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
             'but_roll' :{'de' : 'Würfeln',
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
           'hlp_about'     : {'de' : 'über',
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
                          'new_char' : "new character",
                          'new_grp' : "new characer party"
                          },
                    },
           'opts'  :{'de' : {'lang' : 'Einstellungen',
                             },
                     'en' : {'lang' : 'preferences',
                             }
                     },
           'help'  :{'de' : {'about' : '\xc3\x9cber rpg-tools',
                             'page'  : '\xc3\x9cber diese Seite',
                             'win'   : '\xc3\x9cber dieses Fenster',
                             'global' : 'Handbuch',
                             },
                     'en' : {'about' : 'about rpg-tools',
                             'page'  : 'about this page',
                             'win'   : 'about this window',
                             'global' : 'handbook',
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
                              'ed_equip' : 'edit equipment'
                               },
            
                      },
           'items' : {'de' : {'treasure': "Schatz generieren",
                              'magical' : "Magische Gegenstände erzeugen",
                              },
                      'en' : {'treasure': "create treasure",
                              'magical' : "create magic items",
                              },
                      },
           'group' : {'de' : {'add/rem' : "Charakter hinzufügen/entfernen",
                              'new'     : "Neue Charaktergruppe",
                              'gmview'  : "Spielleiterübersicht",
                              },
                      'en' : {'add/rem' : "add/remove characters",
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
          'json_files': {'de' : ('JSON Dateien', '.json'),
                         'en' : ('JSON files', '.json')
                         },
          }

## \var processing
#some processing messages
processing = {'saved' : {'de' : 'Gespeichert...',
                         'en' : 'Saved...',
                         },
              'exported' : {'de' : 'Export abgeschlossen.',
                            'en' : 'export finished.'
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
                       'en' : 'additional elements (comma separated list)',
                       },
          'connect'  : {'de' : 'Verbinden',
                       'en' : 'connect',
                       },
          'update'   : {'de' : 'aktualisieren',
                       'en' : 'update',
                       },
          'cancel'   : {'de' : 'Abbrechen',
                        'en' : 'Cancel',
                      },
          'preview' : {'de' : 'Vorschau',
                       'en' : 'preview',
                       },
          }


##\var errmsg
#Error messages for all opportunities 
errmsg = {'no_file' : {'de' : 'Datei existiert nicht!',
                       'en' : 'File does not exists!',
                       },
          'no_name' : {'de' : 'Kein Dateiname angegeben!',
                       'en' : 'No file name given!',
                       },
          'no_read' : {'de' : 'Datei ist nicht lesbar!',
                       'en' : 'File is not readable!',
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
                                 'primären Attributen (+) betragen!',
                          'en' : 'Wrong attibute value:\n\n'\
                                 'it must have a min of 20 concerning standard and\n'\
                                 '90 concerning primary attributes (+)!'
                          },
          'too_much_stats':{'de' : 'Die vorhandenen Punkte für Attribute wurden überschritten.\n'\
                                 'Bitte die Temp. Werte reduzieren!',
                          'en' : 'Used too much points for attributes. Plese reduce values of\n'\
                                 'Temp. Stats!'
                          },
          'stats_dp' : {'de' : 'Der Entwicklungspunktestand für die Attribute ist nicht Null!\n'\
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
          'no_race' : {'de' : "Bitte erst ein Volk auswählen!",
                       'en' : "Please chose a race first!"
                       },

          }


##\var infomsg
#simply some info messages for the help window
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
              'MANEUVER' : {'de' : 'Erfolgreiche Manoever',
                           'en' : 'Successful maneuver.',
                           },
              'TRAVEL'   : {'de' : 'Reisestrecke',
                           'en' : 'Traveled distance',
                            },
              'KILLED'   : {'de' : 'Getoetete Gegner',
                            'en' : 'Killed enemies/monster',
                            },
              'INDIVIDUAL' : {'de' : 'Individuelle Punkte.',
                              'en' : 'Individual EPs.',
                             },
              }


##\var csvlabels 
# contains some values for characters
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
