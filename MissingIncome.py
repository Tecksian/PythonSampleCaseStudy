import statsmodels.api as sm
import pandas as pd
from UtilityFunctions import build_eqn
from patsy import dmatrices, Sum, Diff, Poly
from patsy.builtins import standardize
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# df=sm.load('full_transformed.pickle')
# print('transformed data loaded')
# grouped=df.groupby('any_regressand')
# print('transformed data grouped')
#
# nan_income_only = grouped.get_group(False).copy()
# print('NaN regressands selected')
# nan_income_only.to_pickle('nan_income_only.pickle')

df = sm.load('nan_income_only.pickle')


# new_df = pd.DataFrame({'rpm' : df['X21'].values + df['X21'].mean()})
# new_df['vpm'] = df['X30'].values + df['X30'].mean()
# new_df['income'] = df['X13'].copy()
#
# new_df['income']/new_df['income'].mean()
#
# new_df=pd.np.log(new_df)
# new_df['term'] = df['X7']
# df['X13']=df['X13']
# #df['X13']=df['X13'].clip_upper(1000000)
# print('data loaded')
# df['mean_plus_ratio'] = df['X21'].mean() + df['X21']
# df['mean_plus_value'] = df['X30'].mean() + df['X30']
# df['inv_adj_ratio'] = 1.0/df['mean_plus_ratio']
# df['inv_ratio1'] = df['X29']/df['mean_plus_ratio']
# df['inv_ratio2'] = df['X30']/df['mean_plus_ratio']
from numpy import power

m=df['X30'].mean()
new_df = pd.DataFrame({'income' : df['X13'].copy()})
new_df['x_ratio'] = (df['X30']+m)/(m+df['X21'])
new_df['term'] = df['X7'].copy()
new_df['rank'] = df['X8'].copy()
new_df['subrank'] = df['X9'].copy()
new_df['income']=new_df['income']
new_df['state'] = df['X20'].copy()
new_df['X24'] = df['X24'].copy()
new_df['X23'] = df['X23'].copy()
new_df['X31'] = df['X31'].copy()
new_df['X11'] = df['X11'].copy()
new_df['X12'] = df['X12'].copy()
new_df['X14'] = df['X14'].copy()
new_df['X22'] = df['X22'].copy()
new_df['amt_req'] = df['X4'].copy()
new_df['any_delinq'] = df['any_delinq'].copy()
new_df['any_pub_recs'] = df['any_pub_recs'].copy()

y,X = dmatrices('income ~ 0+ x_ratio+ amt_req+any_pub_recs + any_delinq + X23+X24+X31\
+ C(subrank,Diff) + C(state,Sum)', data=new_df, return_type='dataframe')
#~income ~ x_ratio*C(term, Poly)*C(rank, Helmert)'
# y_scaler= StandardScaler()
# y_scaler.fit(y)
# y=y_scaler.transform(y)
# X_scaler= StandardScaler()
# X_scaler.fit(X)
# X=X_scaler.transform(X)
from sklearn.ensemble import RandomForestRegressor
mod=RandomForestRegressor(20)
res=mod.fit(X,pd.np.ravel(y))
yp = res.predict(X)
r2 = r2_score(y,yp)
rmse = mean_absolute_error(y,yp)

print('r2 score: ' + str(r2))
print('RMSE(?):  ' + str(rmse))

# print('dmatrices built')
# mod=sm.OLS(y,X, hasconst=True)
# print('mod instantiated')
# res = mod.fit(normalized=True)

#mod=sm.RLM(y,X, norm=sm.robust.norms.AndrewWave())
# mod=sm.RLM(y,X, norm=sm.robust.norms.TukeyBiweight())
# print('mod instantiated')
# res = mod.fit(scale_est=sm.robust.HuberScale())
# print ('fit run')
# print(res.summary())

yt=y['income']
# yp=res.fittedvalues

# yt=y_scaler.inverse_transform(y)
# yp=y_scaler.inverse_transform(res.fittedvalues)

# resids=res.resid
# print(mean_absolute_error(yt,yp))
import matplotlib.pyplot as plt
# plt.plot(x_new,sorted(yp))
# plt.plot(x_new,sorted(yt))
#plt.plot(x_new,pd.np.exp(yt))


plt.scatter(yp[1:1000],yt[1:1000], color='blue',label='Data')
plt.scatter(yp[1:1000],yp[1:1000] + (yp[1:1000]-yt[1:1000]), color='red', label = 'Predicted +/- residual')
# plt.scatter(yt[1:100],yt[1:100]+resids[1:100])
plt.show()
print(max(yp),max(yt))
print(min(yp),min(yt))
print(max(abs(yp-yt)))