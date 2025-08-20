import json
from tkinter import messagebox
import bcrypt
from cryptography.fernet import Fernet
import os

class SettingsManager:
    def __init__(self, genSettingsFilesPath: str, accountSettingsFilePath: str, queriesSettingsFilePath: str):
        self.generalSettingsFilePath = genSettingsFilesPath
        self.accountSettingsFilePath = accountSettingsFilePath
        self.queriesSettingsFilePath = queriesSettingsFilePath
        

    ###### general.json ######

    def getLogsShownFlag(self) -> bool:
        with open(self.generalSettingsFilePath, 'r') as f:
            settings = json.load(f)

            areLogsShownFlag = settings["areLogsShown"]

            f.close()
            return areLogsShownFlag
        

    def getBgTheme(self) -> bool:
        with open(self.generalSettingsFilePath, 'r') as f:
            settings = json.load(f)

            isDark = settings["isDarkMode"]

            f.close()
            return isDark
        

    

    def editLogsFlagSettings(self, newFlag: bool) -> None:
        currIsDarkTheme = self.getBgTheme()

        with open(self.generalSettingsFilePath, 'w+') as f:
            newSettings = {
                "areLogsShown": newFlag,
                "isDarkMode": currIsDarkTheme
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()


    def editDarkTheme(self, newTheme: str):
        currAreLogsShown = self.getLogsShownFlag()
        
        with open(self.generalSettingsFilePath, 'w+') as f:
            newSettings = {
                "areLogsShown": currAreLogsShown,
                "isDarkMode": (True if newTheme == 'Dark' else False)
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()


    ##### account.json #####
    
    def getSignInFlag(self) -> bool:
        with open(self.accountSettingsFilePath, 'r') as f:
            settings = json.load(f)
            signInFlag = settings["staySignedIn"]
            
            f.close()
            return signInFlag
        

    def getCredentialsSettings(self) -> dict:
        with open(self.accountSettingsFilePath, 'r') as f:
            settings = json.load(f)

            credentials = settings["credentials"]

            f.close()
            return credentials
        

    def getAccUsername(self) -> str:
        with open(self.accountSettingsFilePath, 'r') as f:
            settings = json.load(f)

            username = settings["accUsername"]

            f.close()
            return username
        
        

    def editSignInSettings(self, username: str, dsn: str, signInFlag: bool) -> None:
        currUsername = self.getAccUsername()

        with open(self.accountSettingsFilePath, 'w+') as f:
            newSettings = {
                "staySignedIn": signInFlag,
                "credentials": {
                            "oracleUsername" : username,
                            "connectionString" : dsn
                        },
                "accUsername": currUsername
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()

    
    
    def editCredentialsOptions(self, newOracleUser: str, newOracleDSN: str) -> None:
        currSignInFlag = self.getSignInFlag()
        currUsername = self.getAccUsername()

        with open(self.accountSettingsFilePath, 'w+') as f:
            newSettings = {
                "staySignedIn": currSignInFlag,
                "credentials": {
                            "oracleUsername" : newOracleUser,
                            "connectionString" : newOracleDSN
                        },
                "accUsername": currUsername
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()
    
    
    
    def editUsername(self, newUsername: str) -> None:
        currSignInFlag = self.getSignInFlag()
        currCredentials = self.getCredentialsSettings()

        with open(self.accountSettingsFilePath, 'w+') as f:
            newSettings = {
                "staySignedIn": currSignInFlag,
                "credentials": currCredentials,
                "accUsername": newUsername
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()


    ##### set_queries.json #####

    def getLogsShownMode(self) -> str:
        with open(self.queriesSettingsFilePath, 'r') as f:
            settings = json.load(f)

            logsShownMode = settings["showLogsMode"]

            f.close()
            
            return logsShownMode
        

    def editLogsShownMode(self, newMode: str) -> bool:
        editSuccessful = False

        with open(self.queriesSettingsFilePath, 'w+') as f:
            newSettings = {
                "showLogsMode": newMode
            }
            
            json.dump(newSettings, f, indent=4)

            editSuccessful = True

        f.close()

        return editSuccessful

        


    
        

        


