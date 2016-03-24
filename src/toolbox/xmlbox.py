#!/usr/bin/env python
'''
\file xmlbox.py

\brief This module contains needed XML tools.


\date (C) 2012
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.5.1 alpha

\todo There have be a clean out and a unifying of dictionary keys...
'''



## attrib_struct
# Allowed attributes for functional elements of structure
attrib_struc = {'type'   : ['single', 'multi'],
                'dbtype' : ['nested', 'collection'],
                }

## attrib_metad
# Allowed attributes for metadata elements
attrib_metad = {'display'  : ['text', 'pulldown', 'textbox', 'listbox',
                              'comment', 'date', 'time',
                              'email', 'password'],
                'type'     : ['str', 'int', 'float',
                              'date', 'time'],
                'name'     : '',
                'list'     : ['false', 'true'],
                }
'''
dictionary for the lowest level of the structure elements attributes
'''
submeta = {'type' : '',
          'display' : '',
          'name' : '',
          'list' : ''
          }
'''
dictionary that represents default structure elements
'''
meta = {'PROJECT' :{'Name' : {'type' : attrib_metad['type'][0],
                                       'display' : attrib_metad['display'][0],
                                       'name' : 'Project',
                                       'list' : 'false',
                                       },
                    'Description' : {'type' : attrib_metad['type'][0],
                                     'display' : attrib_metad['display'][2],
                                     'name' : 'Description',
                                     'list' : 'false'
                                     },
                     'Aim' : {'type' : attrib_metad['type'][0],
                              'display' : attrib_metad['display'][2],
                              'name' : 'Aim',
                              'list' : 'false'
                              },
                     'Leader' : {'type' : attrib_metad['type'][0],
                                 'display' : attrib_metad['display'][0],
                                 'name' : 'Leader',
                                 'list' : 'false'
                                 },
                     'Member' : {'type' : attrib_metad['type'][3],
                                 'display' : attrib_metad['display'][1],
                                 'name' : 'Member',
                                 'list' : 'true',
                                 },
                     'Procedure' : {'type' : attrib_metad['type'][0],
                                    'display' : attrib_metad['display'][0],
                                    'name' : 'Procedure',
                                    'list' : 'false',
                                    },
                     },
         'PERSON' : {'Name' : {'type' : 'str',
                              'display' : 'text',
                              'name' : 'Name',
                              'list' : 'false'
                              },
                     'User' : {'type' : 'str',
                               'display' : 'text',
                               'name' : 'Username',
                               'list' : 'false'
                            },
                     'Institute' : {'type' : 'str',
                                    'display' : 'text',
                                    'name' : 'Institute',
                                    'list' : 'false'
                                 },
                     'Email' : {'type' : 'str',
                                'display' : 'email',
                                'name' : 'email',
                                'list' : 'false'
                                },
                     'Phone' : {'type' : 'str',
                                'display' : 'text',
                                'name' : 'phone',
                                'list' : 'true'
                                },
                     },
        'ANIMAL' :{'Species' :{'type': 'str',
                               'display' : 'text',
                               'name': 'Species',
                               'list' : 'false'
                               },
                   'Gender' :{'type' : 'str',
                              'display' : 'text',
                              'name' : 'Gender',
                              'list' : 'false'
                              },
                   'Age' : {'type': 'int',
                            'display' : 'text',
                            'name' :'Age',
                            'list' : 'false'
                            },
                   'Weight' : {'type' : 'float',
                               'display' : 'text',
                               'name' : 'Weight',
                               'list' : 'false'
                               },
                   },
         'PROCEDURE' : {'Name' : {'type' : 'str',
                                  'display' : 'text',
                                  'name' : 'Name',
                                  'list' : 'false'
                                  },
                       'Aim' : {'type' : 'str',
                                 'display' : 'textbox',
                                 'name' :  'Aim',
                                 'list' : 'false'
                                },
                       'Experimenter' : {'type' : 'str',
                                         'display' : 'listbox',
                                         'name' : 'Experimenter',
                                         'list' : 'true'
                                         },
                       'Start_Date' : {'type' : 'date',
                                       'display' : 'date',
                                       'name' : 'Start date',
                                       'list' : 'false'
                                       },
                       'End_Date' : {'type' : 'date',
                                     'display' : 'date',
                                     'name' : 'End date',
                                     'list' : 'false'
                                     },
                       },
         'EXPERIMENT' : {'Name' : {'type' : 'str',
                                   'display' : 'text',
                                   'name' : 'Experiment name',
                                   'list' : 'false'
                                   },
                         'Aim' : {'type' : 'str',
                                  'display' : 'textbox',
                                  'name' : 'Aim',
                                  'list' : 'false'
                                  },
                         'Approach' : {'type' : 'str',
                                       'display' : 'textbox',
                                       'name' :'Approach',
                                       'list' : 'false'
                                       },
                         'Method' : {'type' : 'str',
                                     'display': 'pulldown',
                                     'name': 'Method',
                                     'list' : 'true'
                                     },
                         'Comment' : {'type' : 'str',
                                      'display' : 'textbox',
                                      'name' : 'Comment',
                                      'list' : 'false'
                                      },
                        },
         'FILESET' : {'Name' : {'type' : 'str',
                               'display' : 'text',
                               'name' : 'Set name',
                               'list' : 'false'
                               },
                     'Data_Type' : {'type' : 'str',
                                    'display' : 'pulldown',
                                    'name' : 'Data type',
                                    'list' : 'true'
                                    },
                     'Aim' : {'type' : 'str',
                              'display' : 'textbox',
                              'name' : 'Aim',
                              'list' : 'false'
                              },
                     },
         'PROGRAM' : {'Name' : {'type' : 'str',
                               'display' : 'text',
                               'name' : 'Program name',
                               'list' : 'false'
                               },
                     'Description' : {'type' : 'str',
                                      'display' : 'textbox',
                                      'name' : 'Description',
                                      'list' : 'false'
                                      },
                     'Type' : {'type' : 'str',
                               'display' : 'text',
                               'name' : 'Program/File type',
                               'list' : 'false'
                               },
                     'Creator' : {'type' : 'str',
                                  'display' : 'text',
                                  'name' : 'Creator',
                                  'list' : 'true',
                               },
                     'File_Name' : {'type' : 'str',
                                    'display' : 'text',
                                    'name' : 'File name',
                                    'list' : 'false'
                                    },
                     'File_Size' : {'type' : 'int',
                                    'display' : 'text',
                                    'name' : 'File size',
                                    'list' : 'false'
                                    },
                     'Date_Uploaded' : {'type' : 'date',
                                        'display' : 'date',
                                        'name' : 'date uploaded',
                                        'list' : 'false'
                                        },
                     'Version' : {'type' : 'str',
                                  'display' : 'text',
                                  'name' : 'version',
                                  'list' : 'false'
                                  },
                     'Comment' : {'type' : 'str',
                                  'display' : 'textbox',
                                  'name' : 'Comment',
                                  'list' : 'false'
                                  },
                  },
         'DATAFILE' : {'Name' : {'type' : 'str',
                                'display' : 'text',
                                'name' : 'Data file name',
                                'list' : 'false'
                                },
                      'Size' : {'type' : 'int',
                                'display' : 'text',
                                'name' : 'file size',
                                'list' : 'false'
                                },
                      'Comment' : {'type' : 'str',
                                   'display' : 'textbox',
                                   'name' : 'Comment',
                                   'list' : 'false'
                                   },
                      'Creation_Date' : {'type' : 'date',
                                         'display' : 'date',
                                         'name' : 'creation date',
                                         'list' : 'false'
                                         },
                      'Upload_Date' : {'type' : 'date',
                                       'display' : 'date',
                                       'name' : 'upload date',
                                       'list' : 'false'
                                       },
                      },
        }

## struct
# holds the default data structure.
struct = {'PROJECT' : {'attrib'  : {'type'   : 'single',
                                    'name'   : 'project',
                                    'dbtype' : 'collection',
                                    },
                       'subelem' : ['PROCEDURE',
                                    'PERSON',
                                    ],
                       'parent'  : [],
                       },
          'PERSON'  : {'attrib'  : {'type'   : 'multi',
                                    'name'   : 'person',
                                    'dbtype' : 'collection',
                                    },
                       'subelem' : [],
                       'parent'  : ['PROJECT',
                                    'PROGRAM',
                                    'PROCEDURE',
                                    'DATAFILE',
                                    'FILESET',
                                    'EXPERIMENT',
                                    ],
                       },
          'ANIMAL'  : {'attrib'  : {'type'   : 'multi',
                                    'name'   : 'animal',
                                    'dbtype' : 'nested',
                                    },
                       'subelem' : [],
                       'parent'  : ['EXPERIMENT'],
                       },
          'PROGRAM' : {'attrib'  : {'type'   : 'multi',
                                    'name'   : 'program',
                                    'dbtype' : 'collection',
                                    },
                       'subelem' : ['PERSON'],
                       'parent'  : ['EXPERIMENT',
                                    'FILESET',
                                    ],
                       },
          'PROCEDURE' : {'attrib'  : {'type'   : 'multi',
                                      'name'   : 'procedure',
                                      'dbtype' : 'collection'
                                      },
                         'subelem' : ['PERSON',
                                      'EXPERIMENT'
                                      ],
                         'parent'  : ['PROJECT'],
                         },
          'DATAFILE' : {'attrib'  : {'type'   : 'multi',
                                     'name'   : 'datafile',
                                     'dbtype' : 'collection',
                                     },
                        'subelem' : ['PERSON'],
                        'parent'  : ['EXPERIMENT',
                                     'FILESET',
                                     ],
                        },
          'EXPERIMENT' : {'attrib'  : {'type'   : 'multi',
                                       'name'   : 'experiment',
                                       'dbtype' : 'collection',
                                       },
                          'subelem' : ['PERSON',
                                       'DATAFILE',
                                       'PROGRAM',
                                       'FILESET',
                                       'ANIMAL',
                                       ],
                          'parent'  : ['PROCEDURE'],
                          },
          'FILESET' : {'attrib' : {'type'   : 'multi',
                                   'name'   : 'fileset',
                                   'dbtype' : 'collection',
                                   },
                       'subelem': ['PROGRAM',
                                   'DATAFILE',
                                   ],
                       'parent' : ['EXPERIMENT'],
                       },

          }


