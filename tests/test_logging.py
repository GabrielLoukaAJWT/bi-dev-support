import unittest
from unittest import mock
from unittest.mock import patch, MagicMock

import constants as cta
import Models.Query as query
import src.Services.logging as log

class LoggingTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFile = "./tests/test_folders/test_logs/queries_for_logs.log"
        cls.loggingManager = log.QueryLoggerManager(cls.mockFile, "test logging")

    
    def test_init(self):
        self.assertIsNotNone(self.loggingManager.logger)

    
    def test_new_log_added(self):
        self.loggingManager.clearLogsFile()

        exQuery = query.Query()
        self.loggingManager.addLog("info", exQuery, "")

        self.loggingManager.addLog("error", exQuery, "errrrrrrrr")
        res = self.loggingManager.getLogsFromFile(self.mockFile)

        self.assertEqual(len(res), 2)

        self.loggingManager.addLog("no type", exQuery, "errrrrrrrr")
        res = self.loggingManager.getLogsFromFile(self.mockFile)
        
        self.assertEqual(len(res), 2)
        
        self.loggingManager.clearLogsFile()

    
    def test_bad_file(self):
        self.mockFile = "badfile"
        res = self.loggingManager.getLogsFromFile(self.mockFile)

        self.assertEqual(res, [])


    def test_daily_logs(self):
        self.loggingManager.clearLogsFile()
        exQuery = query.Query()

        self.loggingManager.addLog("info", exQuery, "")

        self.loggingManager.addLog("error", exQuery, "errrrrrrrr")

        daily = self.loggingManager.getDailyLogs()

        self.assertEqual(len(daily), 2)

        self.loggingManager.clearLogsFile()


    def test_daily_empty_logs(self):
        self.loggingManager.clearLogsFile()
        res = self.loggingManager.getDailyLogs()

        self.assertEqual(res, [])


    def test_daily_today(self):
        self.loggingManager.clearLogsFile()
        res = self.loggingManager.getDailyLogs()

        self.assertEqual(len(res), 0)



if __name__ == '__main__':
    unittest.main(verbosity=2)
