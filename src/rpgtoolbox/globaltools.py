#!/usr/bin/env python

'''
\package rpgtoolbox
\file globaltools.py

\brief a bunch of nice global tools.

This module holds some nice small helper functions like I/O things.

\author Marcus Schwamberger
\date (c) 2012-2018
\version 0.5.4
\email marcus@lederzeug.de
\todo checkout whether all functions are really needed for this project.
'''

__msg__ = {'ERR_NO_DATA'     : "ERROR: no data to compute :(",
           'ERR_NO_FILENAME' : "ERROR: no file name :(",
           'ERR_WRONG_TYPE'  : "ERROR: wrong data/variable type",
           'ERR_WRONG_MODE'  : "ERROR: wrong FS I/O mode!",
           'OK'              : "OK: job is done :D"
          }

import os
import os.path
from . import logbox as log
import csv
import json

logger = log.createLogger('global', 'warning', '1 MB', 1, './' , 'globaltools.log')



def readFile(path = './', file_name = None, mode = 'r'):
    '''
    This function reads a file and returns its content.
    This function is designed to read files from a file system. It knows two
    modes of reading: text and binary mode.

    @param path path to the file
    @param file_name name of the file
    @param mode reading mode of the file: r = text; rb = binary
    @return error message or content of the file
    '''

    if mode != 'r' and mode != 'rb':
        logger.warning('readFile: %s' % (__msg__['ERR_WRONG_MODE']))
        return(__msg__['ERR_WRONG_MODE'])

    if file_name == None:
        print((__msg__['ERR_NO_FILENAME']))
        logger.error('readFile: %s' % (__msg__['ERR_NO_FILENAME']))
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
    logger.debug('readFile %s' % (path + file_name))

    for i in range(len(content)):
        content[i] = content[i].strip('\n')

    logger.debug('readFile: cleaned file content')
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

    @return error message or ok state
    '''

    if mode != 'w' and mode != 'wb':
        logger.warning('writeFile: %s' % (__msg__['ERR_WRONG_MODE']))
        return __msg__['ERR_WRONG_MODE']

    if data == None:
        print(__msg__['ERR_NO_DATA'])
        logger.error('writeFile: %s' % (__msg__['ERR_NO_DATA']))
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
        logger.error('writeFile: %s' % (__msg__['ERR_WRONG_TYPE']))
        print(__msg__['ERR_WRONG_TYPE'])
        return __msg__['ERR_WRONG_TYPE']

    if os.name == 'posix' or os.name == 'mac':

        if path[-1] != '/' and file_name[1:] != '/':
            path = path + '\\'

    f = open(path + file_name, mode)
    f.write(content)
    f.close()
    logger.info('writeFile: %s' % (__msg__['OK']))
    return __msg__['OK']



def checkFiles(path = './', file_list = []):
    """
    This function check out whether a list of files exists in a specific
    directory.

    @param path Path to be searched for the files
    @param file_list an array containing the list of filenames to search for.

    @retval result a dictionary which holds the filename as key and False/True
                   as value. If the path does not exist it contains just
                   {'path':False}
    """

    result = {}
    if os.name == 'posix' and path[-1] != '/':
        path += '/'
    if os.path.exists(path):

        if type(file_list) == type([]):

            for key in file_list:

                if os.path.isfile(path + key):
                    result[key] = True

                else:
                    result[key] = False

        elif type(file_list) == type(""):

            if os.path.isfile(path + file_list):
                result[file_list] = True

        else:
            result[str(file_list)] = False

    else:
        result = {'path' : False}

    return result



def sortIndex(dic = {}):
    """
    \brief This function is a little helper when sorting a dictionary.

    This function gets a dictionary and gives back the dictionary index as a
    sorted array. With that the content of a dictionary in Python can be shown
    in alphabetical order.

    @param dic a dictionary whose index shall be sorted
    @retval index an array with the sorted index of the given dictionary dict
    """
    index = list(dic.keys())
    index.sort()
    return index



def array2dict(array = [], expr = '=', comment = '#'):
    """
    This function transforms an array <str1>=<str2> into a dictionary
    { <str1> : <str2>}

    @param array the array which shall be transformed
    @param expr the character where the string shall be split; default is '='
    @param comment this parameter holds the comment character to filter
                   comments out.
    @retval result a dictionary
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
    @param array List/tupel to be transformed to string
    @retval result string which holds the elements space separated
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
    @param string input 'tuple' string
    @retval result list of 'tuple' string elements
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
    @param dic dictionary to check
    @param klist keylist which shall be compared with the dictionary index
    @return klist generated/completed list
    @return fit Boolean whether index and key list are the same.
    '''
    for key in dic:
        if key not in klist:
            klist.append(key)

    __dummy = list(dic.keys())
    if __dummy.sort() == klist.sort():
        return klist, True
    else:
        return klist, False



def writeJSON(filename = "", content = {}):
    '''
    This function writes a dictionary into a JSON file.

    @param filename  path+file where to save the data in
    @param content dictionary which shall be saved as JSON content.
    '''
    try:
        with open(filename, "w") as fp:
            json.dump(content, fp, indent = 4)
        logger.info("%s saved" % filename)

    except:
        logger.error("%s could not be saved!" % filename)



def readJSON(filename):
    '''
    This function reads JSON files into a dictionary.

    @param filename path+file of the JSON file to read.
    '''
    try:
        with open(filename, 'r') as fp:
            content = json.load(fp)

        logger.info('%s loaded.' % filename)
    except:
        content = {}
        logger.error("Could not load %s" % filename)

    return content



def getLast(string = "/", sep = '/'):
    '''
    This function gives the last element of a list stored in a string.
    @param string where the list is stored.
    @param sep separator of the list elements. E.g., '/' or ','
    @return last element of the list.
    '''
    dummy = string.split(sep)
    return str(dummy[-1].split())



def readCSV(fname = "test.csv"):
    '''
    This function reads a CSV file and returns a dictionary
    @param fname name (and path) of the CSV file
    @retval result a list containing dictionaries with keys from CSV header line
    ----
    @todo handle problems with wierd unicode characters
    '''
    result = []
    with open(fname, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    csvfile.close()
    return result



def getCSVNames(chkpath = "data/default/fight/attacks"):
    """
    This returns a list of CSV files from a path, but CSVs <name>-.csv are excluded
    too
    @param chkpath path to search for the CSV file names
    @reval result list of CSV filenames
    """
    result = []
    dummy = os.listdir(chkpath)

    for elem in dummy:
        if ".csv" in elem and "-.csv" not in elem:
            result.append(elem)

    result.sort()
    return result



def sortTupleList(tuplelist, sortindex = 0, desc = True):
    """
    This sorts a list of tuples by the given index.
    @param tuplelist list of the tuples
    @param sortindex index of tuple by which list should be sorted
    @param desc determines whether list shall be sorted descending (true/false)
    """
    tuplelist.sort(key = lambda x:x[sortindex], reverse = desc)



def splitExceptBetween(inputstr = 'bla,fasel', delimiter = ',', quotes = '"'):
    '''
    This function splits a string into a list by delimiter but excepts delimiters
    placed between quotes
    @param inputstr string to split into a list
    @param delimiter for the elements to separate into list
    @param quotes to mark areas which should not be separated even if delimiters
           are inside.
    @retval result the separated list.
    '''
    inside = -1
    result = []
    oldt = 0

    for index, letter in enumerate(inputstr):

        if letter == quotes:
            inside = -inside

        elif letter == delimiter and inside == -1:
            result.append(inputstr[oldt:index])
            oldt = index + 1

    if oldt < len(inputstr):
        result.append(inputstr[oldt:])

    if inputstr[-1] == delimiter:
        result.append("")

    return result



def writeCSV(fname = "test.csv", cont = [{'Spam' : 'Ham'}, {'Spam':'eggs'}]):
    '''
    This function creates a CSV file from a given list of dictionaries
    @param fname file name of the CSV
    @param cont list of dictionaries
    '''
    header = list(cont[0].keys())
    with open(fname, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = header)

        writer.writeheader()
        for myrow in cont:
            writer.writerow(myrow)

    csvfile.close()



def readMagic(root = "./data/default/magic", slgroup = None):
    '''
    This function runs trough the magic root dir and collects the spell list groups
    (dirs) and the names of the spell lists (files). It filters if a spell list
    group is given.
    @param root root dir from where to start the walk trough. Ususally the dir
                ./data/default/magic
    @param slgroup a single spell list group (for filtering purposes)
    @return dictionary with SL group(s) as key and SL names as value list.
    \deprecated it is now implemented in handlemagic.py
    '''
    magiclists = {}

    for path, dirs, files in os.walk(root):

        if root != path:
            magiclists[path.replace("_", " ").strip(root)] = files

    if slgroup:
        return {slgroup: magiclists[slgroup]}

    else:
        return magiclists
