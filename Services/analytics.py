


class AnalyticsManager:
    def __init__(self, loggingManager):
        self.loggingManager = loggingManager
        self.logs = self.loggingManager.logs

        print(F"CREATED ANALYTICS MANAGER\n")

    def readLogs(self):
        for log in self.logs:
            print(log) 
        print(f"count of queries ran = {len(self.logs)}")

    def computeTotalQueries(self):
        return str(len(self.logs))


