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
