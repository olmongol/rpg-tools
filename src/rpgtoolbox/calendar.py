#!/usr/bin/env python
'''!
\file /home/mongol/git/rpg-tools/src/rpgtoolbox/calendar.py
\package rpgtoolbox.calendar
\brief date/time module for RPG in-time calenders


\date (C) 2017-2022
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''
__updated__ = "27.12.2022"
__version__ = "1.0"

__me__ = "calendar.py"
__author__ = "Marcus Schwamberger"

import re

monthnames = {
    "Quenya": ["Narviny\u00eb",
               "N\u00e9nim\u00eb",
               "S\u00fal\u00ecm\u00eb",
               "V\u00edress\u00eb",
               "L\u00f3tess\u00eb",
               "N\u00e1r\u00ed\u00eb",
               "Cermi\u00eb",
               "Urim\u00eb",
               "Yavanni\u00eb",
               "Narqueli\u00eb",
               "H\u00edsim\u00eb",
               "Ringar\u00eb"
               ],
    "Sindarin": ["Narwain",
                 "N\u00ednui",
                 "Gwaeron",
                 "Gwirith",
                 "Lothron",
                 "N\u00f3rui",
                 "Cerveth",
                 "Urui",
                 "Ivanneth",
                 "Narbeleth",
                 "Hithui",
                 "Girithron"
                ],
    "Shire":["Afteryule",
             "Solmath",
             "Rethe",
             "Astron",
             "Thrimidge",
             "Forelithe",
             "Afterlithe",
             "Wedmath",
             "Halimath",
             "Winterfilth",
             "Blotmath",
             "Foreyule"
             ],
    "en": ["January",
           "February",
           "March",
           "April",
           "May",
           "June",
           "July",
           "August",
           "September",
           "October",
           "November",
           "December"
           ],
    "de": ["Januar",
           "Februar",
           "März",
           "April",
           "Mai",
           "Juni",
           "Juli",
           "August",
           "September",
           "Oktober",
           "November",
           "Dezember"
           ]
}

weekdaynamess = {"Quenya":["Elenya", "Anarya", "Isilya", "Aldúya", "Menelya", "Valanya or Tárion"],
           "Sindarin":["Orgilion", "Oranor", "Orithil", "Orgaladhad", "Ormenel", "Orbelain or Rodyn"],
           "Shire":["Monday", "Trewsday", "Hevensday", "Mersday", "Highday", "Sterday", "Sunday"],
           "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
           "de": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
           }



class date(object):
    '''!
    This class contains the attributes
    - minutes
    - hours
    - day
    - month
    - year
    - time age
    - day of the week
    '''


    def __init__(self, minute = 0, hour = 12, day = 1, month = 1, year = 1689, age = "2nd Time Age",
                 weekdays = weekdaynamess["Shire"], months = monthnames["Shire"]):
        '''
        \param day number of the day
        \param month number of the month
        \param year number of the year
        \param age name of the time age
        '''
        self.min = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year
        self.age = age

        self.__limitDay = 30
        self.__limitMonth = 12
        self.weekdays = weekdays
        self.months = months
        initday = 0
        #initdate = 1 + (1 - 1) * 30 + (1689 - 1) * 12 * 30
        initdate = self.datestamp(day = 1, month = 1, year = 1689)

        while self.day > self.__limitDay:
            self.month += 1
            self.day -= 1

        while self.month > self.__limitMonth:
            self.year += 1
            self.month -= 12

        # currdate = self.day + (self.month - 1) * 30 + (self.year - 1) * 12 * 30
        currdate = self.datestamp(self.day, self.month, self.year)

        #if initdate < currdate:
        #    datediff = currdate - initdate
        #
        #else:
        #    datediff = initdate - currdate
        #
        #dow = datediff % 7 + initday
        #
        #while dow >= len(self.weekdays):
        #    dow -= 7
        #
        #self.weekday = self.weekdays[dow]

        self.getWeekday(stamp = currdate, initday = initday, initdate = initdate)
        ## @var self.startdate
        # this holds the static start date with which the object was initiated
        self.startdate = {"short": (self.min, self.hour, self.day, self.month, self.year),
                          "full short": (self.weekday, self.min, self.hour, self.day, self.month, self.year)
                          }
        ## @var self.currentdate
        # this saves the dynamic current date & time
        self.currentdate = {"short": [self.min, self.hour, self.day, self.month, self.year],
                            "full short": [self.min, self.hour, self.weekday, self.day, self.month, self.year],
                            "full":[self.min, self.hour, self.weekday, self.day, self.months[self.month], self.year],
                            "date":[ self.day, self.month, self.year],
                            "date full":[self.weekday, self.day, self.months[self.month], self.year]
                          }


    def getWeekday(self, stamp = 1 + (1 - 1) * 30 + (1689 - 1) * 12 * 30, initday = 0, initdate = 1 + (1 - 1) * 30 + (1689 - 1) * 12 * 30):
        """!
        This calculates the day of the week with a given init date and init day
        @param stamp timestamp to calculate the day of the week for
        @param initday weekday for the init day: 0=Mo, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
        @param initdate timestamp of the init date.

        """
        if initdate < stamp:
            datediff = stamp - initdate

        else:
            datediff = initdate - stamp

        dow = datediff % 7 + initday

        while dow >= len(self.weekdays):
            dow -= 7

        ## @var self.weekday
        # holds name of the calculated day of the week.
        self.weekday = self.weekdays[dow]


    def datestamp(self, day, month, year):
        """!
        This calculates a date stamp of a date [d]d.[m]m.yyyy and returns it

        @param day number of the day (in month)
        @param month number of month (in year)
        @param year number of the year
        """
        stamp = day + (month - 1) * 30 + (year - 1) * 12 * 30

        return stamp


    def add(self, add = "20m1h3d2m1y"):
        regex = "([0-9]*m|)([0-9]*h|)([0-9]*d|)([0-9]*M|)([0-9]*y|)"
        check = re.compile(regex)
        re_result = check.match(add)
        adder = {}
        r = " mhdMy"

        for g in range(1, 6):
            adder[r[g]] = re_result.group(g).strip(r[g])

            if adder[r[g]]:
                adder[r[g]] = int(adder[r[g]])

            else:
                adder[r[g]] = 0

        adder["h"] += (self.min + adder["m"]) // 60
        self.min = (self.min + adder["m"]) % 60
        adder["d"] += (self.hour + adder["h"]) // 24
        self.hour = (self.hour + adder["h"]) % 24
        adder["M"] += (self.day + adder["d"]) // 30
        self.day = (self.day + adder["d"]) % 30
        adder["y"] += (self.month + adder["M"]) // 12
        self.month = (self.month + adder["M"]) % 12
        self.year = self.year + adder["y"]
        self.currentdate = {"short": [self.min, self.hour, self.day, self.month, self.year],
                            "full short": [self.min, self.hour, self.weekday, self.day, self.month, self.year],
                            "full":[self.min, self.hour, self.weekday, self.day, self.months[self.month], self.year],
                            "date":[ self.day, self.month, self.year],
                            "date full":[self.weekday, self.day, self.months[self.month], self.year]
                           }

    def showdate(self,option="short"):
        """!
        deliverss a string with time and date
        @param option the options"""
        if option == "short":
            

class time(object):
    '''
    Has to be implemented
    '''


    def __init__(self, hour = 0, min = 0, sec = 0):
        pass



class datetime(date, time):
    '''
    Combined class
    '''


    def __init__(self):
        pass
