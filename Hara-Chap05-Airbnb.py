# いつものライブラリの読み込み
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

# エクセルデータの読み込み
input_book = pd.ExcelFile('AB_NYC_2019.xlsx')
# input_book = pd.read_csv("AB_NYC_2019.csv")

# シート名sheet_namesをinput_sheet_nameに代入
input_sheet_name = input_book.sheet_names
# input_sheet_nameのデータの個数をnum_sheetに代入
num_sheet = len(input_sheet_name) # 1個
print(input_sheet_name) #エクセルシートの名前を表示

input_sheet_df = input_book.parse(input_sheet_name[0])
# head(10)で先頭10行を表示
input_sheet_df.head(10) 

# ダミー変数を作成 列番号を使ったケース
manhattan_dummy = input_sheet_df.iloc[:,5]
private_dummy = input_sheet_df.iloc[:,10]
home_dummy = input_sheet_df.iloc[:,11]
shared_dummy = input_sheet_df.iloc[:,12]
price = input_sheet_df.iloc[:,13]
minimum_nights = input_sheet_df.iloc[:,14]
number_of_reviews = input_sheet_df.iloc[:,15]
reviews_per_month = input_sheet_df.iloc[:,17]
calculated_host_listings_count = input_sheet_df.iloc[:,18]
availability_365 = input_sheet_df.iloc[:,19]

# ダミー変数を作成 変数名を使っても大丈夫
manhattan_dummy = input_sheet_df.Manhattan_dummry # dummryって...


#単回帰分析をscipyを使って分析する
result = scipy.stats.linregress(number_of_reviews, price)
print('傾き=', result.slope.round(4), '切片=', result.intercept.round(4), '信頼係数=', result.rvalue.round(4), 'p値=', result.pvalue.round(4), '標準誤差=', result.stderr.round(4))
result_slope = result.slope
result_intercept = result.intercept

# 散布図を作図
plt.plot(number_of_reviews, [result_slope * u + result_intercept for u in number_of_reviews])
plt.scatter(number_of_reviews,price) # 散布図を作成
plt.title('price and number_of_reviews in Airbnb Dataset') # 図タイトル
plt.ylabel('price') # y軸のラベル
plt.xlabel('number_of_reviews') # x軸のラベル
plt.show() # 表示

# 単回帰分析をstatsmodelsを使って分析
import statsmodels.api as sm
# 単回帰モデル price = a + b * number_of_reviews
model = sm.OLS(price, sm.add_constant(number_of_reviews))
results = model.fit() # 推定
print(results.summary()) # 結果
print('p-values\n', results.pvalues) # p値

# 重回帰分析
## まずは相関係数をheatmap
import seaborn as sns
plt.figure(figsize = (12,9)) # 図の大きさ
# 相関係数を計算する変数をequation_dfに格納
equation_df = pd.concat([manhattan_dummy, private_dummy, home_dummy, shared_dummy, price, minimum_nights, number_of_reviews, reviews_per_month, calculated_host_listings_count, availability_365], axis = 1)
# seabornでheatmapを作成
sns.heatmap(equation_df.pct_change().corr(), annot=True, cmap = 'Blues')
plt.show() # 図を表示
## つぎに重回帰分析
## 線形回帰分析に必要なライブラリを読み込む
from sklearn import linear_model, datasets
from sklearn.linear_model import LinearRegression

# equation_dfの中からpriceを取り出してpriceに代入
price = pd.DataFrame(equation_df.price)
# 被説明変数であるpriceをequation_dfからdropしてx_listに代入
x_list = equation_df.drop("price",1)
# number_of_reviewsとreviews_per_monthの相関係数が高い(0.92)のでreviews_per_monthを落とす。
x_list = x_list.drop("reviews_per_month",1)
# Manhattan_Dummryとの相関係数が高い?のでshared_dummy(0.24)とhome_dummy(0.2)も除去する。
x_list = x_list.drop("shared_dummy",1)
x_list = x_list.drop("home_dummy",1)
# 異常値や欠損茅野除去
x_list = x_list.drop(x_list.columns[np.isnan(x_list).any()], axis = 1)

# 重回帰モデルを構築
model = sm.OLS(price, sm.add_constant(x_list))
# 推定
result = model.fit()
# 結果を表示
print(result.summary())
print(result.pvalues)

# 多重共線性の確認のためVIFを導出
from statsmodels.stats.outliers_influence import *
num_cols = model.exog.shape[1]
print(num_cols) # 説明変数の個数
vifs = [variance_inflation_factor(model.exog, i) for i in range(0, num_cols)]
pdv = pd.DataFrame(vifs, index = model.exog_names, columns = ["VIF"])
print(pdv) # 表示


# 被説明変数と説明変数を結合
x_list3 = pd.concat([price, x_list], axis = 1) 
# pairplotを作成
sns.pairplot(x_list3, hue = "Manhattan_dummry") 
plt.show() # 図を表示

# 位置情報を使った分析
import geocoder
location = '自由の女神像'
adress = geocoder.osm(location, timeout = 5.0)
adress.latlng # 緯度と経度

# 緯度経度情報を使った分析
## geodesicを読み込む
from geopy.distance import geodesic

# 空のオブジェクトdistanceを作成
distance = []

for x,y in zip(input_sheet_df.latitude, input_sheet_df.longitude):
    location = np.array([x, y])
    distance.append(geodesic(address.latlng, location).km)

input_sheet_df['distance'] = distance
input_sheet_df.distance.head()
