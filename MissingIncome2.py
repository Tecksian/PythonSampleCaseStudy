import statsmodels.api as sm
import pandas as pd
from UtilityFunctions import build_eqn
from patsy import dmatrices, Sum, Diff, Poly
from patsy.builtins import standardize
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler


df = sm.load('nan_income_only.pickle')

m=df['X30'].mean()
# Create a new variable that adds 1 to a ratio of two variables, but in such
# a way as to make cases where the denominator is zero less problematic.
df['income'] = df['X13'].copy()
df['x_ratio'] = (df['X30']+m)/(m+df['X21'])

eqn = build_eqn(df, y='income',omit=['x_ratio','regressand', 'X13', 'income_present', 'any_regressand', 'income'])
print(eqn)

y, X = dmatrices(eqn, data=df, return_type='dataframe')

y_scaler= StandardScaler()
y_scaler.fit(y)
y=y_scaler.transform(y)

X_scaler= StandardScaler()
X_scaler.fit(X)
X=X_scaler.transform(X)

from sklearn.ensemble import RandomForestRegressor
mod=RandomForestRegressor(200)
res=mod.fit(X,pd.np.ravel(y))

yt=y_scaler.inverse_transform(y)
yt=pd.np.ravel(yt)
yp = res.predict(X)
yp=y_scaler.inverse_transform(yp)

r2 = r2_score(yt,yp)
rmse = mean_absolute_error(yt,yp)

print('r2 score: ' + str(r2))
print('RMSE(?):  ' + str(rmse))

#
import matplotlib.pyplot as plt

x=range(0,1000)
plt.scatter(yt[0:1000],yp[0:1000])
#plt.scatter(x,, color='red', label = 'Predicted')

plt.show()
