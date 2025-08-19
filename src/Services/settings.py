import json
from tkinter import messagebox
import bcrypt
from cryptography.fernet import Fernet
import os

class SettingsManager:
    def __init__(self, genSettingsFiles: str, accountSettingsFile: str):
        self.generalSettingsFile = genSettingsFiles
        self.accountSettingsFile = accountSettingsFile
        
        self.logsFlagSettings = self.getLogsShownFlag()
        self.isDarkMode = self.getBgTheme()
        
        self.checkboxVarSettings = self.getSignInFlag()
        self.credentialsSettings = self.getCredentialsSettings()
        self.accUsername = self.getAccUsername()


    def getLogsShownFlag(self) -> bool:
        with open(self.generalSettingsFile, 'r') as f:
            settings = json.load(f)

            areLogsShownFlag = settings["areLogsShown"]

            f.close()
            return areLogsShownFlag
        

    def getBgTheme(self) -> bool:
        with open(self.generalSettingsFile, 'r') as f:
            settings = json.load(f)

            isDark = settings["isDarkMode"]

            f.close()
            return isDark

    
    def getSignInFlag(self) -> bool:
        with open(self.accountSettingsFile, 'r') as f:
            settings = json.load(f)
            signInFlag = settings["staySignedIn"]
            
            f.close()
            return signInFlag
        

    def getCredentialsSettings(self) -> dict:
        with open(self.accountSettingsFile, 'r') as f:
            settings = json.load(f)

            credentials = settings["credentials"]

            f.close()
            return credentials
        

    def getAccUsername(self) -> str:
        with open(self.accountSettingsFile, 'r') as f:
            settings = json.load(f)

            username = settings["accUsername"]

            f.close()
            return username
        
        

    def editSignInSettings(self, username: str, dsn: str, signInFlag: bool) -> None:
        currUsername = self.getAccUsername()

        with open(self.accountSettingsFile, 'w+') as f:
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

    
    def editUsername(self, newUsername: str) -> None:
        currSignInFlag = self.getSignInFlag()
        currCredentials = self.getCredentialsSettings()

        with open(self.accountSettingsFile, 'w+') as f:
            newSettings = {
                "staySignedIn": currSignInFlag,
                "credentials": currCredentials,
                "accUsername": newUsername
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()

        


    def editLogsFlagSettings(self, newFlag: bool) -> None:
        currIsDarkTheme = self.isDarkMode

        with open(self.generalSettingsFile, 'w+') as f:
            newSettings = {
                "areLogsShown": newFlag,
                "isDarkMode": currIsDarkTheme
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()


    def editDarkTheme(self, newTheme: str):
        currAreLogsShown = self.logsFlagSettings
        
        with open(self.generalSettingsFile, 'w+') as f:
            newSettings = {
                "areLogsShown": currAreLogsShown,
                "isDarkMode": (True if newTheme == 'Dark' else False)
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()

        

        


