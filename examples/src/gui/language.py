#!/usr/bin/env python
'''
\file /home/mongol/workspace/bpcheck2/src/gui/language.py
\package gui.language
\brief Language Support File.


\date (C) 2012
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''
'''
This holds general screen messages.
'''
screenmsg = {'welcome'     : {'de' : "Willkommen beim ADaManT Profil Generator",
                               'en' : "Welcome at the ADaManT profile generator",
                               },
              'wrongver'    : {'de' : 'Falsche Python-Version!!',
                               'en' : 'Wrong Python version!!',
                               },
              'ossupport'   : {'de' : 'Das Betriebsystem wird unterst\xc3\xbctzt.',
                               'en' : 'The operating system is supported.',
                               },
              'osnosupport' : {'de' : 'Das Betriebssystem wird leider' \
                                      'nicht unterst\xc3\xbctzt',
                                'en': ' Sorry, OS not supported!',
                                },
              'notdoneyet' : {'de' : 'Leider ist dieser Punkt noch nicht fertig!',
                              'en' : 'Sorry, not done yet!!'
                              },
              'saved' : {'de' : 'Datei gespeichert',
                         'en' : 'File saved'
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
             'but_refr' : {'de' : 'Auffrischen!',
                           'en' : 'refresh!'},
             'but_take' : {'de' : '\xc3\x9cbernehmen',
                           'en' : 'take over'},
             }

'''
This holds the texts of the main menu bar
'''
txtmenu = {'menu_help'     : {'de' : 'Hilfe',
                              'en' : 'Help',
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
          }

'''
This holds the cascade entries of the menu fields
'''
submenu = { 'file' : {'new' : {'de' : 'Neue Datei',
                              'en' : 'New File'},
                      'open' : {'de' : 'Datei oeffnen',
                                'en' : 'Open File'
                                },
                      'save' : {'de' : 'Speichern',
                                'en' : 'Save'
                                },
                      'save_as' : {'de' : 'Speichern unter',
                                   'en' : 'Save as'
                                   },
                      'close' : {'de' : 'Schliessen',
                                 'en' : 'Close'
                                 },
                      'quit' : {'de' : 'Beenden',
                                'en' : 'Quit'}
                      },
            'help' : {'about' : {'de' : 'Ueber dieses Programm',
                                 'en' : 'About this program'
                                 },
                      'context' : {'de' : 'Kontexthilfe',
                                   'en' : 'context help'
                                   },
                      },
           'edit' : {'add' : {'de' : 'Daten hinzufuegen',
                              'en' : 'Add Data'
                              },
                     'remove' : {'de' : 'Daten entfernen',
                              'en' : 'Remove Data'
                              },
                     'edit' : {'de' : 'Daten bearbeiten',
                               'en' : 'Edit Data'
                               },
                     'graph' : {'de' : 'Graph plotten',
                                 'en' : 'plotting graphs'
                                 },
                     },
           'opts' : {'basic' : {'de' : 'Grundeinstellungen',
                               'en' : 'Basic Options'
                               },
                    'graph' : {'de' : 'Grafikeinstellungen',
                               'en' : 'Graphics Options'
                               },
                    'output' : {'de' : 'Ausgabeoptionen',
                                'en' : 'Output Options'}
                    }
           }
'''
This holds the window titles
'''
wintitle = {'main' : {'de' : 'Blutdruck-Checker',
                      'en' : 'Blood Pressure Checker'
                      },
            'options'  : {'de' : 'Einstellungen',
                          'en' : 'Options'
                         },
            'graph' : {'de' : 'Graphenplotter',
                       'en' : 'Plotting graphs'
                       },
            'help' : {'de' : 'Hilfe',
                      'en' : 'Help'
                      },
            }

buttons = {'ok' : {'de' : 'OK',
                   'en' : 'Okay'
                   },
           'cancel' : {'de' : 'Abbrechen',
                        'en' : 'Cancel'
                        },
           'graph' : {'de' : 'Graph plotten',
                      'en' : 'plotting graph'
                      },
           }

widget = {'systolic' : {'de' : 'systolischer Wert',
                         'en' : 'systolic value'
                         },
          'diastolic' : {'de' : 'diastolischer Wert',
                          'en' : 'diastolic value'
                          },
          'pulse' : {'de' : 'Puls',
                      'en' : 'pulse'
                      },
          }

txtwin = {'all_files' : {'de' : ("alle Dateien", '.*'),
                         'en' : ("all files", '.*'),
                         },
         'bpc'  : {'de' : ('BPC-Dateien', '.bpc'),
                         'en' : ('BPC files', '.bpc'),
                         },
          }
