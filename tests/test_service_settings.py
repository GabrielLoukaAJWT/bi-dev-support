import getpass
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
import pandas as pd
import datetime

import constants as cta
import Models.Query as query
import src.Services.settings as set


class SettingsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFileGeneral = "./tests/test_folders/test_settings/general.json"
        cls.mockFileAccount = "./tests/test_folders/test_settings/account.json"
        cls.mockFileQueries = "./tests/test_folders/test_settings/set_queries.json"

        cls.settingsManager = set.SettingsManager(
            cls.mockFileGeneral, 
            cls.mockFileAccount, 
            cls.mockFileQueries
        )


    def test_edit_logs_flag(self):
        self.settingsManager.editLogsFlagSettings(True)
        
        res = self.settingsManager.getLogsShownFlag()

        self.assertTrue(res)
        


    def test_edit_theme(self):
        self.settingsManager.editDarkTheme("Light")

        res = self.settingsManager.getBgTheme()

        self.assertFalse(res)


    def test_edit_acount(self):
        self.settingsManager.editSignInSettings("test", "dsn test", True)

        res = self.settingsManager.getSignInFlag()
        res2 = self.settingsManager.getCredentialsSettings()

        self.assertTrue(res)
        self.assertEqual(res2, {
            "oracleUsername": "test",
            "connectionString": "dsn test"
        })

        self.settingsManager.editCredentialsOptions("anotha", "dsn 222")

        res3 = self.settingsManager.getCredentialsSettings()
        self.assertEqual(res3, {
                "oracleUsername": "anotha",
                "connectionString": "dsn 222"
            }
        )


    def test_acc_username(self):
        self.settingsManager.editUsername("gazo")

        res = self.settingsManager.getAccUsername()

        self.assertEqual(res, "gazo")


    def test_logs_mode(self):
        self.settingsManager.editLogsShownMode("All-time")

        res = self.settingsManager.getLogsShownMode()

        self.assertEqual(res, "All-time")


        


    