import os
import shutil

from extract.ftp import download_latest_cnes_dataset
from transform.cnes import get_transformed_df
from utils.logger import Logger
from utils.unzip import unzip

EXTRACTION_DIR = "extracted"
TEMP_DIR = "temp/"
OUTPUT_FILE_NAME = "cnes-hospitais"


def main():
    logger = Logger()
    err = run(logger)
    if err:
        logger.info("Terminated due to error")
        logger.error(err)
        return

    logger.info("Finished without errors")


def run(logger):
    try:
        os.mkdir(TEMP_DIR)

        logger.info("Downloading latest archived CNES dataset from FTP server...")
        cnes_zip_file, version = download_latest_cnes_dataset(TEMP_DIR)

        logger.info("Extracting archived CNES dataset to {}...".format(TEMP_DIR + EXTRACTION_DIR))
        unzip(cnes_zip_file, TEMP_DIR + EXTRACTION_DIR)

        logger.info("Applying transformations...")
        df = get_transformed_df(TEMP_DIR + EXTRACTION_DIR, version)

        logger.info("Generating {}.csv...".format(OUTPUT_FILE_NAME))
        df.to_csv(OUTPUT_FILE_NAME + ".csv", index=False)

        logger.info("Cleaning temp files and directories...")
        shutil.rmtree(TEMP_DIR)
    except Exception as e:
        return e


main()
