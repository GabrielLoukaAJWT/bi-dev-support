import json

class SettingsManager:
    def __init__(self):
        self.checkboxVarSettings = self.getSettings()[0]
        self.credentialsSettings = self.getSettings()[1]

    
    def getSettings(self):
        with open('./settings/settings.json', 'r') as f:
            settings = json.load(f)
            cbvar = settings["checkbox var"]
            credentials = settings["credentials"]

            f.close()
            return cbvar, credentials
        

    def editSettings(self, username, dsn, pwd, cbvar):
        with open('./settings/settings.json', 'w+') as f:
            newSettings = {
                "checkbox var": cbvar,
                "credentials": {
                            "username" : username,
                            "connectionString" : dsn,
                            "pwd" : pwd
                        }
            }
            
            json.dump(newSettings, f)

        f.close()
        


