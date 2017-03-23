import pandas as pd
import MetadataInfo as mdi

def transform_data(df, to_scale = False):
    # create a new column only reflecting whether or not people have any public records.
    df['any_pub_recs'] = df['X26'].notnull()
    # reassign the original column from ordinal to scale
    df['X26']=df['X26'].astype(pd.np.float64)

    # create a new column only reflecting whether or not people have any delinquincies
    df['any_delinq'] = df['X25'].notnull()
    # reassign the original column from ordinal to scale.
    df['X25']=df['X25'].astype(pd.np.float64)

    # create a new column only reflecting whether or not income (X13) is empty.
    df['income_present'] = df['X13'].notnull()
    # create a new column only reflecting whether or not the regressand (X1) is empty
    df['any_regressand'] = df['regressand'].notnull()

    # set empty string fields to be something rather than nothing
    df['X16'] = df['X16'].fillna('NULL STRING REPLACEMENT')

    if to_scale:
        # pretend some ordinal variables are scale
        to_scale_fields = ['X11', 'X22', 'X24', 'X27', 'X28', 'X31']
        for field in to_scale_fields:
            df[field] = df[field].astype(pd.np.float64)
        df.to_pickle('full_transformed_to_scale.pickle')
    else:
        df.to_pickle('full_transformed.pickle')

    return df
