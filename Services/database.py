from typing import Any, Dict
import pysondb 
import pandas as pd

import Models.Query as models

class DatabaseManager:
    def __init__(self):
        self.queriesLocalDB = pysondb.getDb("./local_DB/queries.json")
        print(f"DATABASE : {self.queriesLocalDB}")


    def addQueryToDB(self, query: models.Query) -> None:
        queryJSON = {
            "name": query.name,
            "initTime": query.initTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "endTime": query.endTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "execTime": query.execTime.total_seconds(),
            "ranBy": query.ranBy,
            # "columns": [str(col) for col in query.columns],
            # "rows": [[str(cell) for cell in row] for row in query.rows],
            "code": query.code,
            "nb_rows" : len(query.rows)
        }

        self.queriesLocalDB.add(queryJSON)


    def getQueriesFromDB(self) -> list[Dict[str, Any]]:
        return self.queriesLocalDB.getAll()
    
    
    def clearDB(self) -> None:
        if len(self.getQueriesFromDB()) > 0:
            self.queriesLocalDB.deleteAll()


    def createDataframe(self, query: models.Query) -> pd.DataFrame:
        if query:
            df = pd.DataFrame(query.rows, columns=query.columns)
        else:
            return pd.DataFrame([], [])
        return df
    
    
