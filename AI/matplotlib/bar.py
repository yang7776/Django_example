# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/11/8 11:14
# file_name     bar.py

import os
from matplotlib import pyplot as plt
import matplotlib
# pyplot并不默认支持中文显示，需要rcParams修改字体实现。'Microsoft YaHei'：微软雅黑字体风格
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
""" 柱状图 """
"""
bar(x，height， width，*，align=‘center’，**kwargs)
主要参数：
	x：包含所有柱子的下标的列表
	height：包含所有柱子的高度值的列表
	width：每个柱子的宽度。可以指定一个固定值，那么所有的柱子都是一样的宽。或者设置一个列表，这样可以分别对每个柱子设定不同的宽度。
	align：柱子对齐方式，有两个可选值：center和edge。center表示每根柱子是根据下标来对齐, edge则表示每根柱子全部以下标为起点，然后显示到下标的右边。如果不指定该参数，默认值是center。

其他可选参数：
	color：每根柱子呈现的颜色。同样可指定一个颜色值，让所有柱子呈现同样颜色；或者指定带有不同颜色的列表，让不同柱子显示不同颜色。
	edgecolor：每根柱子边框的颜色。同样可指定一个颜色值，让所有柱子边框呈现同样颜色；或者指定带有不同颜色的列表，让不同柱子的边框显示不同颜色。
	linewidth：每根柱子的边框宽度。如果没有设置该参数，将使用默认宽度，默认是没有边框。
	tick_label：每根柱子上显示的标签，默认是没有内容。
	xerr：每根柱子顶部在横轴方向的线段。如果指定一个固定值，所有柱子的线段将一直长；如果指定一个带有不同长度值的列表，那么柱子顶部的线段将呈现不同长度。
	yerr：每根柱子顶端在纵轴方向的线段。如果指定一个固定值，所有柱子的线段将一直长；如果指定一个带有不同长度值的列表，那么柱子顶部的线段将呈现不同长度。
	ecolor：设置 xerr 和 yerr 的线段的颜色。同样可以指定一个固定值或者一个列表。
	capsize：这个参数很有趣, 对xerr或者yerr的补充说明。一般为其设置一个整数，例如 10。如果你已经设置了
	yerr 参数，那么设置 capsize 参数，会在每跟柱子顶部线段上面的首尾部分增加两条垂直原来线段的线段。对 xerr 参数也是同样道理。可能看说明会觉得绕，如果你看下图就一目了然了。
	error_kw：设置 xerr 和 yerr 参数显示线段的参数，它是个字典类型。如果你在该参数中又重新定义了 ecolor 和 capsize，那么显示效果以这个为准。
	log：这个参数，我暂时搞不懂有什么用。
	orientation：设置柱子是显示方式。设置值为 vertical ，那么显示为柱形图。如果设置为 horizontal 条形图。不过 matplotlib 官网不建议直接使用这个来绘制条形图，使用barh来绘制条形图。
"""
plt.figure(figsize=(20, 8), dpi=100)

movie_name = ['雷神3：诸神黄昏', '正义联盟', '寻梦环游记']

x = range(len(movie_name))
# 若只需要一种y轴柱状图，只写一种即可
y1 = [73853, 57767, 22354]
y2 = [8725, 8716, 8318]

# 利用for循环，设置x的柱形位置（移动到两个柱状图相连位置)
# 注意柱状图用“bar”关键字表示
plt.bar([i + 0.2 for i in x], y1, width=0.2)
plt.bar([i + 0.4 for i in x], y2, width=0.2, color='r')

# 文字代替，设置x文字的位置（移动到中心位置)
plt.xticks([i + 0.3 for i in x], movie_name)

plt.savefig(os.path.join(os.getcwd(), "bar_01.png"))

plt.show()
