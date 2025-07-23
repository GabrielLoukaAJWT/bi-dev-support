import logging 

import Models.Query as models

class QueryLoggerManager:
    def __init__(self):

        logging.basicConfig(
            format="{asctime} - {levelname} - {message}",
            style="{",
            filename="./logs/queries.log",
            level=logging.INFO
        )

        self.logger = logging.getLogger(__name__)


    def addLog(self, type: str, query: models.Query, msg: str):
        match type:
            case "info":
                self.logger.info(
                    f"Exec time : {query.execTime}\n"
                )
            case "error":
                self.logger.error(
                    f"Detected error : {msg}"
                )


    def clearLogsFile(self):
        log_file = open('./logs/queries.log', "r+")
        log_file.truncate(0)


        