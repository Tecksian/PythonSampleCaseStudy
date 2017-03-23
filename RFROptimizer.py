from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import FeatureAgglomeration
from CommonImports import *

df1=sm.load('full_chain_data.pickle')

# grouped = df.groupby(['any_pub_recs','any_delinq'])
#
# df1=grouped.get_group((True, True)).copy()


eqn = build_eqn(df1,'regressand', ['any_regressand','X25,X26'])
print(eqn)
y, X = dmatrices(eqn, data=df1,return_type = 'dataframe')


n_cluster_range=pd.np.arange(5,100,5)
n_clusters = 50
n_estimators_range = pd.np.arange(100,200,10)
rmse_values = []
r2_values = []
for n in n_estimators_range:
    X_reduction = FeatureAgglomeration(n_clusters=n_clusters).fit(X,pd.np.ravel(y))
    reduced_X = X_reduction.transform(X)
    mod = RandomForestRegressor(n_estimators=n)
    res = mod.fit(reduced_X,pd.np.ravel(y))
    yp = pd.DataFrame({'predicted': res.predict(reduced_X)})
    yp=yp['predicted']
    yt=y['regressand']
    r2 = metrics.r2_score(yt,yp)
    r2_values.append(r2)
    rmse = metrics.mean_absolute_error(yt,yp)
    rmse_values.append(rmse)
    print('n_clusters = '+str(n) + '   r2 score: ' + str(r2) + '   RMSE(?):  ' + str(rmse))

plt.plot(n_estimators_range,r2_values)
plt.plot(n_estimators_range, rmse_values)
plt.show()