import Services.database as db

class AnalyticsManager:
    def __init__(self, loggingManager):
        self.loggingManager = loggingManager
        self.logs = self.loggingManager.logs

        self.databaseManager = db.DatabaseManager()

        print(F"CREATED ANALYTICS MANAGER\n")


    def readLogs(self):
        for log in self.logs:
            print(log) 
        print(f"count of queries ran = {len(self.logs)}")


    def computeTotalQueries(self):
        return len(self.databaseManager.getQueriesFromDB())
    

    def getRowsForTree(self):
        data = self.databaseManager.getQueriesFromDB()
        rows = []

        for query in data:
            rowToInsert = (
                query["id"],
                query["name"],
                query["execTime"],
                query["initTime"],
                query["nb_rows"]
            )

            rows.append(rowToInsert)

        return rows
    

    def getQueryWithLongestExecTime(self):
        data = self.databaseManager.getQueriesFromDB()
        idAndExecTimeMap = {}
        slowestQueryID = 0

        try:
            if data:
                for query in data:
                    idAndExecTimeMap[query["id"]] = query["execTime"]

                slowestQueryID = max(idAndExecTimeMap, key=idAndExecTimeMap.get)

            return self.databaseManager.queriesLocalDB.find(slowestQueryID)
        
        except Exception as error:
            print(f"{error}")


    def computeAvgExecTime(self):
        data = self.databaseManager.getQueriesFromDB()
        totalExecTime = 0

        if data and len(data) != 0:
            for query in data:
                totalExecTime += query["execTime"]

            return "{:.6f}".format(totalExecTime / self.computeTotalQueries())
        else:
            return 0
        


