import pandas as pd
import io
import os
import matplotlib.pyplot as plt

# カレントディレクトリの場所を確認
os.getcwd()
# csvデータの読み込み
input_data = pd.read_csv("carprice.csv")

# データの先頭10行を表示
input_data.head(10)

# データの概要を表示 info()
input_data.info()

# データの記述統計をまとめて表示 describe()
input_data.describe()

# 各種記述統計量を計算
## 平均
print(input_data.price.mean())
## 以下同様

# pandasのgroupbyでカテゴリ別に統計量を計算
## 平均
print(input_data.groupby("doornumber")["price"].mean())
## 以下同様

# ヒストグラム
## 価格のヒストグラム
plt.hist(input_data.price)
plt.xlabel('price') # x軸のラベル
plt.ylabel('count') # y軸のラベル
plt.grid(True) # 補助線を引く