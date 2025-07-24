import pysondb 

import Models.Query as models

class DatabaseManager:
    def __init__(self):
        self.queriesLocalDB = pysondb.getDb("./local_DB/queries.json")
        print(f"DATABASE : {self.queriesLocalDB}")


    def addQueryToDB(self, query: models.Query):

        queryJSON = {
            "name": query.name,
            "initTime": query.initTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "endTime": query.endTime.strftime("%Y-%m-%d %H:%M:%S,%f"),
            "execTime": f"{query.execTime.total_seconds():.6f} sec",
            # "columns": [str(col) for col in query.columns],
            # "rows": [[str(cell) for cell in row] for row in query.rows],
            "code": query.code,
            "nb_rows" : str(len(query.rows))
        }

        self.queriesLocalDB.add(queryJSON)


    def getQueriesFromDB(self):
        return self.queriesLocalDB.getAll()
    
    
    def clearDB(self):
        self.queriesLocalDB.deleteAll()
