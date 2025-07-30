import json
import bcrypt
from cryptography.fernet import Fernet

class SettingsManager:
    def __init__(self):
        self.checkboxVarSettings = self.getSettings()[0]
        self.credentialsSettings = self.getSettings()[1]

    
    def getSettings(self) -> tuple[int, dict]:
        with open('./settings/settings.json', 'r') as f:
            settings = json.load(f)
            cbvar = settings["checkbox var"]
            credentials = settings["credentials"]

            f.close()
            return cbvar, credentials
        

    def editSettings(self, username: str, dsn: str, pwd: str, cbvar: int) -> None:
        with open('./settings/settings.json', 'w+') as f:
            newSettings = {
                "checkbox var": cbvar,
                "credentials": {
                            "username" : username,
                            "connectionString" : dsn
                            # "pwd" : self.hashPwd(pwd)
                            # "pwdEncr" : self.encryptPlainPwd(pwd)
                        }
            }
            
            json.dump(newSettings, f)

        f.close()


    def hashPwd(self, pwd: str) -> str:
        salt = bcrypt.gensalt()
        hashedPwd = bcrypt.hashpw(pwd, salt)

        return hashedPwd
    

    def validatePasswordHash(self, rawPwd: str) -> bool:
        storedHash = self.credentialsSettings["pwd"]
        return bcrypt.checkpw(rawPwd, storedHash)
    

    def encryptPlainPwd(self, plainPwd: str) -> str:
        key = Fernet.generate_key()
        cipherSuite = Fernet(key)
        encodedPwd = json.dumps(cipherSuite.encrypt(plainPwd.encode(encoding="utf-8")))

        return encodedPwd

    

        


