import unittest

from findherbs import findHerbs

'''
This is first experimentaton for testing the module findherbs

Findings:
'''

class TestFindherbs(unittest.TestCase):
    def test_shouldFindHerbsWithArea(self):
        print("test_shouldFindHerbsWithArea")
        areyWhereIsSearched = "";
        result = findHerbs(roll=200, area=areyWhereIsSearched)
        print(result);  
        
        self.assertGreater(result, 1)

if __name__ == '__main__':
    unittest.main()