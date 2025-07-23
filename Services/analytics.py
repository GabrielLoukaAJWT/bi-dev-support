


class AnalyticsManager:
    def __init__(self):
        self.logs = []

        print(F"CREATED ANALYTICS MANAGER\n")

    def readLogs(self):
        with open("./logs/queries.log") as f:
            for line in f:
                # print(line)
                print(type(line))

        f.close()
