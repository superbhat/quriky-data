"""
Accepts data in .csv file and generates parquet file free of any duplicates and junk data.
"""
import argparse
from src.quirks import RemoveQuirks
from src.setup_logger import logger

# CLI Interface Arguments.
parser = argparse.ArgumentParser(
    description="Script to perform data cleansing on .csv file and generates parquet file.",
    epilog="""""")
parser.add_argument(
    "--source",
    "-s",
    type=str,
    metavar="",
    required=True,
    help='Please provide .csv file path.')
args = parser.parse_args()


def main():
    """
    Call RemoveQuirks class, instantiate class with the source file path.
    Out data is in compressed praquet file written in Data/Output Path.
    """
    source = args.source
    logger.info('File Received %s', source)
    # Instantiate Class.
    logger.info('Instantiate class')
    obj = RemoveQuirks(path=source)

    logger.info('Start Data Cleansing Activity')
    obj.execute()


if __name__ == "__main__":
    main()
