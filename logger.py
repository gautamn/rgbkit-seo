import logging
from dotenv import load_dotenv
import os

load_dotenv()

def get_logger(logger_name, log_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.propagate = False  # Prevent log propagation to avoid double logging

    log_format = "%(asctime)s [%(process)d] %(levelname)s %(filename)s : %(funcName)s %(lineno)d - %(message)s"
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # if os.getenv("generate_debug_logs") == "true":
    #     file_name = os.getenv("backend_log_file")
    #     file_handler = logging.FileHandler(file_name, mode='a')
    #     file_handler.setFormatter(formatter)
    #     logger.addHandler(file_handler)

    return logger
