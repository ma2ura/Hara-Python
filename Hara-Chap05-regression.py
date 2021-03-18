# パッケージをインポート
import pandas as pd # データ解析ライブラリ
import statsmodels.api as sm # 統計解析ソフト

# データを読み込む
input_data = pd.read_csv("carprice.csv")
#最初の10行を表示
input_data.head(10)

# 単回帰分析を行う。最小二乗法で推定する 
# 従属変数をprice，独立変数をenginesizeとする線形回帰モデル
model = sm.OLS(input_data.price, sm.add_constant(input_data.enginesize))
results = model.fit() # 推定
print(results.summary()) # 結果を表示
print('p-values\n', results.pvalues) # p値だけを表示

#モデルで利用する変数を接合し, ひとつの DataFrame にする
#読み込むデータを変えれば, 説明変数や被説明変数を変えることが可能
x_list = pd.concat([input_data.price, input_data.enginesize,input_data.wheelbase, input_data.horsepower, input_data.carheight], axis=1)

x_list2 = x_list.drop("price", 1) # price以外の4つだけをx_list2に 
price = input_data.price # priceだけを個別におく

#重回帰分析の結果を表示する
# 従属変数をprice，独立変数をx_list2の4つの変数として最小二乗法により推定
model = sm.OLS(price, sm.add_constant(x_list2))
result =model.fit()
print(result.summary())
print(result.pvalues)

#ダミー変数を get_dummies で作成する
# pandasのget_dummiesをつかってダミー変数を作成する。
input_data2=pd.get_dummies(input_data)
# カテゴリー変数にたいして自動的にダミー変数を作成
pd.get_dummies(input_data.doornumber)
#変数リストをプロットする たくさんの変数が作成されている。
print(input_data2.columns.values)


# 機械学習ライブラリ sklearnから，linear_model と datasets を読み込む
from sklearn import linear_model, datasets
# LinearRegressionを読み込む
from sklearn.linear_model import LinearRegression

# pandasのconcat をつかって6個の変数を抽出して1つのDataFrame x_list3にまとめる
x_list3 = pd.concat([input_data2.enginesize,input_data2.wheelbase, input_data2.horsepower, input_data2.carheight, input_data2.doornumber_four, input_data2.fueltype_gas], axis=1)
# input_data2からpriceを取り出してprice2に格納
price2 = input_data2.price


#重回帰分析の結果を表示する
model = sm.OLS(price2, sm.add_constant(x_list3))
result =model.fit()
print(result.summary())
print(result.pvalues)

# 多重共線性の確認
## statsmodels.stats.outliers_influenceの全モジュールをインポート
from statsmodels.stats.outliers_influence import * 
# modelに格納された線型回帰モデルの独立変数の列数をexog.shape[]で取る
num_cols = model.exog.shape[1] 
print(num_cols) # 独立変数の列数
# 独立変数ごとにVIFを計算する
vifs = [variance_inflation_factor(model.exog, i) for i in range (0, num_cols)]
# 結果をデータフレームとしてpdvに格納する
pdv = pd.DataFrame(vifs, index=model.exog_names, columns=["VIF"])
print(pdv) # 結果を表示