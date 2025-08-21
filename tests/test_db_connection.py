import unittest
from unittest import mock
from unittest.mock import patch, MagicMock

import src.Services.db_connection as oracle_cnx
import constants as cta

class DBConnectionTest(unittest.TestCase):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor 

    @classmethod
    def setUpClass(cls):
        cls.oracleConnector = oracle_cnx.OracleConnector()


    def test_valid_oracle_instant_client_files(self):
        res = self.oracleConnector.validateOracleInstantClientFiles(cta.LIB_DIR_AJWT)

        self.assertTrue(res)


    def test_exception_oic_files(self):
        with self.assertRaises(Exception) as cm:
            res = self.oracleConnector.validateOracleInstantClientFiles("its over")

            self.assertFalse(res)
            self.assertIn(cta.INVALID_ORACLE_INSTANT_CLIENT, str(cm.exception))


    @patch("oracledb.connect", return_value=mock_connection)
    def test_oracle_connection_success(self, mock_oracledb_connect):
        res = self.oracleConnector.connectToOracle("user", "hostname:port/servicename", "password")

        mock_oracledb_connect.assert_called_once_with(
                user="user", password="password", dsn="hostname:port/servicename"
        )
        self.assertTrue(self.oracleConnector.isOracleClientValid)

    
    @patch("oracledb.connect", return_value=mock_connection)
    def test_oracle_connection_failure(self, mock_oracledb_connect):

        with self.assertRaises(Exception) as cm:
            res = self.oracleConnector.connectToOracle("shit1", "hostname:port/servicename", "password")

            self.assertFalse(res)
            self.assertIsNone(self.oracleConnector.connection)


    def test_run_query_success(self):
        res = self.oracleConnector.runQuery("select * from dual", "queryname")

        self.assertIsNotNone(self.oracleConnector.currentQuery)

        
            
            
    



if __name__ == '__main__':
    unittest.main(verbosity=2)
