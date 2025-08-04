from datetime import datetime
import logging
import re

import Models.Query as models
import constants as cta

class QueryLoggerManager:
    def __init__(self):
        self.logger = logging.getLogger('sql logger')
        self.logger.setLevel(logging.INFO)

        fh = logging.FileHandler(cta.LOGS_FILE)
        # ch = logging.StreamHandler()        

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        
        fh.setFormatter(formatter)
        # ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        # self.logger.addHandler(ch)

        self.logs = self.getQueriesFromFile(cta.LOGS_FILE)

        listHandler = ListHandler(self.logs)
        listHandler.setFormatter(formatter)

        self.logger.addHandler(listHandler)



    def addLog(self, type: str, query: models.Query, msg: str) -> None:
        match type:
            case "info":
                self.logger.info(
                    f"Exec time : {query.execTime}\n"
                )
            case "error":
                self.logger.error(
                    f"{msg}"
                )


    def clearLogsFile(self) -> None:
        log_file = open(cta.LOGS_FILE, "r+")
        log_file.truncate(0)
        log_file.close()


    def getQueriesFromFile(self, filepath: str) -> list[str]:
        log_entries = []
        current_entry = ""

        # this regex matches the date format, so it has to adapt to changes
        new_entry_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if new_entry_pattern.match(line):
                        if current_entry:
                            log_entries.append(current_entry.strip())
                        current_entry = line
                    else:
                        current_entry += line
                if current_entry:
                    log_entries.append(current_entry.strip())
                    print(f"CURRENT ENTRY READ {current_entry.strip()}")
        except FileNotFoundError:
            print(f"Log file not found: {filepath}")
        except Exception as e:
            print(f"Error reading log file: {e}")

        return log_entries
    

    def getDailyLogs(self) -> list[str]:
        logs = self.getQueriesFromFile(cta.LOGS_FILE)

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


        