import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
import pandas as pd

import constants as cta
import Models.Exceptions as exc
import Models.Query as query
import src.Services.database as db

class DatabaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFile = "./tests/test_folders/test_local_DB/queries.json"
        cls.dbManager = db.DatabaseManager(cls.mockFile)

    def setUp(self):
        self.dbManager.clearDB()
    
    
    def tearDown(self):
        self.dbManager.clearDB()


    def test_init(self):
        self.assertIsNotNone(self.dbManager.queriesLocalDB)


    def test_add_query(self):
        exQuery = query.Query()        
        self.dbManager.addQueryToDB(exQuery)
        res = self.dbManager.getQueriesFromDB()

        self.assertEqual(len(res), 1)


    def test_dataframe_creation_valid_query(self):
        exQuery = query.Query()
        res = self.dbManager.createDataframe(exQuery)

        self.assertIsNotNone(res)
    
    
    def test_dataframe_creation_invalid_query(self):
        exQuery = None
        res = self.dbManager.createDataframe(exQuery)

        self.assertTrue(res.empty)



if __name__ == '__main__':
    unittest.main(verbosity=2)