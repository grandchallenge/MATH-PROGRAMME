import unittest
from ci.validate_gcl_erdos3_programme import validate

class GclErdos3ProgrammeTest(unittest.TestCase):
    def test_registration(self):
        self.assertEqual(validate(),[])

if __name__=='__main__':
    unittest.main()
