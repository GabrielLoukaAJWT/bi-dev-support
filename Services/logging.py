import logging 

class QueryLoggerManager:
    def __init__(self):

        self.logger = logging.getLogger(__name__)

        logging.basicConfig(
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            filename="../logs/queries.log"
        )


    def logSuccessfulQuery(self, type: str, message: str):
        match type:
            case "info":
                self.logger.info(message)
            case "error":
                self.logger.error(message)
            case "warning":
                self.logger.warning(message)
            case "debug":
                self.logger.debug(message)

        