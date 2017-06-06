#!/usr/bin/env python
'''
\file /home/mongol/git/rpg-tools/src/rpgtoolbox/calendar.py
\package rpgtoolbox.calendar
\brief date/time module for RPG in-time calenders


\date (C) 2017
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''

class date(object):
    '''
    This class contains the attributes
    - day
    - month
    - year
    - time age
    - day of the week
    '''
    def __init__(self, day = 1, month = 1, year = 1689, age = "2nd Time Age"):
        '''
        \param day number of the day
        \param month number of the month
        \param year number of the year
        \param age name of the time age
        '''
        self.day = day
        self.month = month
        self.year = year
        self.age = age
        
        self.__limitDay = 30
        self.__limitMonth = 12
        weekdays = ('MO',
                    'DI',
                    'MI',
                    'DO',
                    'FR',
                    'SA',
                    'SO')
        initday = 0
        initdate = 1 + (1 - 1) * 30 + (1689 - 1) * 12 * 30
        
        while self.day > self.__limitDay:
            self.month += 1
            self.day -= 1
            
        while self.month > self.__limitMonth:
            self.year += 1
            self.month -= 12
            
        currdate = self.day + (self.month - 1) * 30 + (self.year - 1) * 12 * 30
        
        if initdate < currdate:
            datediff = currdate - initdate
        
        else:
            datediff = initdate - currdate
        
        dow = datediff % 7 + initday
        while dow >= len(weekdays):
            dow -= 7
            
        self.weekday = weekdays[dow]
            
