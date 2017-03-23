import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from patsy import dmatrices, Sum, Diff, Poly

ols_results=sm.load('basic_OLS_results.pickle')

p='C(X20, Sum)'
params = ols_results.params
state_key_set =[key for key in params.keys() if p in key]

pvalues= ols_results.pvalues[state_key_set]

for key in state_key_set:
    if pvalues[key] <.05:
        print(key)

print(pvalue for pvalue in pvalues if pvalues.value() < .05)

plt.hist(pvalues.values.tolist(), bins=pd.np.arange(0,1,.05))
plt.show()
# print(ols_results.pvalues)


