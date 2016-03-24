#!/usr/bin/env python

## \file lang.py
#
# \brief multi language support library for rpg-tools 
#
# Here are all the things implemented that are needed for the switching of 
# language in the rpg-tools. So this file consists mainly 
# of dictionary structures.
# Currently supported languages are:
# \li English
# \li Deutsch
# \attention At the moment just Linux/Unix is supported
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
           'menu_edit'     : {'de' : 'editieren',
                              'en' : 'edit',
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
                          },
                    'en':{'open'  : 'Open file',
                          'close' : 'Close file',
                          'new'   : 'New file',
                          'save'  : 'Save file',
                          'sv_as' : 'Save as',
                          'quit'  : 'Quit',
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
           'edit'  : {'de' : {'edt'  : 'bearbeiten',
                              },
                      'en'  :{'edt'  : 'edit',
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
wintitle = {'opt_lang' : {'de' : 'ADaManT Spracheinstellungen',
                          'en' : 'ADaManT Language Settings',
                          },
            'main'     : {'de' : 'ADaManT Profil-Generator',
                          'en' : 'ADaManT Profile Generator',
                          },
            'edit'     : {'de' : 'ADaManT Profil Editor',
                          'en' : 'ADaManT Profile Editor',
                          },
            'struc_elem' : {'de' : 'ADaManT Struktur-Element-Editor',
                            'en' : 'ADaManT editor for structual elements',
                            },
            'meta_1' :{'de' : 'ADaManT Metadaten-Felder Editor',
                       'en' : 'ADaManT meta data editor',
                       },
            'meta_2' : {'de' : 'ADaManT Metadatenfeldkonfiguration',
                        'en' : 'ADaManT meta data field configuration'}
            }

'''
labels for window elements (labels, listboxes etc.)
'''
labels = {'cfg_path' : {'de' : 'Speicherpfad f\xc3\xbcr die XML-Dateien',
                        'en' : 'Path where to store the XML files',
                        },
          'log_path' : {'de' : 'Pfad zu den Log-Dateien',
                        'en' : 'Path of the log files',
                        },
          'default_c' : {'de' : 'Standartauswahl',
                         'en' : 'standard selection',
                         },
          'select_c' : {'de' : 'getroffene/geladene Auswahl',
                        'en' : 'selected/loaded choice',
                        },
          'add_elem' :{'de' :'Zus\xc3\xa4tzliche Elemente (Komma getrennte Liste)',
                       'en' : 'additional elements (comma separated list)',
                       },
          'sel_root' :{'de' : 'Root-Element festlegen',
                       'en' : 'select root element',
                       },
          'sel_par' : {'de' : '\xc3\x9cbergeordnetes Element',
                       'en' : 'parent element',
                       },
          'sel_child' : {'de' : 'Untergeordnete(s) Element(e)',
                         'en' : 'child element(s)',
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
s_elem_def = { 'PROJECT' : {'de' : 'PROJECT: Dieses Strukturelement be'\
                                   'schreibt f\xc3\xbcr gew\xc3\xb6hnlich die'\
                                   ' oberste '\
                                   'Ebene der Datenstruktur. Anschaulich '\
                                   'ist hiermit das Gesamtprojekt gemeint, '\
                                   'in dem die Daten erhoben wurden.',
                            'en' : 'PROJECT: This element of structure means '\
                                   'usually the highest level of the data '\
                                   'structure. Desciptively, it means the '\
                                   'whole project where the data were'\
                                   ' generated.',
                           },
              'PROCEDURE' :{'de' : 'PROCEDURE: Hiermit ist eine allgemeinere '\
                                   'Herangehensweise gemeint, die dann letzten'\
                                   ' Endes zu EXPERIMENTen f\xc3\xbchrt.',
                            'en' : 'PROCEDURE: This means a more general '\
                                   'approach which leads last but not least to'\
                                   'different types of EXPERIMENTs.',
                            },
              'EXPERIMENT' : {'de' : 'EXPERIMENT: Dieses Strukturelement be'\
                                     'schreibt das tats\xc3\xa4chliche Experiment,'\
                                     'in dem Daten erzeugt werden.',
                              'en': 'EPERIMENT: This element of structure '\
                                    'really stands for an experiment where '\
                                    'data are raised.',
                              },
              'PERSON' :{'de' : 'PERSON: Dieses ELement steht f\xc3\xbcr Personen,'\
                                'die mit einem Strukturlevel z.B. EXPERIMENT '\
                                'in Zusammenhang stehen.',
                         'en' : 'PERSON: This element stands for persons who'\
                                'are connected to a structure level, e.g. '\
                                'EXPERIMENT.',
                         },
              'PROGRAM' : {'de' : 'PROGRAM: Diese Element steht f\xc3\xbcr Programm-'\
                                  'Dateien, die z.B. zum Erzeugen oder Aus'\
                                  'werten von Daten benutzt wurden.',
                           'en' : 'PROGRAM: This element stands for program '\
                                  'files which were used, e.g. for generating '\
                                  'or examining data.',
                           },
              'DATAFILE' : {'de' : 'DATAFILE: Hiermit wird ein Struturelement '\
                                   'f\xc3\xbcr Datendateien beschrieben. Dabei ist '\
                                   'es nicht wichtig welcher Art die Daten'\
                                   ' sind.',
                            'en' : 'DATAFILE: This describes an element of '\
                                   'structure for data files. It is not '\
                                   'important what kind of data they hold.',
                            },
              'FILESET' : {'de' : 'FILESET: Steht f\xc3\xbcr S\xc3\xa4tze von Dateien, die'\
                                  ' zusammengeh\xc3\xb6ren.',
                           'en' : 'FILESET: This stands for sets of files which'\
                                  'belong to each other.',
                           },
              'ANIMAL' : {'de' : 'ANIMAL: Beschreibt die Tierart, die '\
                                  'f\xc3\xbcr die Datenerhebung verwendet wurde.',
                          'en' : 'ANIMAL: That type of animal used for getting'\
                                 ' the experimental data.',
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
             
             }
