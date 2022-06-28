import sys
import logging


def get_logger(name: str, level: str = 'WARNING', file_output: str='./logs/logs.log') -> logging.Logger:
    log_level = logging._nameToLevel.get(level, 'WARNING')

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(file_output, 'w', 'utf-8')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
