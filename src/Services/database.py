from typing import Any, Dict
import pysondb 
import pandas as pd

import Models.Query as models

class DatabaseManager:
    def __init__(self, file: str):
        self.file = file
        self.queriesLocalDB = pysondb.getDb(self.file)
        print(f"DATABASE : {self.queriesLocalDB}")


    def addQueryToDB(self, query: models.Query) -> None:
        queryJSON = {
            "name": query.name,
            "initTime": query.initTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "endTime": query.endTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "execTime": query.execTime.total_seconds(),
            "ranBy": query.ranBy,
            "code": query.code,
            "nb_rows" : len(query.rows)
        }

        self.queriesLocalDB.add(queryJSON)


    def getQueriesFromDB(self) -> list[Dict[str, Any]]:
        return self.queriesLocalDB.getAll()
    

    def getQueryById(self, id: int):
        return self.queriesLocalDB.getById(id)
    
    
    def clearDB(self) -> None:
        if len(self.getQueriesFromDB()) > 0:
            self.queriesLocalDB.deleteAll()


    def editQueryName(self, id: int, newName: str) -> None:
        self.queriesLocalDB.updateById(id, {"name": newName})

    
    def deleteQueryByID(self, id: int) -> None:
        return self.queriesLocalDB.deleteById(id)


    def createDataframe(self, query: models.Query) -> pd.DataFrame:
        if query:
            df = pd.DataFrame(query.rows, columns=query.columns)
        else:
            return pd.DataFrame([], [])
        
        return df
    

    
    
