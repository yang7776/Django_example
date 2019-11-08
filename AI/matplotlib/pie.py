# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/11/8 12:08
# file_name     pie.py

import os
from matplotlib import pyplot as plt
import matplotlib
# pyplot并不默认支持中文显示，需要rcParams修改字体实现。'Microsoft YaHei'：微软雅黑字体风格
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'

""" 饼形图 """
"""
pie(x,labels=,autopct=,colors)
x：数量，自动计算百分比
labels：每部分名称
autopct：占比显示指定%1.2f%%   （%0.1%% 保留一位小数）
colors：每部分颜色，不指定会有默认值
"""

# 电影排片场次占比饼形图
def example_one():
    plt.figure(figsize=(20, 8), dpi=100)

    # 准备每部电影的名字，电影的排片场次
    movie_name = ['雷神3：诸神黄昏', '正义联盟', '东方快车谋杀案', '寻梦环游记', '全球风暴', '降魔传', '追捕', '七十七天', '密战', '狂兽', '其它']

    place_count = [60605, 54546, 45819, 28243, 13270, 9945, 7679, 6799, 6101, 4621, 20105]

    # 饼形图需要“pie”关键字表示。
    # 参数：pie(x,labels=,autopct=,colors)
    # 一般情况下autopct="%1.2f%%"，其中“2”表示小数点后保留几位小数，一般为两位小数。
    plt.pie(place_count, labels=movie_name, autopct="%1.2f%%", colors=['b', 'r', 'g', 'y', 'c', 'm', 'y', 'b', 'c', 'g', 'g'])

    # 设置x轴和y轴的长度相等，即“equal”为均等
    plt.axis('equal')
    # 显示图例
    plt.legend(loc='best')
    plt.savefig(os.path.join(os.getcwd(), "pie_01.png"))
    plt.show()


# 饼形图特殊效果设置
def example_two():
    plt.figure(figsize=(20, 8), dpi=100)
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]

    # 和labels中的一一对应，值越大偏移距离越远
    explodes = (0, 0.1, 0, 0.2)

    """
	explode：数组，可选参数，默认为None。
	如果不是None，是一个长度与x相同长度的数组，用来指定每部分的偏移量。
	例如：explode=[0,0,0.2,0,0]，第二个饼块被拖出。
	"""
    # 设置阴影，爆裂效果,其中explode设置爆炸效果，shadow设置阴影效果，startangle设置逆时针旋转90度
    plt.pie(sizes, explode=explodes, labels=labels, autopct='%1.2f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.legend(loc='best')
    plt.savefig(os.path.join(os.getcwd(), "pie_02.png"))
    plt.show()


if __name__ == "__main__":
    # example_one()
    example_two()
