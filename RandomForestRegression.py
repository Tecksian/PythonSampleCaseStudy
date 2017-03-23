from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import FeatureAgglomeration
from CommonImports import *
import pickle

def TrainRFRegression(df1):
    # generate the equation to use for our design matrices
    eqn = build_eqn(df1,'regressand', ['any_regressand','X25','X26','X29'])

    # build our design matrices
    y, X = dmatrices(eqn, data=df1,return_type = 'dataframe')

    # employ clustering to reduce our dimensionality
    X_reduction = FeatureAgglomeration(n_clusters=50).fit(X,pd.np.ravel(y))
    reduced_X = X_reduction.transform(X)

    # define our regressor
    mod = RandomForestRegressor(n_estimators=50)

    # fit our data
    res = mod.fit(reduced_X,pd.np.ravel(y))

    # evaluate our fit
    yp = pd.DataFrame({'predicted': res.predict(reduced_X)})
    yp=yp['predicted']
    yt=y['regressand']
    r2 = metrics.r2_score(yt,yp)
    rmse = metrics.mean_absolute_error(yt,yp)
    # save our model, including scalers and feature agglomerator
    with open('RFR_trained_model.pickle','wb') as output:
        pickle.dump(res, output, pickle.HIGHEST_PROTOCOL)

    return r2, rmse

def TestRFRegression(df1):

    # generate the equation to use for our design matrices
    eqn = build_eqn(df1,'regressand', ['any_regressand','X25','X26','X29'])

    # build our design matrices
    X = dmatrix(eqn.replace('regressand ~ ',''), data=df1,return_type = 'dataframe')

    # load our model, including scalers and feature agglomerator
    with open('RFR_trained_model.pickle','rb') as input:
        res = pickle.load(input)

    # employ clustering to reduce our dimensionality
    X_reduction = FeatureAgglomeration(n_clusters=50).fit(X)
    reduced_X = X_reduction.transform(X)
    # define our regressor
    mod = RandomForestRegressor(n_estimators=50)

    # predict the interest rates
    yp = pd.DataFrame({'predicted' : res.predict(reduced_X)})

    return yp
