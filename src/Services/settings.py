import json
from tkinter import messagebox
import bcrypt
from cryptography.fernet import Fernet
import os

class SettingsManager:
    def __init__(self, genSettingsFiles: str, credentialsSettingsFile: str):
        self.generalSettingsFile = genSettingsFiles
        self.credentialsSettingsFile = credentialsSettingsFile
        
        self.logsFlagSettings = self.getLogsShownFlag()
        self.isDarkMode = self.getBgTheme()
        
        self.checkboxVarSettings = self.getSignInFlag()
        self.credentialsSettings = self.getCredentialsSettings()


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
        with open(self.credentialsSettingsFile, 'r') as f:
            settings = json.load(f)
            signInFlag = settings["staySignedIn"]
            
            f.close()
            return signInFlag
        

    def getCredentialsSettings(self) -> dict:
        with open(self.credentialsSettingsFile, 'r') as f:
            settings = json.load(f)

            credentials = settings["credentials"]

            f.close()
            return credentials
        
        

    def editSignInSettings(self, username: str, dsn: str, pwd: str, signInFlag: bool) -> None:
        with open(self.credentialsSettingsFile, 'w+') as f:
            newSettings = {
                "staySignedIn": signInFlag,
                "credentials": {
                            "username" : username,
                            "connectionString" : dsn
                            # "pwd" : self.hashPwd(pwd)
                            # "pwdEncr" : self.encryptPlainPwd(pwd)
                        },
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

        



    # def hashPwd(self, pwd: str) -> str:
    #     salt = bcrypt.gensalt()
    #     hashedPwd = bcrypt.hashpw(pwd, salt)

    #     return hashedPwd
    

    # def validatePasswordHash(self, rawPwd: str) -> bool:
    #     storedHash = self.credentialsSettings["pwd"]
    #     return bcrypt.checkpw(rawPwd, storedHash)
    

    # def encryptPlainPwd(self, plainPwd: str) -> str:
    #     key = Fernet.generate_key()
    #     cipherSuite = Fernet(key)
    #     encodedPwd = json.dumps(cipherSuite.encrypt(plainPwd.encode(encoding="utf-8")))

    #     return encodedPwd

    

        


