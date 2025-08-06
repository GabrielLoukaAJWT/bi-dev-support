import unittest
from unittest import mock
from unittest.mock import patch, MagicMock

import constants as cta
import Models.Exceptions as exc
import Models.Query as query
import src.Services.logging as log

class LoggingTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFile = "./tests/test_folders/test_logs/queries.log"
        cls.loggingManager = log.QueryLoggerManager(cls.mockFile)

    def setUp(self):
        self.loggingManager.clearLogsFile()

    def tearDown(self):
        self.loggingManager.clearLogsFile()

    
    def test_init(self):
        self.assertIsNotNone(self.loggingManager.logger)

    
    def test_new_log_added(self):
        exQuery = query.Query()
        self.loggingManager.addLog("info", exQuery, "")
        res = self.loggingManager.getQueriesFromFile(self.mockFile)

        self.loggingManager.addLog("error", exQuery, "errrrrrrrr")
        res = self.loggingManager.getQueriesFromFile(self.mockFile)

        self.assertEqual(len(res), 2)

        self.loggingManager.addLog("no type", exQuery, "errrrrrrrr")
        res = self.loggingManager.getQueriesFromFile(self.mockFile)
        
        self.assertEqual(len(res), 2)

    
    def test_bad_file(self):
        self.mockFile = "badfile"
        res = self.loggingManager.getQueriesFromFile(self.mockFile)

        self.assertEqual(res, [])


    def test_daily_logs(self):
        exQuery = query.Query()

        self.loggingManager.addLog("info", exQuery, "")
        res = self.loggingManager.getQueriesFromFile(self.mockFile)

        self.loggingManager.addLog("error", exQuery, "errrrrrrrr")
        res = self.loggingManager.getQueriesFromFile(self.mockFile)

        daily = self.loggingManager.getDailyLogs()

        self.assertEqual(len(daily), 2)


    def test_daily_empty_logs(self):
        self.loggingManager.logs = []
        res = self.loggingManager.getDailyLogs()

        self.assertEqual(res, [])


    def test_daily_not_today(self):
        res = self.loggingManager.getDailyLogs()

        self.assertEqual(res, [
           
            ]
        )



if __name__ == '__main__':
    unittest.main(verbosity=2)
