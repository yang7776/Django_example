# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/11/7 15:58
# file_name     plot.py

import os
import random
from matplotlib import pyplot as plt
import matplotlib
# pyplot并不默认支持中文显示，需要rcParams修改字体实现。'Microsoft YaHei'：微软雅黑字体风格
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'

""" 折线图 """

# 绘制温度变化图
def example_one():
    # 设置画布：figsize:指定figure的宽和高，单位为英寸；dpi参数指定绘图对象的分辨率，即每英寸多少个像素，缺省值为80
    plt.figure(figsize=(12, 5), dpi=100)

    # 设置x，y轴的范围刻度
    x_ticks = range(60)
    y_ticks = range(40)

    # 设置两个城市的y轴，random.uniform(x, y) 在x,y之间随机生成一个实数
    y_beijing = [random.uniform(15, 18) for i in x_ticks]
    y_shenzhen = [random.uniform(5, 8) for i in x_ticks]

    # 设置两个城市的坐标轴数据，并设置参数（color为颜色(第一个英文字母小写)，linestyle为线类型(网上有线类型对应写法)，label为线的标签名）
    plt.plot(x_ticks, y_beijing, color='r', linestyle='-.', label='北京', linewidth=2)
    plt.plot(x_ticks, y_shenzhen, color='k', linestyle='-', label='深圳')

    # 设置刻度，[::5]坐标轴刻度之间以5为间隔，即步长，其中xticks内部的参数定义：xticks(x,**kwages)
    plt.xticks(x_ticks[::5], ['7点{}分'.format(i) for i in x_ticks][::5])
    plt.yticks(y_ticks[::5])

    # 设置表格标题和坐标轴的标签
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.title('温度变化表格')

    # 城市信息备注显示，即把上面线的label的信息展现出来，不设置则不展示。loc：显示的位置（网上有对应位置参数）
    plt.legend(loc="best")

    # 存储图片到指定路径，如果不指定，默认存到“ C:\Users\admin ”中。
    plt.savefig(os.path.join(os.getcwd(), "plot_01.png"))

    # 展示画布
    plt.show()


"""
# 两个城市的温度，在多个坐标系中显示
# 当在多个ax里面画图的时候，刻度，标签，必须在相应的坐标系里面指定
# 当画布中需要多个坐标系时，用axes[num]设置各个坐标系的编号。之前使用的plt，都可用axes[num]代替，直接用对应的坐标系编号并设置各个方法
"""
def example_two():
        # 其中参数1和2分别代表子图的行数和列数，一共有 1x3 个子图像。函数返回一个figure图像和子图ax的array列表，一行里显示两列。
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8), dpi=100)
    x = range(60)
    y = range(40)

    # 设置坐标拉到原点
    plt.xlim(0, 60)

    y_shanghai = [random.uniform(15, 18) for i in x]
    y_beijing = [random.uniform(1, 3) for i in x]

    axes[0].plot(x, y_shanghai, label="上海")
    axes[1].plot(x, y_beijing, color='r', linestyle='--', label="北京")

    # set_xticks里面有两个参数，一个是步长，一个是布尔类型，故不能在此方法中指定文字代替
    axes[0].set_xticks(x[::5])
    # 在set_xticks设置刻度步长的基础上，用set_xticklabels设置文字代替刻度值
    axes[0].set_xticklabels(["7点{}分".format(i) for i in x][::5])
    axes[0].set_yticks(y[::5])

    axes[1].set_xticks(x[::5])
    axes[1].set_xticklabels(["7点{}分".format(i) for i in x][::5])
    axes[1].set_yticks(y[::5])

    axes[0].set_xlabel("时间")
    axes[0].set_ylabel("温度")
    axes[0].set_title("一些城市的温度变化曲线图1")
    axes[1].set_xlabel("时间")
    axes[1].set_ylabel("温度")
    axes[1].set_title("一些城市的温度变化曲线图2")

    axes[0].legend(loc="best")
    axes[1].legend(loc="best")

    plt.savefig(os.path.join(os.getcwd(), "plot_02.png"))

    plt.show()


if __name__ == "__main__":
    # 绘制两个城市的温度变化图在一个坐标系里（画布中只有一个坐标系）
    example_one()
    # 两个城市的温度，在多个坐标系中显示（画布中显示多个坐标系）
    example_two()
