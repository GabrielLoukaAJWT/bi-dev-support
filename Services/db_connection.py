import oracledb 
import os
import platform
from typing import Tuple
import datetime

import constants as cta
import Services.db_connection as cnx
import Models.Query as qry


class OracleConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

        self.columnsNames = []
        self.queryOutput = []

        self.currentQuery = qry.Query(None, None, 0.0, [], [])
        

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
            print("Error connecting:  oracledb.init_oracle_client()")
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


    def runQuery(self, sqlQuery: str):
        if self.connection is None or self.cursor is None:
            print("Connection lost.\n")

        else:
            try:
                self.currentQuery.initTime = datetime.datetime(1, 1, 1, 0, 0)
                self.currentQuery.endTime = datetime.datetime(1, 1, 1, 0, 0)
                self.currentQuery.execTime = datetime.timedelta()
                self.currentQuery.columns = []
                self.currentQuery.rows = []
                
                self.columnsNames = []
                self.queryOutput = []

                self.currentQuery.initTime = datetime.datetime.today()
                for r in self.cursor.execute(sqlQuery):
                    self.queryOutput.append(r)
                    self.currentQuery.rows.append(r)
                    # print(r)
                self.currentQuery.endTime = datetime.datetime.today()
                self.currentQuery.execTime = self.currentQuery.endTime - self.currentQuery.initTime

                self.columnsNames = [row[0] for row in self.cursor.description]
                self.currentQuery.columns = [row[0] for row in self.cursor.description]
            
            except Exception as error:
                return f"{error}\n"
