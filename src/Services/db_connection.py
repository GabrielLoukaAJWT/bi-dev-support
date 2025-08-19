import oracledb 
import getpass
import datetime

import constants as cta
import Models.Query as qry
import src.Services.settings as settings


class OracleConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.isOracleClientValid = False

        self.queryOutput = []

        self.currentQuery = qry.Query()

        self.settingsManager = settings.SettingsManager(cta.DIR_SETTINGS_GENERAL, cta.DIR_SETTINGS_ACCOUNT)


    def validateOracleInstantClientFiles(self, file: str) -> bool:
        try:
            oracledb.init_oracle_client(lib_dir=file)
            self.isOracleClientValid = True
            print(f"{cta.VALID_ORACLE_INSTANT_CLIENT}")
            
            return self.isOracleClientValid
        
        except Exception as error:
            print(error)



    def connectToOracle(self, username: str, connectionString: str, pwd : str) -> bool:
        self.validateOracleInstantClientFiles(cta.LIB_DIR_AJWT)

        if self.isOracleClientValid:
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
                self.currentQuery.ranBy = self.settingsManager.getAccUsername()
                self.currentQuery.code = sqlQuery
                self.currentQuery.name = queryName
                self.currentQuery.columns = [row[0] for row in self.cursor.description]  
            
            except Exception as error:
                return f"{error}\n"
