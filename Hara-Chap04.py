import pandas as pd
import io
import os
import matplotlib.pyplot as plt

# カレントディレクトリの場所を確認
os.getcwd()
# csvデータの読み込み
input_data = pd.read_csv("carprice.csv")

# データの先頭10行を表示 head()
input_data.head(10)

# データの概要を表示 info()
input_data.info()

# データの記述統計をまとめて表示 describe()
input_data.describe()

# 各種記述統計量を計算 mean()
## 平均
print(input_data.price.mean())
## 以下同様

# pandasのgroupbyでカテゴリ別に統計量を計算 groupby
## 平均
print(input_data.groupby("doornumber")["price"].mean())
## 以下同様

# ヒストグラム hist()
## 価格のヒストグラム
plt.hist(input_data.price)
plt.xlabel('price') # x軸のラベル
plt.ylabel('count') # y軸のラベル
plt.grid(True) # 補助線を引く

# 箱ひげ図 boxplot
plt.boxplot(input_data.price)
plt.grid(True)

# 4.5 データを把握する 変数間の関係性

# scipyパッケージを読む
import scipy.stats
# エンジンサイズと価格の散布図
plt.scatter(input_data.enginesize, input_data.price, s = 50, c = "blue", alpha = "0.3", linewidths = 1, edgecolors = "blue")
plt.title('Engine and Price')
plt.ylabel('Price')
plt.xlabel('Engine')

# 共分散や相関行列

# 科学技術計算ライブラリ numpyを読み込む
import numpy as np
#共分散 cov
print(np.cov(input_data.price, input_data.enginesize))
#相関行列 corrcoef
print(np.corrcoef(input_data.price, input_data.enginesize))

# 散布図とヒストグラムを書く
import seaborn as sns
sns.jointplot(input_data.price, input_data.enginesize)

# 5つのをまとめてリストx_listに格納しておく
x_list = pd.concat([input_data.price, input_data.enginesize, input_data.wheelbase, input_data.horsepower, input_data.carheight], axis = 1)
# pairplot 
sns.pairplot(x_list, kind = "reg")

# 相関係数をプロットし，色で強弱を示す。
plt.figure(figsize = (12, 9)) # 図の大きさ
sns.heatmap(x_list.pct_change().corr(), annot = True, cmap = "Blues")

# 作業結果の保存
sns.pairplot(x_list, kind = "reg").savefig("test.png")
