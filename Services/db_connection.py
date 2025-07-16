import sys
import constants as cta

import oracledb 
import os
import platform
from typing import Tuple

import Services.db_connection as cnx


class OracleConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None
        

    def getOracleInstantClient(self):
        print("ARCH:", platform.architecture())
        print("FILES AT lib_dir:")
        for name in os.listdir(cta.LIB_DIR):
            print(name)


    def connectToOracle(self, psw : str) -> Tuple[bool, str] :
        try:
            oracledb.init_oracle_client(lib_dir=cta.LIB_DIR)
            print("Initialized Oracle Instant Client.\n")
        except Exception as error:
            print("Error connecting: cx_Oracle.init_oracle_client()")
            print(error)

        try:    
            self.connection = oracledb.connect(
                user=cta.USERNAME,
                password=psw,
                dsn=cta.CONNECTION_STRING
            )
            self.cursor = self.connection.cursor()
            print("Valid credentials - connection successful.\n")

            return True, cta.DB_CONNECTION_SUCCESS
        
        except Exception as error:
            print("Invalid credentials - connexion denied.\n")
            self.connection = None

            return False, cta.DB_CONNECTION_ERROR


    def run_query(self, sqlQuery: str):
        if self.connection is None or self.cursor is None:
            print("Connection lost.\n")
        else:
            for r in self.cursor.execute(sqlQuery):
                print(r)
