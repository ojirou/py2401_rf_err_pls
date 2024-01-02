import numpy as np
import seaborn as sns
from matplotlib import rcParams
import matplotlib.pyplot as plt
import webbrowser
from matplotlib import ticker
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import forestci as fci
def set_graph_params():
    rcParams['xtick.labelsize']=12
    rcParams['ytick.labelsize']=12
    rcParams['figure.figsize']=7,5
    sns.set_style('whitegrid')
base_folder=r'C:\\Users\\user\\git\\github\\py2401_rf_err_pls\\'
FileName=base_folder+'regression_pls.csv'
PdfFile_err=base_folder+'pdf\\PdfFile_err.pdf'
columns=['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11','x12','x13','x14','x15','x16','x17','x18','x19','Target']
target_column='Target'
df=pd.read_csv(FileName, encoding='utf-8', engine='python', usecols=columns)
features=[c for c in df.columns if c !=target_column]
train, test=train_test_split(df, test_size=0.2, random_state=115)
X_train=train[features]
y_train=train['Target'].values
X_test=test[features]
y_test=test['Target'].values
model=RandomForestRegressor(n_estimators=366, max_depth=32, max_features=6, random_state=444)
model.fit(X_train, y_train)
pred_train=model.predict(X_train)
pred_test=model.predict(X_test)
r2_train=r2_score(y_train, pred_train)
adjusted_r2_train=1-(1-r2_train)*(len(y_train)-1)/(len(y_train)-X_train.shape[1]-1)
mse_train=mean_squared_error(y_train, pred_train)
rmse_train=mse_train**0.5
r2_test=r2_score(y_test, pred_test)
adjusted_r2_test=1-(1-r2_test)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
mse_test=mean_squared_error(y_test, pred_test)
rmse_test=mse_test**0.5
set_graph_params    
sns.set_color_codes()
plt.figure()
fig, ax=plt.subplots(figsize=(7,7))
plt.xlim([-12,2])
plt.ylim([-12,2])
sns.set(font='Arial')
plt.scatter(y_train, pred_train, alpha=0.5, color='blue', label='Train')
plt.scatter(y_test, pred_test, alpha=0.5, color='green', label='Test')
plt.plot(np.linspace(-12, 2, 14), np.linspace(-12, 2, 14), 'black')
plt.xlabel('True Target', fontsize=14)
plt.ylabel('Predicted True Target', fontsize=14)
plt.title(f'Train - Adjusted R2 Score: {adjusted_r2_train:.3f}, RMSE: {rmse_train:.3f}\nTest - Adjested R2 Score: {adjusted_r2_test:.3f}, RMSE: {rmse_test:.3f}', fontsize=13)
plt.legend(fontsize=14)
plt.show()
plt.figure()
fig, ax=plt.subplots(figsize=(7,7))
plt.xlim([-12,2])
plt.ylim([-12,2])
sns.set(font='Arial')
V_IJ_unbiased=fci.random_forest_error(model, X_train, X_test)
plt.scatter(y_train, pred_train, alpha=0.5, color='blue', label='Train')
plt.errorbar(y_test, pred_test, yerr=np.sqrt(V_IJ_unbiased), fmt='o', alpha=0.5, color='green', label='Test')
plt.plot(np.linspace(-12,2,14), np.linspace(-12,2,14), 'black')
plt.ylabel('Predicted Target', fontsize=14)
plt.title(f'Train - Adjusted R2 Score: {adjusted_r2_train:.3f}, RMSE: {rmse_train:.3f}\nTest - Adjusted R2 Score: {adjusted_r2_test:.3f}, RMSE: {rmse_test:.3f}', fontsize=13)
plt.legend(fontsize=14)
plt.savefig(PdfFile_err)
webbrowser.open_new(PdfFile_err)