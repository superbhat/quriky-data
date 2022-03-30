# Data Cleansing
This package helps in cleansing .csv file i.e. removing quirky/junk data. Generates output as a compressed parquet file.

## Assumption.
- Dataset received will have the following columns.
  - **donor_id**.
  - **postcode**. 
  - **gender**.
  - **birthdate**.
  - **donor_type**.
- File size expected not be greater than 1 Gib.
- Used **Pandas** for Transformation Process.
- Commands mentioned are the one used on MAC OS.
- Input data received should in .csv format.
- Python3.8 version used.

## Data Issues and Resolution.
- Found almost **50%** of data was duplicate,seems the whole file was copied again inside the file creating duplicates. Resolution sorted was to remove row level duplicates before going to column level.
- **donor_id** - Other than valid values UUID/19digit numbers there were other values discovered i.e. scientific values, negative value, decimal value and nan values. To solve this donor_id col was transformed with the help of is_valid_donor_id function
which examines junk data and converts into nan values. Now we have only three types of data UUID/19Digit/NAN values which simplifies querying data. See `is_valid_donor_id` function for furthers details.
- **postcode** - As per requirement it needs to comply with Australian Format Post Code. After examination found that postcode data had leading junk values, some codes where enclosed under brackets, double quotes and also had 5 digits codes. To resolve, regex expression where used to find 3/4digit numbers only. 
Extracted 3/4 digit as valid post codes everything else was discarded as in replaced with NAN.See `is_valid_post_code` function for furthers details.
- **gender** - Issue found, it had trailing spaces, junk values etc. Male and Females was misspelled. Valid data considered as 'M/F/Null'. Also had`['UNK', '\x0bOther', 'Unknown', 'Other', 'gender']`. Also, any values starting with M/F were replaced by M/F.
See `is_valid_gender` function for furthers details.
- **birthdate** - Received wrong date as '3531-03-17'. These dates where caught in exception and was converted into NAN. See `is_valid_birthdate` function for furthers details.  
- **donor_type** - It had int, float, string all trailed with junk, spaces and unknown characters. `is_valid_donor_type` was used to counter the issues. Initially was checked with int and float values if not exception raised were converted into NAN values.

## Components.
- Python3.8
- Pandas(1.4.1)
- Fastparuet
- Venv

## Build and Run.
### Steps
- `git clone https://github.com/superbhat/quriky-data.git` - Clone the project into a local drive.
- `cd quriky-data`
- Create virtual env using CLI on terminal- `python3 -m venv ./venv`
- Activate the virtual env - `source venv/bin/activate`
- Install the project - `pip install -e .`
- Run CLI command `transform -h` to get information. 
- CLI command to execute the process `transform -s data/donors.csv`
- Target data will be written into `Output/donors.gzip`
- Run `deactivate` to come out of venv.

## Test
- Run CLI command `pytest test/` to perform unit test.
