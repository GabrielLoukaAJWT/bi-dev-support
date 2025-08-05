import unittest

import src.Services.db_connection as oracle_cnx
import constants as cta
import Models.Exceptions as exc

class DBConnectionTest(unittest.TestCase):

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

    
    def test_oracle_connection(self):
        res = self.oracleConnector.connectToOracle("ok", "ok", "ok")

        self.assertIsNone(self.oracleConnector.connection)
        self.assertIsNone(self.oracleConnector.cursor)
            
    



if __name__ == '__main__':
    unittest.main(verbosity=2)
