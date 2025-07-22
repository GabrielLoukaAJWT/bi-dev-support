import logging 

import Models.Query as models

class QueryLoggerManager:
    def __init__(self):

        logging.basicConfig(
            format="{asctime} - {levelname} - {message}",
            style="{",
            # datefmt='%Y-%m-%d %H:%M:%S,%f',
            filename="./logs/queries.log",
            level=logging.INFO
        )

        self.logger = logging.getLogger(__name__)


    def logSuccessfulQuery(self, type: str, query: models.Query):
        match type:
            case "info":
                self.logger.info(
                    f"Exec time : {query.execTime}"
                )


        