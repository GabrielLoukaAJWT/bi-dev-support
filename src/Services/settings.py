import json
from tkinter import messagebox
import bcrypt
from cryptography.fernet import Fernet
import os

class SettingsManager:
    def __init__(self, file: str):
        self.file = file
        
        if os.path.exists(self.file):    
            self.checkboxVarSettings = self.getSettings()[0]
            self.logsFlagSettings = self.getSettings()[1]
            self.credentialsSettings = self.getSettings()[2]
        else:
            messagebox.showinfo("File not found", "There are missing files.")



    
    def getSettings(self) -> tuple[int, dict]:
        with open(self.file, 'r') as f:
            settings = json.load(f)
            signInFlag = settings["staySignedIn"]
            logsFlag = settings["areLogsShown"]
            credentials = settings["credentials"]

            f.close()
            return signInFlag, logsFlag, credentials
        

    def editSignInSettings(self, username: str, dsn: str, pwd: str, signInFlag: bool) -> None:
        currLogsFlagValue = self.logsFlagSettings

        with open(self.file, 'w+') as f:
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
            
            json.dump(newSettings, f)

        f.close()


    def editLogsFlagSettings(self, newFlag: bool) -> None:
        currLogsFlagValue = self.logsFlagSettings
        currSignIn = self.credentialsSettings

        with open(self.file, 'w+') as f:
            newSettings = {
                "staySignedIn": currLogsFlagValue,
                "credentials": currSignIn,
                "areLogsShown": newFlag
            }
            
            json.dump(newSettings, f)

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

    

        


