import unittest

import src.Services.prerun_set as prerun
import src.Services.database as db

class PrerunTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFile = ".tests/prerun_test_folders/test_local_DB/queries.json"
        cls.dbManager = db.DatabaseManager(cls.mockFile)
    

    def test_folders_creation(self):
        prerun.createFoldersIfNotExist(
          "tests/prerun_test_folders/test_local_DB",
          "tests/prerun_test_folders/test_logs",
          "tests/prerun_test_folders/test_settings"
        )  

        # with self.assertRaises(Exception) as context:
        #     prerun.createFoldersIfNotExist(
        #       "tests/prerun_test_folders/test_local_DB",
        #       "tests/prerun_test_folders/test_logs",
        #       "tests/prerun_test_folders/test_settings"
        #     ) 
    
    