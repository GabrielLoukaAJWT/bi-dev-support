import oracledb 
import os, getpass
import platform
import datetime

import constants as cta
import Models.Query as qry
import src.Services.settings as settings


class OracleConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

        self.queryOutput = []

        self.currentQuery = qry.Query()

        self.settingsManager = settings.SettingsManager()


    def getOracleInstantClient(self) -> None:
        print("ARCH:", platform.architecture())
        print("FILES AT lib_dir:")
        for name in os.listdir(cta.LIB_DIR_AJWT):
            print(name)


    def validateOracleInstantClientFiles(self) -> bool:
        isOracleClientValid = False

        try:
            oracledb.init_oracle_client(lib_dir=cta.LIB_DIR_AJWT)
            isOracleClientValid = True
            print(f"{cta.VALID_ORACLE_INSTANT_CLIENT}\n")
            
            return isOracleClientValid
        except Exception as error:
            print(f"{cta.INVALID_ORACLE_INSTANT_CLIENT}\n")
            print(error)



    def connectToOracle(self, username: str, connectionString: str, pwd : str) -> bool:
        isOICValid = self.validateOracleInstantClientFiles()

        if isOICValid:
            # if self.settingsManager.validatePasswordHash(pwd):
                try:    
                    self.connection = oracledb.connect(
                        user=username,
                        password=pwd,
                        dsn=connectionString
                    )
                    self.cursor = self.connection.cursor()

                    return True
                
                except Exception as error:
                    self.connection = None
                    print(error)
                    return False


    def runQuery(self, sqlQuery: str, queryName: str) -> str:
        if self.connection is None or self.cursor is None:
            print(f"{cta.LOST_CONNECTION}\n")

        else:
            try:
                self.currentQuery.initTime = datetime.datetime(1, 1, 1, 0, 0)
                self.currentQuery.endTime = datetime.datetime(1, 1, 1, 0, 0)
                self.currentQuery.execTime = datetime.timedelta()
                self.currentQuery.ranBy = ""
                self.currentQuery.columns = []
                self.currentQuery.rows = []
                self.currentQuery.code = ""
                self.currentQuery.name = ""
                
                self.currentQuery.initTime = datetime.datetime.today()

                for r in self.cursor.execute(sqlQuery):
                    self.queryOutput.append(r)
                    self.currentQuery.rows.append(r)

                self.currentQuery.endTime = datetime.datetime.today()
                self.currentQuery.execTime = self.currentQuery.endTime - self.currentQuery.initTime
                self.currentQuery.ranBy = getpass.getuser()
                self.currentQuery.code = sqlQuery
                self.currentQuery.name = queryName
                self.currentQuery.columns = [row[0] for row in self.cursor.description]  
            
            except Exception as error:
                return f"{error}\n"
