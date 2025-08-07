import getpass
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
import pandas as pd
import datetime

import constants as cta
import Models.Exceptions as exc
import Models.Query as query
import src.Services.settings as set


class SettingsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mockFile = "./tests/test_folders/test_settings/settings.json"

        cls.settingsManager = set.SettingsManager(cls.mockFile)
        


    def test_edit_settings(self):
        self.settingsManager.editSettings(
            "bla",
            "dsn222",
            "bleh",
            1
        )

        self.assertEqual(self.settingsManager.credentialsSettings, 
                                {
                                    "username": "bla",
                                    "connectionString": "dsn222"
                                }                         
                        )
        self.assertEqual(self.settingsManager.checkboxVarSettings, 1)

    