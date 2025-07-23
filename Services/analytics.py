


class AnalyticsManager:
    def __init__(self, loggingManager):
        self.logs = loggingManager.logs

        print(F"CREATED ANALYTICS MANAGER\n")

    def readLogs(self):
        with open("./logs/queries.log") as f:
            for line in f:
                print(line)
                # print(type(line))

        f.close()
        self.displayCurrentLogsFromHandler()

    def displayCurrentLogsFromHandler(self):
        print(self.logs)
        print(f"count of queries ran = {len(self.logs)}")
