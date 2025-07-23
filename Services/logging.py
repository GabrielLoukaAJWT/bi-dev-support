import logging

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

        self.logs = []
        listHandler = ListHandler(self.logs)
        listHandler.setFormatter(formatter)

        self.logger.addHandler(listHandler)



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
        log_file.close()




class ListHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        self.log_list.append(self.format(record))


        