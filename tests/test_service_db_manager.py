import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
import pandas as pd

import constants as cta
import Models.Query as mod_query
import src.Services.database as db

class DatabaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFile = "./tests/test_folders/test_local_DB/queries.json"
        cls.dbManager = db.DatabaseManager(cls.mockFile)

    # def setUp(self):
    #     self.dbManager.clearDB()
    
    
    # def tearDown(self):
    #     self.dbManager.clearDB()


    def test_init(self):
        self.assertIsNotNone(self.dbManager.queriesLocalDB)


    def test_add_query(self):
        self.dbManager.clearDB()

        exQuery = mod_query.Query()        
        self.dbManager.addQueryToDB(exQuery)
        res = self.dbManager.getQueriesFromDB()

        self.assertEqual(len(res), 1)

        self.dbManager.clearDB()


    def test_get_queryId(self):
        self.dbManager.clearDB()

        exQuery = mod_query.Query()        
        self.dbManager.addQueryToDB(exQuery)

        res = self.dbManager.getQueriesFromDB()
        query = self.dbManager.getQueryById(res[0]["id"])

        self.assertEqual(query, res[0])

        self.dbManager.clearDB()


    def test_edit_name(self):
        self.dbManager.clearDB()

        exQuery = mod_query.Query()        
        self.dbManager.addQueryToDB(exQuery)

        res = self.dbManager.getQueriesFromDB()
        query = self.dbManager.getQueryById(res[0]["id"])

        self.dbManager.editQueryName(query["id"], "itssover")

        res2 = self.dbManager.getQueriesFromDB()

        self.assertEqual(res2[0]["name"], "itssover")

        self.dbManager.clearDB()


    def test_delete_query(self):
        self.dbManager.clearDB()

        exQuery = mod_query.Query()
        self.dbManager.addQueryToDB(exQuery)

        res = self.dbManager.getQueriesFromDB()
        query = self.dbManager.getQueryById(res[0]["id"])
        queryId = query["id"]

        self.dbManager.deleteQueryByID(queryId)

        res2 = self.dbManager.getQueriesFromDB()

        self.assertEqual(len(res2), 0)

        self.dbManager.clearDB()


    def test_dataframe_creation_valid_df(self):
        exQuery = mod_query.Query()
        res = self.dbManager.createDataframe(exQuery)

        self.assertIsNotNone(res)
    
    
    def test_dataframe_creation_invalid_df(self):
        exQuery = None
        res = self.dbManager.createDataframe(exQuery)

        self.assertTrue(res.empty)



if __name__ == '__main__':
    unittest.main(verbosity=2)