import unittest

from findherbs import findHerbs
from findherbs import loadHerbs

'''
This is first experimentaton for testing the module findherbs

You have to be in ./src folder to start it

roll	classification
 < -26	Spectacular Failure
-25 < 04	Absolute Failure
05 < 75	Failure
UM < 66	Unusual Event
76 < 90	Partial Success
91 < 110	Near Success
UM < 100	Unusual Success
111 < 175	Success
176 < 	Absolute Success


----
@todo add better given statements to set up tests
@todo add constants for realistic roles and skills
@todo improve error messages 

'''

class TestFindherbs(unittest.TestCase):
    herbsList = loadHerbs(path="./data/default/inventory/herbs.csv")

    def test_shouldFindHerbsIn(self, list=herbsList):
        # given
        searcherHasNoSkill = -15
        rollIsMaximum = 200 
        areyWhereIsSearched = ["Arnor"]
        climateWhereIsSearched = ["cold"]
        localeWhereIsSearched = ["mountains"]

        #when
        result = findHerbs(list, skill=searcherHasNoSkill, roll=rollIsMaximum, area=areyWhereIsSearched, climate=climateWhereIsSearched, locale=localeWhereIsSearched)
        
        #then
        self.assertTrue(msg="The result should have at least a result", expr=(result != []) )

    def test_shouldFindHerbsIn(self, list=herbsList):
        # given
        searcherHasNoSkill = -15
        rollIsMaximum = 200 
        areyWhereIsSearched = ["Dagorlad"]
        climateWhereIsSearched = ["cold"]
        localeWhereIsSearched = ["mountains"]

        #when
        result = findHerbs(list, skill=searcherHasNoSkill, roll=rollIsMaximum, area=areyWhereIsSearched, climate=climateWhereIsSearched, locale=localeWhereIsSearched)
        
        #then
        self.assertTrue(msg="The result should have at least a result", expr=(result != []) )

#Thurl	Concussion Relief	northeastern Eriador	cool temperate	decidous/mixed forest	routine	Clove	Brew	3tp	0		Heals 1-4 hit points. Brew keeps 1-2 weeks.

    def test_shouldFindHerbsIn(self, list=herbsList):
        # given
        searcherHasNoSkill = 50
        rollIsMaximum = 50
        areyWhereIsSearched = ["northeastern Eriador"]
        climateWhereIsSearched = ["cool temperate"]
        localeWhereIsSearched = ["decidous/mixed forest"]

        #when
        result = findHerbs(list, skill=searcherHasNoSkill, roll=rollIsMaximum, area=areyWhereIsSearched, climate=climateWhereIsSearched, locale=localeWhereIsSearched)
        
        #then
        self.assertTrue(msg="The result should have at least a result", expr=(result != []) )

if __name__ == '__main__':
    unittest.main()