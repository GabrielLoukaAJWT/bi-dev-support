import unittest
from unittest import mock
from unittest.mock import patch

import src.GUI.main_window as main_win
import src.Services.settings as settings
import src.Services.style as style_cust 
import constants as cta

class MainWindowTest(unittest.TestCase):                     

	@classmethod		  	             
	def setUpClass(cls):
		cls.mockFileGeneral = "./tests/test_folders/test_settings/general.json"
		cls.mockFileAccount = "./tests/test_folders/test_settings/account.json"
		cls.mockFileQueries = "./tests/test_folders/test_settings/set_queries.json"

		cls.settingsManager = settings.SettingsManager(
				cls.mockFileGeneral, 
				cls.mockFileAccount, 
				cls.mockFileQueries						
		)
		
		cls.mainwin = mock.MagicMock()	

		cls.mainwin.root = mock.MagicMock()
		cls.mainwin.connectBtn = mock.MagicMock()
		cls.mainwin.usernameEntry = mock.MagicMock()
		cls.mainwin.connectionStringEntry = mock.MagicMock()
		cls.mainwin.pswEntry = mock.MagicMock()
		cls.mainwin.oracleConnector = mock.MagicMock()
		cls.mainwin.connectionStatusLabel = mock.MagicMock()

		cls.mainwin.handleConnection = mock.MagicMock()
		cls.mainwin.showStatus = mock.MagicMock()
		cls.mainwin.clearRoot = mock.MagicMock()
		cls.mainwin.accessQueryView = mock.MagicMock()
		cls.mainwin.handleSaveSettingsCheckbox = mock.MagicMock()
		cls.mainwin.loadSavedCredentialsToUI = mock.MagicMock()
		cls.mainwin.show_about_dialog = mock.MagicMock()


	# @patch("src.Services.main_window.MainWindow.handleConnection")
	# def test_handleConnection(self, mock_handleConn):


	# def test_connection_good(self):
	# 	self.mainwin.usernameEntry.get.return_value = "user"
	# 	self.mainwin.connectionStringEntry.get.return_value = "db://host"
	# 	self.mainwin.pswEntry.get.return_value = "pw"
	# 	self.mainwin.oracleConnector.connectToOracle.return_value = True
	
	# 	self.real_handleConnection = main_win.MainWindow.handleConnection(self.mainwin)

	# 	self.mainwin.connectBtn.config.assert_any_call(state="disabled")
	# 	self.mainwin.handleSaveSettingsCheckbox.assert_called_once()
	# 	self.mainwin.accessQueryView.assert_called_once()
	# 	self.mainwin.root.after.assert_called()
	# 	self.assertTrue(self.mainwin.isSuccessful)
	
	
	# def test_connection_fail(self):
	# 	self.mainwin.usernameEntry.get.return_value = "user"
	# 	self.mainwin.connectionStringEntry.get.return_value = "db://host"
	# 	self.mainwin.pswEntry.get.return_value = "pw"
	# 	self.mainwin.oracleConnector.connectToOracle.return_value = False
	
	# 	self.real_handleConnection = main_win.MainWindow.handleConnection(self.mainwin)

	# 	self.mainwin.connectBtn.config.assert_any_call(state="normal")
	# 	self.assertFalse(self.mainwin.isSuccessful)


	# def test_show_status(self):
	# 	self.mainwin.usernameEntry.get.return_value = "user"
	# 	self.mainwin.connectionStringEntry.get.return_value = "db://host"
	# 	self.mainwin.pswEntry.get.return_value = "pw"
	# 	self.mainwin.oracleConnector.connectToOracle.return_value = True
	
	# 	self.mainwin.handleConnection()

	# 	# self.mainwin.connectionStatusLabel.configure.assert_any_call(text=cta.DB_CONNECTION_SUCCESS, 
	# 	# 													style="MainConectionLabelSuccess.TLabel")