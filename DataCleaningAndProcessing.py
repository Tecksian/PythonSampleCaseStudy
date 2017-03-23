import pandas as pd
import MetadataInfo as mdi
import datetime as dt

#process imported data
def process_data(df_input):
    df_processed = pd.DataFrame({'loan_id' : df_input.index } )

    # NOTE: the loan id (X2) is of no computational interest -- at least, if it is relevant, than something has gone very wrong upstream!
    # We don't keep applicant ID (X3), either, though it potentially could be used to fill in missing values later.
    # the interest rate assigned, X1, is our sole target regressand
    # Note: it is the only field we rename -- we deliberately leave the others as X#, to limit inuition sneaking in to
    # the analysis. Except when we want to use intuition -- but then we have to do a bit of work looking at the metadata.
    df_processed = pd.DataFrame({'regressand' : df_input[mdi.regressand] })

    # set our nominal (unordered categorical) variables
    for field in mdi.nominal_fields:
        df_processed[field] = pd.Categorical(df_input[field].values,ordered=False)#  .astype('category', ordered=False)

    # set our ordinal (ordered categorical) variables
    for field in mdi.ordinal_fields:
        df_processed[field] = pd.Categorical(df_input[field].values, ordered=True)

    # no dtype change necessary for scale fields (we except X1 and X2 as they are already in place
    for field in mdi.scale_fields:
        if field not in {'X2','X3'}: #ignore the loan and applicant IDs
            df_processed[field] = df_input[field].values

    for field in mdi.date_fields:
        df_processed[field] = df_input[field].astype(pd.np.float64)

    for field in mdi.string_fields:
        df_processed[field] = df_input[field]

    return df_processed

