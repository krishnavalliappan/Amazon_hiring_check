from dotenv import load_dotenv
import os
import logging
import logging.handlers
from check_url import CheckURL
import time

load_dotenv()

# The URL you will send the POST request to
url = 'https://hvr-amazon.my.site.com/BBIndex'

sender_email = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


if __name__ == "__main__":
    checker = CheckURL(url, logger, sender_email, password)
    while True:
        try:
            checker.send_email()
        except:
            logger.exception("Exception occured")
