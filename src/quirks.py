"""
A Class which takes in donors details and removed any junk/outlier data.
"""
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn' As sometimes it give FalsePositives.
import re
from src.setup_logger import logger
import uuid
import numpy as np


def is_valid_donor_id(val):
    """
    Perform data cleansing on donor_id values. Expected values are UUID/19Digit number
    :param val:data from the raw file
    :return: UUID/19Digit/NAN string values.
    """
    try:
        return str(uuid.UUID(str(val)))
    except Exception:
        if str(val).isdigit() and len(str(val)) == 19:
            return str(val)
        else:
            return np.nan


def is_valid_post_code(val):
    """
    Format postcode into a 3/4 digit post code.
    :param val:postcode
    :return:postcode/nan
    """
    try:
        if not pd.isna(val):
            # check for a 3 digit and 4 digit numbers. If 3 digit add leading 0.
            if re.search(r"(?<!\d)\d{3,4}(?!\d)", val):
                return re.findall(r"(?<!\d)\d{3,4}(?!\d)", val)[0].zfill(4)
            else:
                # check for a 5 digit numbers starting with 0.
                if re.search(r"(?<!\d)\d{5}(?!\d)", val):
                    return re.findall(r"(?<!\d)\d{5}(?!\d)", val)[0][1:]
                else:
                    # for everything else return nan value.
                    return np.nan
        else:
            return np.nan
    except Exception:
        logger.error('New Junk Value Popped in for Post Code %s', val)
        raise Exception


def is_valid_gender(val):
    """
    Looks for Gender values ie F/M is found replaces it with F/M/Null.
    :param val:gender
    :return:gender
    """
    try:
        if str(val).strip()[0].upper() == 'M':
            return 'M'
        elif str(val).strip()[0].upper() == 'F':
            return 'F'
        else:
            # ['UNK', '\x0bOther', 'Unknown', 'Other', 'gender']
            return np.nan
    except Exception:
        logger.error('New Junk Value Popped in for Gender %s', val)
        raise Exception


def is_valid_birthdate(val):
    """
    Receives date as string convert into datetime if valid else populate NAN.
    :param val: birthdate
    :return: birthdate
    """
    try:
        return pd.to_datetime(val)
    except Exception:
        return np.nan


def is_valid_donor_type(value):
    """
    Looks for any int or float in a string. Return int value.
    :param value: int/float/string
    :return:int
    """
    try:
        if len(str(value)) <= 32:
            if isinstance(value, float):
                return int(value)
            elif isinstance(value, str):
                return int(float(value))
            else:
                return np.nan
        else:
            return np.nan
    except Exception:
        return np.nan


class RemoveQuirks:
    """
    Class to be called to perform data cleansing on the input file provided. Accepts source path.
    """
    def __init__(self, path):
        self.path = path

    def execute(self):
        """
        Main Method, which converts file into dataframe perfrom beloww steps
        - drop duplicates
        - apply transformation functions on columns.
        - transform column into respective datatype.
        - Rename, cast and DROPNA if NAN found in more than 3 columns.
        """
        logger.info('Create Dataframe for the file received')
        df = pd.read_csv(self.path)
        raw_count = df.shape[0]
        logger.info('Original Record Count %s', str(raw_count))

        # Remove any duplicate row, repeating itself.
        unique_df = df.drop_duplicates()
        unique_count = unique_df.shape[0]
        logger.info('Record Count after removing duplicates %s', str(unique_count))

        # Percentage Drop in Records
        drop_percent = int((abs(unique_count - raw_count) / raw_count) * 100.0)
        logger.warning('Percent of Duplicates is %s', str(drop_percent))

        # Perform Transformation/Validation on each columns.
        logger.info('donor_id processing')
        unique_df.loc[:, 'transformed_donor_id']\
            = unique_df['donor_id'].map(is_valid_donor_id)

        # postcode
        logger.info('postcode processing')
        unique_df.loc[:, 'transformed_postcode']\
            = unique_df['postcode'].map(is_valid_post_code)

        # gender.
        logger.info('gender processing')
        unique_df.loc[:, 'transformed_gender']\
            = unique_df['gender'].map(is_valid_gender)

        # birth_date.
        logger.info('birth_date processing')
        unique_df.loc[:, 'transformed_birth_date']\
            = unique_df['birth_date'].map(is_valid_birthdate)

        # donor_type.
        logger.info('donor_type processing')
        unique_df.loc[:, 'transformed_donor_type']\
            = unique_df['donor_type'].map(is_valid_donor_type)

        # Convert donor_type into int32 datatype.
        logger.info('Casting donor_type into int32')
        unique_df['transformed_donor_type'] =\
            unique_df['transformed_donor_type'].fillna(0).astype(np.int32)

        # Generate Dataframe to be written into Parquet file.
        logger.info('extracting transformed columns only.')
        transformed_df = unique_df.filter(['transformed_donor_id',
                                           'transformed_postcode',
                                           'transformed_gender',
                                           'transformed_birth_date',
                                           'transformed_donor_type'], axis=1)

        # Rename the columns.
        logger.info('Rename transformed columns only.')
        transformed_df.rename(columns={'transformed_donor_id': 'donor_id',
                                       'transformed_postcode': 'postcode',
                                       'transformed_gender': 'gender',
                                       'transformed_birth_date': 'birth_date',
                                       'transformed_donor_type': 'donor_type'}, inplace=True)

        # Update the datatype.
        logger.info('casting other columns')
        final_df = transformed_df.astype({'donor_id': 'string',
                                          'postcode': 'string',
                                          'gender': 'string', })

        # Drop NA values if found in 4 columns.
        logger.info('Dropping Rows which have 4 columns as NAN.')
        final_df = final_df.dropna(axis=0, thresh=4, how="any")

        # DataTypes.
        logger.info('DataType of Columns in Final DF Datatype %s', str(final_df.dtypes))

        # Final number of records.
        logger.info('Final Record Count %s', str(final_df.shape[0]))

        # Write to Parquet File.
        final_df.to_parquet('Output/donors.gzip', compression='gzip')
        logger.info('Data Cleansing Activity Done, File Generated Path data/output/donors.gzip', )
