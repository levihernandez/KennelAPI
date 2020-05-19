import unittest
from kennel import Kennel as kn

class TestKennel(unittest.TestCase):
    def test_readconf(self):
        argument = "create_dashboard"
        cnffile = '../DataDogApi/config/' + argument + '.conf'
        kclass = kn(cnffile)
        self.assertEqual(kclass.readconf())


if __name__ == '__main__':
    unittest.main()
