#!/usr/bin/env python

'''
\package toolbox
\file globaltools.py

\brief a bunch of nice global tools.

This module holds some nice small helper functions like I/O things.

\author Marcus Schwamberger
\date (c) 2012
\version 0.5.4 alpha
\email marcus@lederzeug.de
'''

__msg__ = {'ERR_NO_DATA'     : "ERROR: no data to compute :(",
           'ERR_NO_FILENAME' : "ERROR: no file name :(",
           'ERR_WRONG_TYPE'  : "ERROR: wrong data/variable type",
           'ERR_WRONG_MODE'  : "ERROR: wrong FS I/O mode!",
           'OK'              : "OK: job is done :D"
          }


import os
import os.path



def readFile(path = './', file_name = None, mode = 'r'):
    '''
    This function reads a file and returns its content.
    This function is designed to read files from a file system. It knows two 
    modes of reading: text and binary mode.

    @param path path to the file
    @param file_name name of the file
    @param mode reading mode of the file: r = text; rb = binary
    \return error message or content of the file
    '''

    if mode != 'r' and mode != 'rb':
        return(__msg__['ERR_WRONG_MODE'])

    if file_name == None:
        print(__msg__['ERR_NO_FILENAME'])
        return(__msg__['ERR_NO_FILENAME'])

    if os.name == 'posix' or os.name == 'mac':
        if path[-1] != '/' and file_name[1:] != '/':
            path = path + '/'
    elif os.name == 'nt':
        if path[-1] != '\\' and file_name[1:] != '\\':
            path = path + '\\'
    
    fp = open(path + file_name, mode)
    content = fp.readlines()
    fp.close()
    
    for i in range(len(content)):
        content[i] = content[i].strip('\n')
    
    return content

def writeFile(path = './', file_name = 'output', data = None, mode = 'w'):
    '''
    This function simply (over)writes a file with given data.
    This function is designed to dump some data into a file. It is possible to
    write binary files or text files.

    @param path path to file
    @param file_name name of the file to be saved (default: output)
    @param data data to be saved. The accepted data format are arrays or strings
    @param mode write mode of the file. Default is 'w' --> text file
    
    \return error message or ok state
    '''

    if mode != 'w' and mode != 'wb':
        return __msg__['ERR_WRONG_MODE']
    if data == None:
        print __msg__['ERR_NO_DATA']
        return __msg__['ERR_NO_DATA']

    if type(data) == type([]):
        content = ""
        for key in data:
            content = content + str(key) + '\n'
    elif type(data) == type(""):
        content = data
    elif type(data) == type(1) or type(data) == type(1.1):
        content = str(data)
    else:
        print __msg__['ERR_WRONG_TYPE']
        return __msg__['ERR_WRONG_TYPE']
    
    if os.name == 'posix' or os.name == 'mac':
        if path[-1] != '/' and file_name[1:] != '/':
            path = path + '\\'

    f = open(path + file_name, mode)
    f.write(content)
    f.close()

    return __msg__['OK']

def checkFiles(path = './', file_list = []):
    """
    This function check out whether a list of files exists in a specific 
    directory.
    
    \param path Path to be searched for the files
    \param file_list an array containing the list of filenames to search for.
    
    \retval result a dictionary which holds the filename as key and False/True
                   as value. If the path does not exist it contains just 
                   {'path':False}
    """
    
    result = {}
    if os.name == 'posix' and path[-1] != '/':
        path += '/'
    if os.path.exists(path):
        for key in file_list:
            if os.path.isfile(path + key):
                result[key] = True
            else:
                result[key] = False
    else:
        result = {'path' : False}
    
    return result
        
def sortIndex(dic = {}):
    """
    \brief This function is a little helper when sorting a dictionary.

    This function gets a dictionary and gives back the dictionary index as a
    sorted array. With that the content of a dictionary in Python can be shown
    in alphabetical order.

    \param dic a dictionary whose index shall be sorted
    \retval index an array with the sorted index of the given dictionary dict
    """
    index = dic.keys()
    index.sort()
    return index

def array2dict(array = [], expr = '=', comment = '#'):
    """
    This function transforms an array <str1>=<str2> into a dictionary 
    { <str1> : <str2>}
    
    \param array the array which shall be transformed
    \param expr the character where the string shall be split; default is '='
    \param comment this parameter holds the comment character to filter 
                   comments out.
    \retval result a dictionary
    """
    result = {}
    
    if type(array) != type([]):
        return result
    
    for i in range(len(array)):
        if comment not in array[i]:
            if expr in array[i]:
                dummy = array[i].split(expr)
                dummy[0] = dummy[0].strip(" ")
                dummy[1] = dummy[1].strip(" ")
                result[dummy[0]] = dummy[1]
    return result

def list2str(array = []):
    """
    This function transforms a list/tuple into a string where the elements are
    separated by spaces.
    \param array List/tupel to be transformed to string
    \retval result string which holds the elements space separated
    """
    if type(array) == type([]) or type(array) == type(()):
        result = ''
        for key in array:
            result += str(key) + " "
            
        result = result.strip()
    return result 

def tstr2list(string = '(1,2,3)'):
    """
    This function transforms a string which 'looks like a tuple' into a list
    \param string input 'tuple' string
    \retval result list of 'tuple' string elements
    """
    result = string.strip()
    result = result.strip('()')
    result = result.split(',')
    
    i = 0
    
    while i < len(result):
        result[i] = result[i].strip(' \"\'')
        i += 1
    return result

def makeKeyList(dic = {}, klist = []):
    '''
    This function simply extracts/compares the key index of a given dictionary
    with a list. If the list is lacking entries they will be added from the key
    index. Finally, the list will be returned and compared with the index list.
    \param dic dictionary to check
    \param klist keylist which shall be compared with the dictionary index
    \return klist generated/completed list
    \return fit Boolean whether index and key list are the same.
    '''
    for key in dic:
        if key not in klist:
            klist.append(key)
            
    __dummy = dic.keys()
    if __dummy.sort() == klist.sort():
        return klist, True
    else:
        return klist, False 
    
    
def countElem (elem = '', alist = []):
    '''
    This tiny functions just count the occurrences of an element in a
    list.
    \param elem the element that shall be checked in the list
    \param alist the list where the element shall be counted in
    \return counter counted occurrences of the element in the list
    '''
    counter = 0
    
    for item in alist:
        if item == elem:
            counter += 1
            
    return counter


def findLoops(struc = {}, elem = '', way = [], result = []):
    '''
    This function looks for loops in a tree structure. The given dictionary
    must have the following structure dic[struc_item]['subelem']. It runs
    recusively through the structure tree.
    Further it will change the global variable \e loops.
    \param struc tree in a dictionary which shall be searched for loop 
                 structures.
    \param elem element of the structure tree where to start the search for
                loops.
    \param way  The path which were actually run through in the tree.
    \param result contains loops as a list of tuples.
    \bug this function finds sometimes loops where no loops are... it 
         seems to concern multiple links to leaves...
    '''
    myway = way
    mytree = struc
    
    for key in mytree[elem]['subelem']:

        if key == []:
            pass
        
        else:
            
            if countElem(key, myway) < 1:
                myway.append(key)
                findLoops(mytree, key, myway, result)
                myway.pop()
                
            else:
                
                if key in mytree[myway[-1]]['subelem']:
                    result.append((list(myway), key))
                
                break
    return result

def asciLoops(way = [], element = ""):
    '''
    This is a small helper function to display a loop from a list as
    'asci'.
    \param way the way which was run through when the loop was found
    \param element the element which causes the loop
    \retval a string containing the asci display of the loop 
    '''
    result = ""
    for key in way:
        if key == element:
            result += '\n======> ' + key
        else:
            result += '\n' + key
    
    result += '\n======> ' + element
    return result

def checkExist(arg = ""):
    '''
    This function checks whether given argument (object/variable/list...)
    already exists or not.
    \param arg a string that holds the name of the object, variable, list etc.
    \return It delivers 'globals' if it is found in globals(), 'locals'
            if it is found in locals() or False if it is not found.
    '''
    if arg != "" and type(arg) == type(""):
        print "locals", locals().keys()
        print "\n globals", globals().keys()
        if arg in locals():
            return "locals"
        elif arg in globals():
            return "globals"
        else:
            return False
        
def getLast(string = "/", sep = '/'):
    '''
    This function gives the last element of a list stored in a string.
    \param string where the list is stored.
    \param sep seperator of the list elements. E.g., '/' or ','
    \return last element of the list.
    '''
    dummy = string.split(sep)
    return str(dummy[-1].split())
    
