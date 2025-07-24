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
        return str(len(self.logs))
    

    def getRowsForTree(self):
        data = self.databaseManager.getQueriesFromDB()
        rows = []

        for query in data:
            rowToInsert = (
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

        for query in data:
            idAndExecTimeMap[query["id"]] = query["execTime"]

        slowestQueryID = max(idAndExecTimeMap, key=idAndExecTimeMap.get)

        return self.databaseManager.find(slowestQueryID)


