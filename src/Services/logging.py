from datetime import datetime
import logging
import re

import Models.Query as models
import constants as cta

class QueryLoggerManager:
    def __init__(self, logFile: str, loggerName: str):
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.INFO)
        self.logFile = logFile

        self.fh = self.setFileHandler(self.logFile)
        # ch = logging.StreamHandler()        

        self.formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        
        self.fh.setFormatter(self.formatter)
        # ch.setFormatter(formatter)

        self.logger.addHandler(self.fh)
        # self.logger.addHandler(ch)

        self.logs = self.getLogsFromFile(self.logFile)

        self.listHandler = ListHandler(self.logs)
        self.listHandler.setFormatter(self.formatter)

        self.logger.addHandler(self.listHandler)


    def setFileHandler(self, logFile: str):
        return logging.FileHandler(logFile)


    def addLog(self, type: str, query: models.Query, msg: str) -> None:
        match type:
            case "info":
                self.logger.info(
                    f"Exec time : {query.execTime}\n" # SEE THIS
                )
            case "error":
                self.logger.error(
                    f"{msg}"
                )
            case _:
                return


    def clearLogsFile(self) -> None:
        log_file = open(self.logFile, "r+")
        log_file.truncate(0)
        log_file.close()


    def getLogsFromFile(self, filepath: str) -> list[str]:
        log_entries = []
        current_entry = ""

        # this regex matches the date format, so it has to adapt to changes
        new_entry_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    # if a line from the logFile starts with a date (regex), then it's a singular log as wanted
                    if new_entry_pattern.match(line):
                        if current_entry:
                            log_entries.append(current_entry.strip())
                        current_entry = line
                    else:
                        current_entry += line
                if current_entry:
                    log_entries.append(current_entry.strip())

        except FileNotFoundError:
            print(f"Log logFile not found: {filepath}")

        return log_entries
    

    def getDailyLogs(self) -> list[str]:
        logs = self.getLogsFromFile(self.logFile)

        if not logs:
            return []

        daily = []
        today = datetime.today().date()

        for log in logs:
            timestampStr = log[:19] 

            parsed = datetime.strptime(timestampStr, "%Y-%m-%d %H:%M:%S")

            if parsed.date() == today:
                daily.append(log)
            else:
                continue

        return daily

        


class ListHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        self.log_list.append(self.format(record))


        