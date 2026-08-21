import logging
from Program.LogicOfProgram.Development import generateLogs 

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if generateLogs == 1:
        logger.setLevel(logging.DEBUG)
    else:
        # skutecznie wyłącza logger
        logger.setLevel(logging.CRITICAL + 1)  

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger