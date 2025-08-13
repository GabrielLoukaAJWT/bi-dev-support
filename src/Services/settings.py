import json
from tkinter import messagebox
import bcrypt
from cryptography.fernet import Fernet
import os

class SettingsManager:
    def __init__(self, credentialsSettingsFile: str):
        self.credentialsSettingsFile = credentialsSettingsFile
        
        if os.path.exists(self.credentialsSettingsFile):    
            self.checkboxVarSettings = self.getSignInFlag()
            self.logsFlagSettings = self.getLogsShownFlag()
            self.credentialsSettings = self.getCredentialsSettings()
        else:
            messagebox.showinfo("File not found", "There are missing files.")


    
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
        

    def getLogsShownFlag(self) -> bool:
        with open(self.credentialsSettingsFile, 'r') as f:
            settings = json.load(f)

            areLogsShownFlag = settings["areLogsShown"]

            f.close()
            return areLogsShownFlag
        

    def editSignInSettings(self, username: str, dsn: str, pwd: str, signInFlag: bool) -> None:
        currLogsFlagValue = self.logsFlagSettings

        with open(self.credentialsSettingsFile, 'w+') as f:
            newSettings = {
                "staySignedIn": signInFlag,
                "credentials": {
                            "username" : username,
                            "connectionString" : dsn
                            # "pwd" : self.hashPwd(pwd)
                            # "pwdEncr" : self.encryptPlainPwd(pwd)
                        },
                "areLogsShown": currLogsFlagValue
            }
            
            json.dump(newSettings, f, indent=4)

        f.close()


    def editLogsFlagSettings(self, newFlag: bool) -> None:
        currStatSignedInValue = self.checkboxVarSettings
        currCredentials = self.credentialsSettings

        with open(self.credentialsSettingsFile, 'w+') as f:
            newSettings = {
                "staySignedIn": currStatSignedInValue,
                "credentials": currCredentials,
                "areLogsShown": newFlag
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

    

        


