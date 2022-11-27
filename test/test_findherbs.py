import unittest

from findherbs import findHerbs
from findherbs import loadHerbs

'''
This is first experimentaton for testing the module findherbs

You have to be in ./src folder to start it

----
@todo add better given statements to set up tests
@todo add constants for realistic roles and skills
@todo improve error messages 

'''

class TestFindherbs(unittest.TestCase):
    herbsList = loadHerbs(path=".\data\default\inventory\herbs.csv")

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

if __name__ == '__main__':
    unittest.main()