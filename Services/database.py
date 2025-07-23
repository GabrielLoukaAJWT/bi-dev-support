import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import pysondb 

import Models.Query as models

class DatabaseManager:
    def __init__(self):
        self.queriesLocalDB = pysondb.getDb("queries.json")
        print(f"DATABASE : {self.queriesLocalDB}")

    def addQueryToDB(self, query: models.Query):
        queryJSON = {
            "initTime" : self.json_serial(query.initTime),
            "endTime" : self.json_serial(query.endTime),
            "execTime" : self.json_serial(query.execTime),
            "columns" : query.columns,
            "rows" : query.rows,
            "code" : query.code,
        }
        
        self.queriesLocalDB.add(queryJSON)

    def getQueriesFromDB(self):
        return self.queriesLocalDB["data"]
    
    def json_serial(self, item):
        return json.dumps(
            item,
            sort_keys=True,
            indent=1,
            cls=DjangoJSONEncoder
        )