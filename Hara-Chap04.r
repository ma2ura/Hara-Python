library(tidyverse)
library(ggExtra)

# カレントディレクトリの設定
# setwd("/Users/soichi/Dropbox/Programing")

# csvデータの読み込み
input_data <- read.csv("carprice.csv")

# データの先頭10行を確認する
head(input_data,10)
# データの構造を確認する
str(input_data)
# データの概要を確認する
summary(input_data)

# データの各種統計量をみる。
mean(input_data$price)
median(input_data$price)
var(input_data$price)
sd(input_data$price)
max(input_data$price)
min(input_data$price)

# dplyrをつかってグループ別統計量を見る。
summary_price <- input_data %>% 
  dplyr::group_by(doornumber) %>%
  dplyr::summarise(
    mean_price = mean(price),
    median_price = median(price),
    var_price = var(price),
    sd_price = sd(price),
    max_price = max(price),
    min_price = min(price)
  )
print(summary_price)


# ggplotでヒストグラム
g <- ggplot(input_data, aes(x=price)) + geom_histogram(boundary = 0, binwidth=5000) 
g <- g +  scale_x_continuous(breaks=seq(5000, 50000, by=5000)) 
g <- g + theme_bw() + xlab("price") + ylab("count") 
print(g)

# 箱ひげ図
## 基本関数
boxplot(input_data$price)
## ggplot
ggplot(input_data, aes(y = price)) + geom_boxplot()

# 散布図
## 基本関数
plot(input_data$enginesize, input_data$price)
## ggplot
g <- ggplot(input_data,aes(x=enginesize,y=price)) + geom_point(alpha = 0.3)
g <- g + ggtitle("Engine and Price") + xlab("Engine") + ylab("Price")
print(g)

# 共分散
cov(input_data$price,input_data$enginesize)
# 相関係数
cor(input_data$price,input_data$enginesize)
# 相関係数行列
dat <- input_data %>% 
  dplyr::select(price,enginesize) #priceとenginesizeを取り出す
cov(dat)
cor(dat)

# 散布図とヒストグラム
g <- ggplot(input_data, aes(x = enginesize, y = price)) + geom_point()
ggMarginal(g, type = "histogram", bins = 20,margins = "both", size = 5)

# 複数変数間の情報量が多い図
dat2 <- input_data %>% 
  dplyr::select(price, enginesize, wheelbase, horsepower, carheight)
# install.packages("psych")
library(psych)
psych::pairs.panels(dat2,hist.col="white", lm=T, rug = F, ellipses=F)

# 相関係数を色で表す
# install.packages("ggcorrplot")
library(ggcorrplot)
res <- cor(dat2)
g <- ggcorrplot(corr = res, hc.order = TRUE, method = "square", lab = TRUE)
print(g)
# macだとggsaveは使えないので，工夫が必要。
ggsave(file = "cor_heat.png", plot = g)

# おしまい