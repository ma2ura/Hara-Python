# パッケージをインポート
import pandas as pd
import statsmodels.api as sm


# データを読み込む
input_data = pd.read_csv("carprice.csv")

# 単回帰分析を行う。最小二乗法で推定する 
model = sm.OLS(input_data.price, sm.add_constant(input_data.enginesize))
results = model.fit()
print(results.summary())
print('p-values\n', results.pvalues)


#モデルで利用する変数を接合し, ひとつの DataFrame にする
#読み込むデータを変えれば, 説明変数や被説明変数を変えることが可能
x_list = pd.concat([input_data.price, input_data.enginesize,input_data.wheelbase, input_data.horsepower, input_data.carheight], axis=1)

x_list2 = x_list.drop("price", 1)
price = input_data.price

#重回帰分析の結果を表示する
model = sm.OLS(price, sm.add_constant(x_list2))
result =model.fit()
print(result.summary())
print(result.pvalues)

#ダミー変数を get_dummies で作成する
input_data2=pd.get_dummies(input_data)
#変数リストをプロットする
print(input_data2.columns.values)


# ダミー変数を組み込んだ回帰分析
from sklearn import linear_model, datasets
from sklearn.linear_model import LinearRegression

#モデルで利用する変数を接合し, ひとつの DataFrame にする
#読み込むデータを変えれば, 説明変数や被説明変数を変えることが可能
x_list3 = pd.concat([input_data2.enginesize,input_data2.wheelbase, input_data2.horsepower, input_data2.carheight, input_data2.doornumber_four, input_data2.fueltype_gas], axis=1)
price2 = input_data2.price


#重回帰分析の結果を表示する
model = sm.OLS(price2, sm.add_constant(x_list3))
result =model.fit()
print(result.summary())

print(result.pvalues)

#多重共線性が発生していないか確認する
from statsmodels.stats.outliers_influence import * num_cols = model.exog.shape[1] 
print(num_cols) #説明変数の列数
# VIF
vifs = [variance_inflation_factor(model.exog, i) for i in range(0, num_cols)]
pdv = pd.DataFrame(vifs, index=model.exog_names, columns=["VIF"])
print(pdv)