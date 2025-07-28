from datetime import datetime
from typing import Counter
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
        

    def getMostCommonErrorLog(self):
        mostCommonError = ""
        errors = []
        errorMap = {}

        for log in self.logs:
            errorSplit = log.split('-')
            
            if errorSplit[4] == " ERROR ":
                error = errorSplit[5] + errorSplit[6].split('\n')[0]
                errors.append(error)

        for err in errors:
            errorMap[err] = errorMap.get(err, 0) + 1
        
        mostCommonError = max(errorMap, key=errorMap.get)

        return mostCommonError
        

    def getExecTimes(self):
        data = self.databaseManager.getQueriesFromDB()
        execTimesArr = [query["execTime"] for query in data]

        return execTimesArr
    

    def getExecDates(self):
        data = self.databaseManager.getQueriesFromDB()
        execDates = [query["execTime"] for query in data]

        return execDates
    

    def getNbRowsOutput(self):
        data = self.databaseManager.getQueriesFromDB()
        nbRows = [query["nb_rows"] for query in data]        

        return nbRows


    def getNbQueriesPerHour(self):
        data = self.databaseManager.getQueriesFromDB()
        timeStrings = [query["initTime"] for query in data]
        timestamps = []
        for ts in timeStrings:
            date = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S,%f")
            timestamps.append(date)
        
        hours = [ts.hour for ts in timestamps]

        hour_counts = Counter(hours)

        # might be problematic for different timezones maybe?
        all_hours = list(range(8, 18))
        counts = [hour_counts.get(h, 0) for h in all_hours]

        return (all_hours, counts)

