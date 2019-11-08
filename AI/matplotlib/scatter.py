# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/11/8 14:10
# file_name     scatter.py

import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
# pyplot并不默认支持中文显示，需要rcParams修改字体实现。'Microsoft YaHei'：微软雅黑字体风格
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'

""" 散点图 """

# 用散点图实例
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8), dpi=100)

# numpy.random.randn(d0, d1, …, dn)是从标准正态分布中返回一个或多个样本值。
# numpy.random.rand(d0, d1, …, dn)的随机样本位于[0, 1)之间。
x = np.random.randn(1000)
y1 = np.random.randn(len(x))
y2 = 1.2 + np.exp(x)  # np.exp(x)：求x的幂次方

# x,y数组数据；color线条颜色；alpha透明度；edgecolors轮廓颜色；更多参数，参考：https://blog.csdn.net/xiaobaicai4552/article/details/79065990 或 官网
axes[0].scatter(x, y1, color='indigo', alpha=0.9, edgecolors='white', label='no correl')
axes[1].scatter(x, y2, color='green', alpha=0.3, edgecolors='grey', label='correl')

axes[0].set_xlabel("no correlation")
axes[1].set_xlabel("strong correlation")

# 设置网格，配置默认
axes[0].grid(True)
axes[1].grid(True)

axes[0].legend(loc="best")
axes[1].legend(loc="best")

plt.savefig(os.path.join(os.getcwd(), "scatter_01.png"))
plt.show()
