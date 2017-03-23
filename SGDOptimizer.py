from CommonImports import *
from sklearn.grid_search import GridSearchCV
from sklearn.cluster import FeatureAgglomeration
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from DataTransformations import *

df1=transform_data(sm.load('full_chain_data.pickle'))
base_parameters = {'alpha' : [.00001,.0001,.001,.01, .1] , \
                   'epsilon' : [.1, .2, .3], \
                   'penalty' : ['l2', 'elasticnet'], \
                   'loss' : ['huber', 'epsilon_insensitive']}

eqn = build_eqn(df1,'regressand', ['any_regressand','X25','X26'])
print(eqn)
y, X = dmatrices(eqn, data=df1,return_type = 'dataframe')
print('design matrices generated')

X_reduction = FeatureAgglomeration(n_clusters=100).fit(X,pd.np.ravel(y))
reduced_X = X_reduction.transform(X)

X_scaler = StandardScaler().fit(reduced_X)
std_X = X_scaler.transform(reduced_X)

y_scaler = StandardScaler().fit(y)
std_y = y_scaler.transform(y)
print (std_y.shape)
#svr = SGDRegressor(n_iter = 20, penalty = 'elasticnet', loss='epsilon_insensitive')
svr = SGDRegressor(n_iter = 30, penalty = 'elasticnet', loss= 'epsilon_insensitive', alpha = .0014, epsilon = .32)

#parameters = { 'alpha' : pd.np.arange(.001,.002,.0001), 'epsilon' : pd.np.arange(.25,.35,.01)}
parameters = { 'l1_ratio' : pd.np.arange(.1,.6,.02)}

SGD_clf = GridSearchCV(svr, parameters, verbose = True)
SGD_clf.fit(std_X, pd.np.ravel(std_y))
scores = SGD_clf.grid_scores_
print(scores)
print(SGD_clf.best_params_)
print( 'Best score: '+str(SGD_clf.best_score_))
print( 'Best params: '+str(SGD_clf.best_params_))

std_yp = SGD_clf.predict(std_X)
print( 'Best r2: '+str(metrics.r2_score(std_yp,std_y)))
print( 'Best RMSE: '+str(metrics.mean_absolute_error(std_yp,std_y)))

yp = y_scaler.inverse_transform(std_yp)
yt = y_scaler.inverse_transform(std_y)

print( 'Best r2: '+str(metrics.r2_score(yp,yt)))
print( 'Best RMSE: '+str(metrics.mean_absolute_error(yp,yt)))
