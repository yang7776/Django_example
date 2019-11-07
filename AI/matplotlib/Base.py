# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/11/7 15:46
# file_name     Base.py

import matplotlib.pyplot as plt

"""
注意：
	建议使用Anaconda软件中的python环境，以及安装“jupyter”来显示
	pyplot并不默认支持中文显示，需要rcParams修改字体实现。

什么是matplotlib？
	是专门用于开发2D图表（包括3D图表）
	使用起来及其简单
	以渐进，交互式方式实现数据可视化

matplotlib框架介绍：“栈”
	后端：实现绘图区域（分配画图的资源）
	美工：figure（画布），axes（坐标系），axis（坐标轴）
	脚本：pyplot

绘图的基本三步：
	绘制画布，  plt.figure()
	准备数据，  plt.plot/bar/hist/pie()    折线图/柱状图/直方图/饼形图
	展示数据，  plt.show()
	
数据挖掘：去使用统计学，机器学习或深度学习的算法挖掘历史数据的价值
机器学习：有自己的领域或者分析问题方式，更多是从历史数据总结经验去预测（图像识别等等）
其实数据挖掘或机器学习应用的领域可以很多，比如金融，教育，医疗，城市，电商等等领域。
"""