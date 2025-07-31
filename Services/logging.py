import logging
import re

import Models.Query as models

class QueryLoggerManager:
    def __init__(self):
        self.logger = logging.getLogger('sql logger')
        self.logger.setLevel(logging.INFO)

        fh = logging.FileHandler('./logs/queries.log')
        ch = logging.StreamHandler()        

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        self.logs = self.getQueriesFromFile("./logs/queries.log")

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
        log_file = open('./logs/queries.log', "r+")
        log_file.truncate(0)
        log_file.close()


    def getQueriesFromFile(self, filepath: str) -> list[str]:
        log_entries = []
        current_entry = ""

        new_entry_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}")

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
        except FileNotFoundError:
            print(f"Log file not found: {filepath}")
        except Exception as e:
            print(f"Error reading log file: {e}")

        return log_entries
        


class ListHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        self.log_list.append(self.format(record))


        