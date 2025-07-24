import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import pysondb 
import pickle
from dataclasses import dataclass, asdict

import Models.Query as models

class DatabaseManager:
    def __init__(self):
        self.queriesLocalDB = pysondb.getDb("./local_DB/queries.json")
        print(f"DATABASE : {self.queriesLocalDB}")


    def addQueryToDB(self, query: models.Query):

        queryJSON = {
            "initTime": query.initTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "endTime": query.endTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "execTime": f"{query.execTime.total_seconds():.3f} sec",
            "columns": [str(col) for col in query.columns],
            "rows": [[str(cell) for cell in row] for row in query.rows],
            "code": query.code
        }

        self.queriesLocalDB.add(queryJSON)


    def getQueriesFromDB(self):
        return self.queriesLocalDB.getAll()
    
    
    def json_serial(self, item):
        serialJSON =  json.dumps(
            item, indent=4, sort_keys=True, default=str
        )

        print(f"SERIAL JSON : {serialJSON}")

        return serialJSON