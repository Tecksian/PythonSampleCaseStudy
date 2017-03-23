import MetadataInfo as mdi
import pandas as pd
import datetime as dt

#define a converter for use with PANDAS' read_csv file
converter={}

# Transform currencies to be more easily usable
chars_to_remove = "$,%"

remove_chars_from = mdi.has_dollarsign + mdi.has_percentsign
remove_chars = lambda x : float(x.translate(str.maketrans('', '', chars_to_remove))) if x else None
for field in remove_chars_from:
    converter[field]=remove_chars

fill_rating = lambda x : x if x else 'NO VALUE ENTERED'
converter['X8']= fill_rating
converter['X9']= fill_rating

fill_residence_status = lambda x : x if x else 'NO VALUE ENTERED'
converter['X12'] = fill_residence_status

fill_employer = fill_residence_status
converter['X10'] = fill_employer

# convert a datetime to number of days, making it scale
def to_days(x):
    reference_date=dt.datetime.strptime('Feb-1-2016','%b-%d-%Y').date()
    dateparts = x.split('-')
    if x:
        if x[0].isdigit():
            diff = reference_date - dt.datetime.strptime(x,"%d-%b").date()
        else:
            diff = reference_date - dt.datetime.strptime(x,"%b-%y").date()
        return float(diff.days / ( 365) )

converter['X23'] = to_days

#removing the years makes it more clearly ordinal
def remove_years(x):
    '''
    Changes the length of employment to obvious ordinal ranks
    :param x: input string for employment length
    :return: number representing ordinal rank
    '''
    if '<' in x:
        return 0
    elif '+' in x:
        return 10
    elif x=='n/a' or x=='':
        return -1
    else:
        return int(x.replace(' years','').replace(' year',''))

converter['X11']=remove_years

# Convert 36 or 60 months into a number, for more plain ordinal ranking
remove_months = lambda x : x.replace(' months','').replace(' ','')
converter[mdi.has_phrase_months] = remove_months

# define the data types we wish the import to assign
field_dtypes={}
for field in mdi.scale_fields:
    field_dtypes[field]=pd.np.float64

for field in mdi.nominal_fields:
    field_dtypes[field] = pd.np.str

for field in mdi.ordinal_fields:
    field_dtypes[field] = pd.np.float64

for field in mdi.string_fields:
    field_dtypes[field] = pd.np.str

for field in mdi.date_fields:
    field_dtypes[field] = pd.np.timedelta64
    converter[field] = to_days

def custom_import_data(rows=None):
    '''
    Import the training data from the CSV file
    :param rows: number of rows to import. If None, import them all
    :return: a Pandas DataFrame containing the data
    '''
    return pd.read_csv('Data for Cleaning & Modeling.csv',nrows=rows, header=0, low_memory=False, converters=converter, dtype=field_dtypes);

def custom_import_test_data(rows=None):
    '''
    Import the test data from the CSV file
    :param rows: number of rows to import. If None, import them all
    :return: a Pandas DataFrame containing the data
    '''
    return pd.read_csv('Holdout for Testing.csv',header=0,nrows=rows, low_memory=False, converters=converter, dtype=field_dtypes);
