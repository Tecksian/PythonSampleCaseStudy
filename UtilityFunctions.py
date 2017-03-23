# import statsmodels.api as sm
import MetadataInfo as mdi
#
#
# def get_processed_data():
#     print('loading processed_data')
#     df1=sm.load('full_processed.pickle')
#
#     #print('loading df2')
#     #df2=sm.load('df2.pkl')
#     return df1
#
# def get_transformed_data():
#     print('loading transformed_data')
#     df1=sm.load('full_transformed.pickle')
#
#     #print('loading df2')
#     #df2=sm.load('df2.pkl')
#     return df1

def build_eqn(df,y='regressand', omit = []):
    eqn=y + ' ~ '
    for key in df.keys():
        if key not in (omit+[y]) \
                and key not in mdi.exclude_fields_from_eqn:
            eqn += '  '+key
    eqn=eqn.replace('  ',' + ')
    eqn=eqn.replace('~ +  ','~ ')
    for key in df:
        if key not in ['any_regressand']:
            if key == 'X7':
                eqn = eqn.replace(key,'C(' + key + ',Poly)')
            elif key in (set(mdi.ordinal_fields) - set(mdi.to_scale_fields)):
                eqn = eqn.replace(key,'C(' + key + ',Diff)')
            elif key in mdi.nominal_fields:
                eqn = eqn.replace(key,'C(' + key + ',Sum)')

    return str(eqn)

def custom_standardize(df):
    return (df-df.mean())/df.std()