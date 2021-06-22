# PythonでMarkdown

## パッケージの読み込み

```python
import pandas as pd # 計算ライブラリ
import os # 作業ディレクトリの指定
os.chdir("/Users/soichi/Dropbox/Programing/")
``` 

## データの読み込み

```python
input_book = pd.ExcelFile('FIFA19_data.xlsx')
```


```python
input_sheet_name = input_book.sheet_names
num_sheet = len(input_sheet_name)
print(input_sheet_name)
print("Sheet の数:", num_sheet)
input_sheet_df = input_book.parse(input_sheet_name[0])
```


GK のデータのみを外す。
この箇所をコメントアウトすると、ゴールキーパーを含んだ形での分析になります。
```python
input_sheet_df = input_sheet_df[input_sheet_df['Position'] != "GK"]
```


#最初の10行のみを表示する
input_sheet_df.head(10)


import numpy as np

#データを読み込む
age=input_sheet_df.Age #年齢
overall=input_sheet_df.Overall #総合能力
wage=input_sheet_df.Wage2 #給与
preferredfoot=input_sheet_df.preferredfoot #利き足
reputation=input_sheet_df.reputation #レピュテーション
least_contract=input_sheet_df.least_contract #残りの契約年数
height=input_sheet_df.height2 #身長
weight=input_sheet_df.weight2 #体重
crossing=input_sheet_df.Crossing #クロス精度
finishing=input_sheet_df.Finishing #フィニッシュ精度
heading=input_sheet_df.HeadingAccuracy #ヘディング精度
shortPassing=input_sheet_df.ShortPassing #ショートパス精度
dribbling=input_sheet_df.Dribbling #ドリブルの精度
Curve=input_sheet_df.Curve #カーブの精度
FKAccuracy=input_sheet_df.FKAccuracy #FK の精度
LongPassing=input_sheet_df.LongPassing #ロングパスの精度
BallControl=input_sheet_df.BallControl #ボールコントロール
Acceleration=input_sheet_df.Acceleration #飛び出し
SprintSpeed=input_sheet_df.SprintSpeed #スプリントスピード
Agility=input_sheet_df.Agility #アジリティ
Reactions=input_sheet_df.Reactions #リアクション
Balance=input_sheet_df.Balance #バランス
ShotPower=input_sheet_df.ShotPower #シュートパワー
stamina=input_sheet_df.Stamina #スタミナ
Jumping=input_sheet_df.Jumping #ジャンプ
Strength=input_sheet_df.Strength #ストレングス
LongShots=input_sheet_df.LongShots #ロングスート
Aggression=input_sheet_df.Aggression #アグレッション
Interceptions=input_sheet_df.Interceptions #インターセプト
Positioning=input_sheet_df.Positioning #ポジショニング
Vision=input_sheet_df.Vision #ビジョン
Penalties=input_sheet_df.Penalties #ペナルティキック
Composure=input_sheet_df.Composure #コンポジュア
Marking=input_sheet_df.Marking #マーキング
StandingTackle=input_sheet_df.StandingTackle #スタンディングタックル
SlidingTackle=input_sheet_df.SlidingTackle #スライディングタックル

#利用するパラメータを指定する
#overall はここから除外しています。結果が変わるので、入れたバージョンも実施してみてください
equation_df2=pd.concat([wage, age, preferredfoot, reputation, least_contract, height, weight, \
crossing, finishing, heading, shortPassing, dribbling, Curve, FKAccuracy, \
LongPassing, BallControl, Acceleration, SprintSpeed, Agility, Reactions, \
Balance, ShotPower, stamina, Jumping, Strength, LongShots, Aggression, \
Interceptions, Positioning, Vision, Penalties, Composure, Marking, \
StandingTackle, SlidingTackle], axis=1)

#被説明変数として利用するものを取り出す
wage2 = pd.DataFrame(equation_df2.Wage2)
#被説明変数を抜き取る
x_list2 = equation_df2.drop("Wage2",1)

#異常値やnull になっている値を除去する
x_list2 = x_list2.drop(x_list2.columns[np.isnan(x_list2).any()], axis=1)


from sklearn import preprocessing, linear_model 
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt

#データの整形を行う
#データの標準化を行う
sc=preprocessing.StandardScaler()
sc.fit(x_list2)

X=sc.transform(x_list2)

sc2=preprocessing.StandardScaler()
sc2.fit(wage2)

Y=sc2.transform(wage2)

#相関係数を確認する
plt.figure(figsize=(30, 24))
sns.heatmap(x_list2.pct_change().corr(), annot=True, cmap='Blues')


from sklearn import model_selection

#学習データとテストデータに分割する
#分割する割合は2:8 で作業する

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, wage2, test_size=0.2, random_state=0)

from sklearn.tree import DecisionTreeClassifier

#決定木分析を, X_train 値と Y_train 値に基づき行う
model3 = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
model3.fit(X_train, Y_train)

print('正解率 (train):{:.3f}'.format(model3.score(X_train, Y_train)))
print('正解率 (test):{:.3f}'.format(model3.score(X_test, Y_test)))


from graphviz import Digraph
from sklearn import tree
import pydotplus
from six import StringIO
from sklearn.externals.six import StringIO
from IPython.display import Image

dot_data=StringIO()
tree.export_graphviz(model3, out_file=dot_data)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

graph.progs = {'dot': u"C:\\Users\\yhara\\Anaconda3\\Library\\bin\\graphviz\\dot.exe"}

Image(graph.create_png())