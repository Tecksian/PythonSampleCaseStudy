from CommonImports import *
from sklearn.linear_model import SGDRegressor
from sklearn.cluster import FeatureAgglomeration
from sklearn.preprocessing import StandardScaler
import pickle

n_clusters = 50
n_iterations = 100
def TrainSGDRegression(df1):
    # generate the equation to use for our design matrices
    eqn = build_eqn(df1,'regressand', ['any_regressand','X25','X26','X29','X13'])

    # build our design matrices
    y, X = dmatrices(eqn, data=df1,return_type = 'dataframe')

    # employ clustering to reduce our dimensionality
    X_reduction = FeatureAgglomeration(n_clusters=n_clusters).fit(X)
    reduced_X = X_reduction.transform(X)
    X_scaler = StandardScaler().fit(reduced_X)
    std_X = X_scaler.transform(reduced_X)

    # y_scaler = StandardScaler().fit(y)
    # standardize our data

    # std_y = y_scaler.transform(y)

    # define our regressor
    mod = SGDRegressor( loss= 'epsilon_insensitive', penalty = 'elasticnet', alpha = 0.0014, epsilon = 0.32, n_iter=n_iterations)
    # fit our data
    #res = mod.fit(std_X,pd.np.ravel(std_y))
    res = mod.fit(std_X,pd.np.ravel(y))

    # evaluate our fit
    yp=res.predict(std_X)

    yp = pd.DataFrame({'predicted': yp})
    yp=yp['predicted']
    yt=y['regressand']
    r2 = metrics.r2_score(yt,yp)
    rmse = metrics.mean_absolute_error(yt,yp)

    #save our model
    with open('SGD_trained_model.pickle','wb') as output:
        pickle.dump(res, output, pickle.HIGHEST_PROTOCOL)

    return r2, rmse

def TestSGDRegression(df1):

    # generate the equation to use for our design matrices
    eqn = build_eqn(df1,'regressand', ['any_regressand','X25','X26','X29','X13'])

    # build our design matrices
    X = dmatrix(eqn.replace('regressand ~ ','0+'), data=df1,return_type = 'dataframe')

    # load our model, including scalers and feature agglomerator
    with open('SGD_trained_model.pickle','rb') as input:
        res = pickle.load(input)

    # employ clustering to reduce our dimensionality
    X_reduction = FeatureAgglomeration(n_clusters=n_clusters).fit(X)
    reduced_X = X_reduction.transform(X)

    # standardize our data
    X_scaler = StandardScaler().fit(reduced_X)
    std_X = X_scaler.transform(reduced_X)

    # predict the interest rates
    yp = res.predict(std_X)

    return yp
