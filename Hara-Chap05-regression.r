library(tidyverse) 
library(broom) # 分析結果を見やすくする
library(car) # vifの計算のため

# options(scipen=10) #指数表記を回避

# データを読み込む
setwd("/Users/soichi/Dropbox/Programing/Hara-Python/Hara-Python-1")
input_data <- readr::read_csv("carprice.csv")
# 先頭10行を確認
head(input_data,10)

# 関数lm()で線形回帰モデルをOLS推定する
model01 <- price ~ enginesize # 単回帰モデル
res01 <- lm(model01, data =input_data) # 最小二乗法
# 結果を表示
summary(res01)
tidy(res01)
tidy(res01)$p.value

# 重回帰
x_list <- input_data %>% dplyr::select(price, enginesize, wheelbase, horsepower, carheight)
res02 <- lm(price ~. , data = x_list)
tidy(res02)


# ダミー変数
## Rはファクター方の変数を自動でダミーにしてくれる
input_data$doornumber <- as.factor(input_data$doornumber)
x_list2 <- input_data %>% dplyr::select(price, enginesize, wheelbase, horsepower, carheight,doornumber)
res2 <- lm(price ~., data = x_list2)
tidy(res2)

# VIF
vif(res2) # vifを表示

# おまけ
## tidy形式で複数のモデルを効率的に管理して，あとで結果を活用しやすくする。
models <- c(
  price ~ enginesize,
  price ~ enginesize + wheelbase + horsepower + carheight,
  price ~ enginesize + wheelbase + horsepower + carheight + doornumber
) %>% 
  enframe("model_no", "models")

df_res <- models %>% 
  mutate(model = map(models, lm, data=input_data),
         tidied = map(model, tidy),
         glanced = map(model, glance)
         )

df_coef <- df_res %>% 
  select(model_no, tidied) %>% 
  unnest(cols=c(tidied)) %>% 
  mutate_if(is.double, round, digits=2)

df_coef %>% 
  mutate(term = fct_inorder(term)) %>% 
  select(model_no, term, estimate) %>% 
  spread(model_no,estimate)
