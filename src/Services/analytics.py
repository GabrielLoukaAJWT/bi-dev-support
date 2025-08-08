from datetime import datetime
import pytz
from typing import Counter

import src.Services.database as db
import constants as cta


class AnalyticsManager:
    def __init__(self, loggingManager, file):
        self.loggingManager = loggingManager
        self.logs = self.loggingManager.logs
        self.file = file

        self.databaseManager = db.DatabaseManager(self.file)

        print(F"CREATED ANALYTICS MANAGER\n")


    def computeTotalQueries(self) -> int:
        return len(self.databaseManager.getQueriesFromDB())
    

    def getRowsForTree(self) -> list:
        data = self.databaseManager.getQueriesFromDB()
        rows = []

        if data:
            for query in data:
                rowToInsert = (
                    query["id"],
                    query["name"],
                    query["execTime"],
                    query["ranBy"],
                    query["initTime"],
                    query["nb_rows"]
                )

                rows.append(rowToInsert)
        else:
            return []

        return rows
    

    def getQueryWithLongestExecTime(self) -> dict:
        data = self.databaseManager.getQueriesFromDB()
        idAndExecTimeMap = {}
        slowestQueryID = 0

        if data and len(data) != 0:
            for query in data:
                idAndExecTimeMap[query["id"]] = query["execTime"]

            slowestQueryID = max(idAndExecTimeMap, key=idAndExecTimeMap.get)
        
        else:
            return {}

        return self.databaseManager.getQueryById(slowestQueryID)



    def computeAvgExecTime(self) -> float:
        data = self.databaseManager.getQueriesFromDB()
        totalExecTime = 0

        if data and len(data) != 0:
            for query in data:
                totalExecTime += query["execTime"]

            return "{:.6f}".format(totalExecTime / self.computeTotalQueries())
        else:
            return 0
        

    def getMostCommonErrorLog(self) -> str:
        mostCommonError = ""
        errors = []
        errorMap = {}        

        if len(self.logs) == 0:
            return ""
        else:
            for log in self.logs:
                errorSplit = log.split('|')
                
                if errorSplit[2] == " ERROR ":
                    error = errorSplit[3].split('\n')[0]
                    errors.append(error)
                else:
                    continue

            if errors:
                for err in errors:
                    errorMap[err] = errorMap.get(err, 0) + 1    
            else:
                return ""       
            
            mostCommonError = max(errorMap, key=errorMap.get, default={})

        return mostCommonError
        

    def getExecTimes(self) -> list:
        data = self.databaseManager.getQueriesFromDB()
        
        if data and len(data) != 0:
            execTimesArr = [query["execTime"] for query in data]
        else:
            return []

        return execTimesArr
    
    

    def getNbRowsOutput(self) -> list[int]:
        data = self.databaseManager.getQueriesFromDB()

        if data and len(data) != 0:
            nbRows = [query["nb_rows"] for query in data] 
        else:
            return []       

        return nbRows


    def getNbQueriesPerHour(self) -> tuple[list[int], list[int]]:
        data = self.databaseManager.getQueriesFromDB()

        if data and len(data) != 0:
            timeStrings = [query["initTime"] for query in data]
        else:
            return ([], [])
        timestamps = []

        today = datetime.today()
        for ts in timeStrings:
            date = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S,%f")
            
            if date.date() == today.date():
                timestamps.append(date)
            else:
                continue
        
        hours = [ts.hour for ts in timestamps]

        hour_counts = Counter(hours)

        # might be problematic for different timezones maybe?
        all_hours = list(range(8, 18))
        counts = [hour_counts.get(h, 0) for h in all_hours]
        res = (all_hours, counts)

        return res

