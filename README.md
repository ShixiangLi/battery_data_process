# 电池试验数据预处理

界面预览

![](E:\github\data_process\battery_data_process\figs\1.jpg)

## 概述

对原始电池数据进行格式化特征参数、计算放电容量、绘制试验剖面等

## 使用说明

### 试验数据.dat转.csv

1. 下拉选项框选择"单体电池.dat转.csv"


2. 读取路径选择.dat数据文件所在文件夹（可以包含多个日期的数据文件）


3. 保存路径选取需要保存的文件位置


4. 点击submit即可在对应保存位置生成格式化的单体电池特征参数文件

![](E:\github\data_process\battery_data_process\figs\2.jpg)

### 电池组.xls转.csv

1. 首先要得到电池组放电信息.xls文件，来源为新威电池系统测量得到的.nda文件（在电池数据中找到）![](E:\github\data_process\battery_data_process\figs\3.jpg)
2. 用新威软件打开.nda文件，在<font color='red'>**英文状态**</font>下导出.xls文件，并以<font color='red'>**XXXX（年）-XX（月）-XX（日）-X（电池组编号）**</font>的格式命名备用![](E:\github\data_process\battery_data_process\figs\4.jpg)
3. 选择电池组.xls转.csv，并选择相应的读取（电池组放电信息.xls）和保存路径点击submit，即可生成电池组放电信息.csv文件![](E:\github\data_process\battery_data_process\figs\5.jpg)

### 电池组放电容量和放电时间提取

1. 选择电池组放电容量及时间计算，选择相应的读取（电池组放电信息.csv）和保存路径，主要是为单体电池容量计算提供截取依据![](E:\github\data_process\battery_data_process\figs\6.jpg)


### 单体电池放电容量计算

1. 选择单体电池放电容量计算，选择相应的读取路径（单体电池.csv文件），电池组放电信息文件（上一步得到的），和保存路径。点击submit即可得到单体电池容量退化数据![](E:\github\data_process\battery_data_process\figs\7.jpg)

### 剖面绘制

1. 选择单体电池放电剖面绘制
2. 读取路径要选择存放原始电池组.xls文件的文件夹（第二步的原始数据）
3. 单体电池绘制路径根据需要选择单体电池.csv文件目录下的某一天的数据
4. 点击submit即可得到当天的循环退化剖面，图像控件可直接保存图片![](E:\github\data_process\battery_data_process\figs\8.jpg)



