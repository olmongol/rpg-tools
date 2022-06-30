import unittest

# importing sys
import sys
  
# adding src to the system path
sys.path.append('C:\\Users\\Nillorian\\coding\\projects\\rpg-tools\\src')

from findherbs import sumDices
from findherbs import findHerbs

class TestFactorial(unittest.TestCase):
    def test_aOneSidedDieAlwaysSumsToOne(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        res = sumDices(1,1)
        self.assertEqual(res, 1)

    def test_twoD20AlwaysInBetween2and40(self):
        res = sumDices(20,2)
        self.assertGreater(res,1)
        self.assertGreater(41,res)

    def test_findHerbs(self):
        herbs = [{
            'type': 'Concussion Relief', 
            'area': 'everywhere', 
            'climate': 'mild temperate', 
            'locale': 'grasslands', 
            'difficulty': 'light', 
            'form': 'Leaf', 
            'prep': 'Ingest', 
            'AF': '0', 
            'lvl': '1', 
            'name': 'Abaas', 
            'description': ' ', 
            'medical use': 'Heals 2-12 hit points.', 
            'worth': {'mithril': 0, 'platinium': 0, 'gold': 0, 'silver': 0, 'bronze': 0, 'copper': 3, 'tin': 0, 'iron': 0}, 
            'weight': 0.1, 
            'location': 'equipped'
            }]
        res = findHerbs(herbs, 100, 50, "everywhere", "mild temperate", "grasslands")
        print(res)
       

if __name__ == '__main__':
    unittest.main()