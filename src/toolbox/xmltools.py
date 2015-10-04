#!/usr/bin/env python
'''
\file xmltools.py

\brief A collection of tools to generate an XML template for Adamant profiles

This module holds a collection of tools needed for generating, reading and 
verifying XML templates for Adamant Project profiles
\date (C) 2012
\author Marcus Schwamberger    
\email marcus@lederzeug.de
\version 0.5.4 alpha
'''
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__copyright__ = "(c) 2012 Marcus Schwamberger"
__date__ = "2012$"
__version__ = "0.5.4 alpha"

from lxml import etree
import xml.dom.minidom as dom
import sys
from toolbox.lang import *
from toolbox.logbox import *
from toolbox.xmlbox import *

class handleXML(object):
    """
    This class offers methods to convert dictionaries to XML and back.
    It also is able to read XML-Files or save them.
    \param lang supported language for information
    \param xmlstruct XML structure in a dictionary.
    \param filename Name of the file where the XML data shall be read from or
                    written to.  
    \param linkfile name of  a linked structure XML file.
    \param action type of the IO action: read or write.
    """
    def __init__(self,
                 lang = 'en',
                 xmlstruct = {},
                 filename = None,
                 linkfile = None,
                 action = 'r'):
        """
        Class constructor
        """
        self.logger = createLogger(logpath = '/tmp/')
        self.lang = lang
        self.xmlstr = xmlstruct
        self.fname = filename
        self.lfile = linkfile
        self.action = action
        self.filename = filename
        
        if self.filename != None:
            if self.action == 'w':
                if self.lfile == None:
                    self.genXML(self.xmlstr, self.fname)
                else:
                    self.genXML(self.xmlstr, self.fname, "metadata", self.lfile)
            elif self.action == 'r':
                if self.lfile == None:
                    self.readStrucXML(self.fname)
            else:
                raise IOError(errmsg['wr_handle'][self.lang])
                self.logger.error("xmltools: " + errmsg['wr_handle']['en'])
        else:
            raise IOError(errmsg['no_name'][self.lang])
            self.logger.error('xmltools: ' + errmsg['no_name']['en'])
            
    def _findElem(self, elem, parent = []):
        """
        Helper function to find a special node of the tree. It is ment to find 
        the root node in the dictionary structure. The function stops when the 
        first occurrence of a given node parent is found. 
        \param elem The dictionary to search for a node with a given parent.
        \param parent the parent to search for
        \retval the dictionary key of the found node.
        """
        self.elem = elem
        self.parent = parent
        
        for self.key in self.elem:
            if self.elem[self.key]['parent'] == None:
                return self.key
            for self.key2 in self.elem[self.key]['parent']:
                if self.elem[self.key2]['parent'] == self.parent:
                    return self.key2
                        
    def genXML(self, structure = None,
               filename = None,
               dtype = "structure",
               fnmeta = None):
        """
        This method creates XML code from a given dictionary.
        The XML code will be returned and saved into a file if a file name is
        given.
        \param structure A dictionary containing the XML structure and the tag
                           names.
        \param filename Name (and path) of the file where the XML code shall 
                        be stored in.
        \param dtype This holds the information whether a 'structure' or a
                     'metadata' file will be saved.
        \param fn_meta  If a meta data file shall be saved this contains the 
                        linked structure XML file name.
        """
        self.structure = structure
        self.filename = filename
        self.dtype = dtype
        self.fnmeta = fnmeta
        
        if self.filename != None:
            self.__handles = {'structure' : {'parent' : 'PROTOTYPE',
                                             'child'  : 'PROTOTYPE',
                                             },
                              'metadata' : {'parent' : 'STRUCTELEM',
                                            'child'  : 'METAFIELD',
                                            },
                              }
            self.prj = {}
            
            if self.dtype.lower() == 'metadata':
                self.start = etree.Element('TEMPLATE',
                                           name = 'metadata',
                                           strucfile = self.fnmeta)
                self.doc = etree.ElementTree(self.start)
                self.prj['start'] = self.start
                
                for self._parent in self.structure:
                    self.prj[self._parent] = etree.SubElement(self.start,
                                                              self.__handles[self.dtype]['parent'],
                                                              {'name': self._parent})
                    
                    for self._label in self.structure[self._parent]:
                        self._dummy = self.structure[self._parent][self._label]
                        self._dummy.update({'label':self._label})
                        etree.SubElement(self.prj[self._parent],
                                         self.__handles[self.dtype]['child'],
                                         self._dummy)
                        
            elif self.dtype.lower() == 'structure':
                self.start = etree.Element('TEMPLATE', name = 'structure')
                self.dtype = 'structure'
                self.doc = etree.ElementTree(self.start)
                self.root = self._findElem(self.structure, [])
                self.parent = self.root
                self.parentList = [self.parent]
                self.prj['start'] = self.start
                self.prj[self.root] = etree.SubElement(self.start,
                                                       self.__handles[self.dtype]['parent'],
                                                       self.structure[self.root]['attrib'])
                self.elementList = list(self.structure[self.parent]['subelem'])
                
                while self.parentList != []:
                    self.subList = []
                    self.elementList = self.structure[self.parent]['subelem']
                   
                    for self.entry in self.elementList:
                        self.subList += self.structure[self.entry]['subelem']
                        self.prj[self.entry] = etree.SubElement(self.prj[self.parent],
                                                                self.__handles[self.dtype]['child'],
                                                                self.structure[self.entry]['attrib'])
                        
                    if self.parentList != []:
                        self.parentList.remove(self.parent)
                    
                    if self.parentList == [] and self.subList != []:
                        self.parentList = list(self.structure[self.parent]['subelem']) 
                           
                        for self.key in self.parentList:
                            if self.structure[self.key]['subelem'] == []:
                                self.parentList.remove(self.key)
                        
                    if self.parentList != []:        
                        self.parent = self.parentList[0]
                
            if filename != '':
                self.fp = open(self.filename, 'a')
                self.doc.write(self.filename, pretty_print = True)
                self.fp.close()   

        else:
            raise IOError(errmsg['no_name'][self.lang])
            self.logger.error('xmltools: ' + errmsg['no_name']['en'])

    def readStrucXML(self, filename = None):
        """
        This method reads a XML file which holds a Adamant functional data 
        structure and converts the content into a dictionary.
        \param filename Path and file containing the XML code
        \return dic A dictionary with the right structure
        """
        self.filename = filename
        self.dic = {}
        
        if self.filename != None and self.filename != '':
            self.doc = etree.parse(self.filename)
            self.walk = self.doc.getiterator()
            
            for self.key in self.walk:
                self.attrib = self.key.attrib
                self.d_key = self.attrib['name'].upper()
                self.dic[self.d_key] = {'attrib' : self.attrib,
                                        'parent' : []
                                        }         
                self.children = []
                
                for self.kid in self.key.getchildren():
                    self.children.append(self.kid.attrib['name'].upper())
                    
                self.dic[self.d_key]['subelem'] = self.children
                
            del(self.dic['STRUCTURE'])
            
            for self.key1 in self.dic:
                for self.key2 in self.dic[self.key1]['subelem']:
                    self.dic[self.key2]['parent'].append(self.key1)
        else:
            raise IOError(errmsg['no_name'][self.lang])
            self.logger.debug('xmltools: ' + errmsg['no_name']['en'])                

        return self.dic
    
    def readMetaXML(self, filename = None):
        """
        This method reads out a XML file which holds the Adamant meta data field
        structure and converts it into a dictionary.
        \param filename Path and file name of the XML file
        return dic A dictionary that holds the data with the right stucture
        """
        self.filename = filename
        self.dic = {}
        if self.filename != None and self.filename != '':
            self.doc = etree.parse(self.filename)
            self.walk = self.doc.getiterator()
            
            for self.struc in self.walk:
                self.attrib = self.struc.attrib
                self.d_key = self.attrib['name'].upper()
                
                for self.label in self.struc.getchildren():
                    self.attrib2 = self.label.attrib
                    self.d2_key = self.attrib2['name']
                    if self.d2_key != '':
                        if self.d2_key.upper() == self.d2_key:
                            self.dic[self.d2_key] = {}
                        for self.at in self.label.getchildren():
                            self.attrib3 = self.at.attrib
                            self.d3_key = self.attrib3['label']
                            try: 
                                type(self.dic[self.d2_key][self.d3_key]) == type({})
                            except:
                                if self.d3_key != '':
                                    self.dic[self.d2_key][self.d3_key] = {}
        
                            self.dic[self.d2_key][self.d3_key]['type'] = self.attrib3['type']
                            self.dic[self.d2_key][self.d3_key]['display'] = self.attrib3['display']
                            self.dic[self.d2_key][self.d3_key]['name'] = self.attrib3['name']
                            self.dic[self.d2_key][self.d3_key]['list'] = self.attrib3['list']

        else:
            raise IOError(errmsg['no_name'][self.lang])
            self.logger.error('xmltools: ' + errmsg['no_name']['en'])  
                                      
        return self.dic
                        
def findElem(elem, parent):
    """
    Helper function to find the (root) node of the tree structure embedded in a
    dictionary.
    \param elem   A dictionary that holds the data structure of an ADaManT 
                  project.
    \param parent This contains the parent to look for. The function will stop
                  when the first is found.
    \retval The key of the dictionary which belongs to the found node.
    """
    for key in elem:
        if elem[key]['parent'] == None:
            return key
        for key2 in elem[key]['parent']:
            if elem[key2]['parent'] == parent:
                return key2


def genXML(elem, filename = ''):
    """
    This function generates an XML document from a given dictionary.
    \param elem  A dictionary to parse for building the XML. It holds a special
                 structure for easier build of the XML template.
    \param filename Path and filename where to save the XML code in. If it is 
                    not given the XML code will be written to stdout.
    """
       
    prj = {}
    start = etree.Element('TEMPLATE', name = 'structure')
    doc = etree.ElementTree(start)
    root = findElem(elem, [])
    
    parent = root
    parentList = [parent]
    prj['start'] = start
    prj[root] = etree.SubElement(start,
                                'PROTOTYPE',
                                elem[root]['attrib'])
    elementList = list(elem[parent]['subelem'])
    
    while parentList != []:
        subList = []
        elementList = elem[parent]['subelem']
       
        for entry in elementList:
            subList += elem[entry]['subelem']
            prj[entry] = etree.SubElement(prj[parent],
                                         'PROTOTYPE',
                                         elem[entry]['attrib'])
            
        if parentList != []:
            parentList.remove(parent)
        
        if parentList == [] and subList != []:
            parentList = list (elem[parent]['subelem']) 
               
            for key in parentList:
                if elem[key]['subelem'] == []:
                    parentList.remove(key)
            
        if parentList != []:        
            parent = parentList[0]
        
    if filename != '':
        fp = open(filename, 'a')
        doc.write(filename, pretty_print = True)
        fp.close()   
        
        
def getXML(filename = ''):
    """
    getXML reads a XML file and checks whether it is conform to the ADaManT 
    profile structure.
    \param filename This parameter holds the path and filename of the XML file
                    to be read.
    \retval result  This dictionary holds the XML information.
    """
    result = {}
    
    if filename == '':
        raise IOError('Empty Filename!!')
        return result
    
    fp = open(filename, 'r')
    content = fp.readlines()
    fp.close()
    
    return content
    
    
    
