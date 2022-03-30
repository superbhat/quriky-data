"""
Logger Module, to be used for adding default config.
Usage - Call this module for logging.
"""
import logging
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(format=logformat, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()
logger.setLevel('INFO')