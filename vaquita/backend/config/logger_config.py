"""Set up a global logger method."""

import logging


def setup_custom_logger(name: str) -> logging.Logger:
    """
    Set up a custom logger with the desired logging level and format.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger.
    """
    formatter = logging.Formatter(
        fmt="".join(
            [
                "{name}: {asctime} | {levelname} | line:{lineno} | ",
                "{process} >>> {message}",
            ]
        ),
        style="{",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger
