import unittest

import main
import constants as cta

class SQLAnalyticsMainTest(unittest.TestCase):

    def test_all_files_exist(self):
        '''Check if the Orcale Instant Client folder exits - it's necessary for thick mode'''
        
        self.assertTrue(main.checkIfAllFilesExist())

    def test_one_missing_file(self):
        badFile = "blah blah"

        self.assertFalse(main.resource_path(badFile))

if __name__ == '__main__':
    unittest.main(verbosity=2)
