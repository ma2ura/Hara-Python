import pandas as pd # 行列計算
import numpy as np # 数値計算

# 都道府県をlistに格納
 list = ["hokkaido", "aomori", "iwate", "miyagi", "akita", "yamagata", "fukushima", "ibaraki", "tochigi", "gunma",
        "saitama", "chiba", "tokyo", "kanagawa", "niigata", "toyama", "ishikawa", "fukui", "yamanashi","nagano", "gifu", 
        "shizuoka", "aichi", "mie", "shiga", "kyoto", "osaka", "hyogo", "nara", "wakayama", 
        "tottori", "shimane", "okayama", "hiroshima", "yamaguchi", "tokushima", "kagawa", "ehime", "kochi", 
        "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima", "okinawa"]
# listの中身を表示
print(list)

# データを取得するurlアドレスをurl1に代入
url1 = 'http://koko-pachi.com/htm/korona.'

# listの中で繰り返し処理
for j in range(len(list)): # 都道府県ごとに
    data3 = pd.DataFrame() # 空データベースdata3を作成
    print(list[j]) # 都道府県を1つずつ表示
    url2 = list[j] + ".5.htm" # urlを作成
    url3 = url1 + url2 # urlを完成させる
    #print(url3)
    dfs = pd.read_html(url3)# url3の中身のhtmlをdfsに代入
    data3 = data3.append(dfs) # データを下に追加しながらdata3に代入

# data3の中身を表示
print(data3)

# データ整理用
# 管理ラベルを付与
#data3.columns = {'A','B','C','D','E','F','G','H'}
data3.columns = {'A','B','C','D','E','F'}

# data3 = data3.dropna(how = 'all', axis = 1)
# data3 = data3.dropna(how = 'any')
data3 = data3.drop('D', axis = 1)
data3 = data3.drop('E', axis = 1)
data3 = data3.drop('F', axis = 1)
data3 = data3.drop('G', axis = 1)
data3 = data3.drop('H', axis = 1)
data3 = data3.drop('B', axis = 1)
data3 = data3.drop('A', axis = 1)
data3 = data3.dropna(how = 'any')

# データの整理，余計な箇所を削除
temp1 = data3.loc[[0]]
temp1.reset_index(drop = True, inplace = True)
temp1.drop(temp1.tail(1).index, inplace = True)
temp1.drop(temp1.head(1).index, inplace = True)
temp1.reset_index(drop = True, inplace = True)

#データの整理 indexを並べ直して，データを取り出す。
temp2 = data3.loc[[1]]
temp2.reset_index(drop = True, inplace = True)
temp3 = data3.loc[[2]]
temp3.reset_index(drop = True, inplace = True)

data5 = pd.concat([temp1,temp2,temp3], axis = 1)

label = "pachinko_" + list[j] + "_20200609.csv"
data5.to_csv(label)
