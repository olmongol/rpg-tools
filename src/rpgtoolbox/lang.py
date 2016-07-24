#!/usr/bin/env python

# \package rpgtoolbox
# \file lang.py
#
# \brief multi language support library for rpg-tools 
#
# Here are all the things implemented that are needed for the switching of 
# language in the rpg-tools. So this file consists mainly 
# of dictionary structures.
# Currently supported languages are:
# \li English
# \li Deutsch
#
# \attention At the moment just Linux/Unix is supported!
#
# \author Marcus Schwamberger
# \email marcus@lederzeug.de
# \date (c) 2015-2016
# \version 0.2 
# \license GNU V3.0
#
# \todo check for German special characters.

'''
This holds general screen messages.
'''
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

'''
This holds the texts written on buttons.
'''
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
             'but_prev' : {'de' : 'Zur\xc3\xbcck',
                           'en' : 'back'},
             'but_refr' : {'de' : 'zeigen/auffrischen',
                           'en' : 'show/refresh'},
             'but_take' : {'de' : '\xc3\x9cbernehmen',
                           'en' : 'take over'},
             'but_sel_root' : {'de' : 'Root-Element festlegen',
                               'en' : 'confirm root element',
                               },
             'but_rem_root' : {'de' : 'Root-Element entfernen',
                               'en' : 'remove root element',
                               },
             'but_cre_link' : {'de' : 'Verkn\xc3\xbcpfung erstellen',
                               'en' : 'create link',
                               },
             'but_rem_link' : {'de' : 'Verkn\xc3\xbcpfung l\xc3\xb6schen',
                               'en' : 'delete link',
                               },
             'but_save_exit' : {'de' : 'Speichern und schliessen',
                                'en' : 'save and exit',
                                },
             'but_save_next' : {'de' : 'Speichern und weiter',
                                'en' : 'save and next',
                                },
             'but_add_meta' : {'de' : 'Metadatenfeld  hinzuf\xc3\xbcgen',
                               'en' : 'add meta data field',
                              },
             'but_rem_meta' : {'de' : 'Metadatenfeld(er) entfernen',
                               'en' : 'remove meta data field(s)',
                               },
             'but_show_graph' : {'de' : 'Struktur plotten',
                                 'en' : 'plot structure'
                                 },
             }

'''
This holds the texts of the main menu bar
'''
txtmenu = {'help'          : {'de' : 'Hilfe',
                              'en' : 'Help',
                              },
           'hlp_about'     : {'de' : '\xc3\x9cber',
                              'en' : 'About',
                              },
           'hlp_first'     : {'de' : 'Erste Schritte',
                              'en' : 'first steps',
                              },
           'hlp_context'   : {'de' : 'Kontexthilfe',
                              'en' : 'context help',
                              },
           'but_ok'        : {'de' : 'OK',
                              'en' : 'ok',
                              },
           'but_quit'      : {'de' : 'Schliessen',
                              'en' : 'quit',
                              },
           'menu_edit'     : {'de' : 'Bearbeiten',
                              'en' : 'Edit',
                              },
           'menu_file'     : {'de' : 'Datei',
                              'en' : 'file',
                              },
           'menu_opt'      : {'de' : 'Optionen',
                              'en' : 'options',
                              },
           'menu_new_prof' : {'de' : 'Ne\xc3\xbcs Profil',
                              'en' : 'New profile',
                              },
           'menu_add_proc' : {'de' : 'Ne\xc3\xbc Prozedur hinzuf\xc3\xbcgen',
                              'en' : 'Add new procedure',
                              },
           'menu_add_exp'  : {'de' : 'Ne\xc3\xbcs Experiment hinzuf\xc3\xbcgen',
                              'en' : 'Add new experiment',
                              },
          }

'''
This holds the texts of the submenu cascades.
'''
submenu = {'file' :{'de':{'open'  : 'Datei \xc3\xb6ffnen',
                          'close' : 'Datei schliessen',
                          'new'   : 'Neue Datei',
                          'save'  : 'Datei speichern',
                          'sv_as' : 'Datei speichern unter...',
                          'quit'  : 'Beenden',
                          'export' : 'Exportieren'
                          },
                    'en':{'open'  : 'Open file',
                          'close' : 'Close file',
                          'new'   : 'New file',
                          'save'  : 'Save file',
                          'sv_as' : 'Save as',
                          'quit'  : 'Quit',
                          'export' : 'Export'
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
           'edit'  : {'de' : {'ed_char'  : 'Charakter bearbeiten',
                              'ed_grp'   : 'Gruppe bearbeiten',
                              'ed_fight' : 'Kampf-EPs',
                              'ed_other' : 'EPs Zauber,Reisen, Man\xc3\xb6ver',
                              'ed_indiv' : 'Ideen-EPs',
                              'ed_calc'  : 'Zusammenrechnen',
                              'ed_sim'   : 'Kampfsimulation (EP)',
                              },
                      'en'  :{'ed_char'  : 'Edit Character',
                              'ed_grp'   : 'Edit Group',
                              'ed_fight' : 'Fight EPs',
                              'ed_other' : 'EPs for Spells,Travel,Maneuver',
                              'ed_indiv' : 'EPs for ideas',
                              'ed_calc'  : 'Calculate all',
                              'ed_sim'   : 'EPs for fight simulation',
                               },
                      },
           
           }

'''
this holds the content of choosable filetypes while open/close files.
'''
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
                         }
          }

'''
some processing messages
'''
processing = {'saved' : {'de' : 'Gespeichert...',
                         'en' : 'Saved...',
                         },
              'exported' : {'de' : 'Export abgeschlossen.',
                            'en' : 'export finished.'
                            }
            }

'''
language shortcuts
'''
shortcut = {'de' : 'Deutsch',
            'en' : 'English',
            }

'''
this are the titles of the windows-
'''
wintitle = {'opt_lang' : {'de' : 'Spracheinstellungen',
                          'en' : 'Language Settings',
                          },
            'main'     : {'de' : 'Rollenspiel Werkzeuge',
                          'en' : 'RPG Tools',
                          },
            'edit'     : {'de' : 'Editor',
                          'en' : 'Editor',
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
            }

'''
labels for window elements (labels, listboxes etc.)
'''
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
                        'en' : 'DB paasword'
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

'''
Elements of  OptionMenus which shall be shown but not choosen.
'''
ommsg = {'sel_struc' :{'de' : 'Strukturelement w\xc3\xa4hlen',
                       'en' : 'select element of structure',
                       },
         }
'''
Error messages
'''
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

          }


'''
simply some info messages for the help window
'''
infomsg = {'help_info' : {'de' : 'F\xc3\xbcr eine genauere Information '\
                                 '\xc3\xbcber die '\
                                 'einzelnen Standardelemente bitte auf das '\
                                 'Hilfe-Men\xc3\xbc klicken.',
                          'en' : 'For a more detailed information about the '\
                                 'default elements please click the help menu.',
                          },
           'help_selem' : {'de' : 'Das Feld STANDARTAUSWAHL zeigt die Struktur'\
                                  'elemente, die als gundlegende Vorgaben vor'\
                                  'geschlagen werden.\n\n'\
                                  'Mit dem Button "--->>" werden ausgew\xc3\xa4hlte '\
                                  'Elemente aus diesem Feld in das Feld GETROF'\
                                  'FENE/GELADENE AUSWAHL kopiert. Alles, was in'\
                                  ' diesem Feld ist, wird auch in den weiteren '\
                                  'Arbeitsschritten verwendet.\n\n'\
                                  'Am unteren Rand findet sich ein Eingabefeld,'\
                                  'in dem man eine Komma-separierte Liste mit '\
                                  'weiteren Strukturelementen eingeben und '\
                                  'hinzuf\xc3\xbcgen kann.\n\n'\
                                  'Ist soweit alles fertig, geht es mit dem '\
                                  'WEITER-Button zum n\xc3\xa4chsten Arbeitsschritt.'
                                  ,
                           'en' : 'The field STANDARD SELECTION shows elements '\
                                  'of structure which are proposed to be basic.\n\n'\
                                  'The button "--->>" copies selected items to '\
                                  'the field SELECTED/LOADED CHOICE. Every item '\
                                  'in there will be used in the following steps.\n\n'\
                                  'On the lower border there is an entry field '\
                                  'were additional elements of structure can be '\
                                  'entered and added.\n\n'\
                                  'When everything is fine and finished so far '\
                                  'the NEXT button takes you to the next step.',
                           },
           'help_back_but' : {'de' : 'Der Zur\xc3\xbcck-Button bringt einem zum'\
                                     ' vohergehenden Fenster. Einstellungen, '\
                                     'die im aktuellen Fenster gemacht wurden,'\
                                     ' gehen dabei allerdings verloren.',
                              'en' : 'The Back button brings you back to the'
                                     ' last window. But clicking it will cancel'\
                                     ' all the editing you might have done in the'\
                                     ' current window.'},
           }


'''
Descriptions of the default structure elements.
'''
s_elem_def = { 'CRITICAL' : {'de' : 'Ausgeteilte kritische Treffer',
                            'en' : 'Made critical hits',
                           },
              'HITS' :{'de' : 'Erhaltene Trefferpunkte',
                            'en' : 'Gained hit points.',
                            },
              'H_CRITS' : {'de' : 'Erhaltene kritische Treffer',
                              'en': 'Gained criticals',
                              },
              'SPELL' :{'de' : 'Stufe angewendeter Zauber',
                         'en' : 'Level of used spell',
                         },
              'MANEUVER' : {'de' : 'Erfolgreiche Manoever',
                           'en' : 'Successful maneuver.',
                           },
              'TRAVEL' : {'de' : 'Reisestrecke',
                            'en' : 'Traveled distance',
                            },
              'KILLED' : {'de' : 'Getoetete Gegner',
                           'en' : 'Killed enemies/monster',
                           },
              'INDIVIDUAL' : {'de' : 'Individuelle Punkte.',
                          'en' : 'Individual EPs.',
                          },
              }

'''
attributes for structure elements
'''
screentext = {'label' : {'de' : 'Bezeichnung',
                          'en' : 'name',
                          },
             'type'  : {'de' : 'Art des Vorkommens',
                        'en' : 'kind of occurence',
                        },
             'dbtype' : {'de' : 'Datenbanktyp',
                         'en' : 'database type',
                         },
             'new' : {'de' : 'Neu',
                      'en' : 'New'
                      },
             }
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
