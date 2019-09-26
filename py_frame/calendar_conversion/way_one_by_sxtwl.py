# -*- coding: utf-8 -*-
# writer        Yang
# create_time   2019/9/19 17:42
# file_name     way_one.py
"""
	公历农历互相转换，获取节日，节气等信息
	方法一： 使用sxtwl组件实现，但是需要gcc版本是4.8.x以上，安装完成之后，可直接输出
"""
import sxtwl
from datetime import date
import datetime

ymc = [u"十一月", u"腊月", u"正月", u"二月", u"三月", u"四月", u"五月", u"六月", u"七月", u"八月", u"九月", u"十月"]
rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十",
       u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九", u"二十",
       u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]
NONG_FESTIVAL = [  # 农历节日表
    ("正月初一", "春节"),
    ("正月十五", "元宵节"),
    ("五月初五", "端午节"),
    ("七月初七", "七夕节"),
    ("八月十四", "中秋节"),
    ("八月十五", "中秋节"),
    ("九月初九", "重阳节"),
    ("腊月初八", "腊八节"),
    ("腊月廿九", "除夕"),
    ("腊月三十", "除夕"),
]
GONG_FESTIVAL = [  # 公历节日表
    ("0101", "元旦"),
    ("0214", "情人节"),
    ("0308", "妇女节"),
    ("0312", "植树节"),
    ("0404", "清明节"),
    ("0405", "清明节"),
    ("0406", "清明节"),
    ("0501", "劳动节"),
    ("0601", "儿童节"),
    # ("0701","建党节"),
    # ("0801","建军节"),
    ("0910", "教师节"),
    ("1001", "国庆节"),
]

CALENDARICITY = [  # 节气表
    (["0203", "0204", "0205"], "立春"),
    (["0218", "0219""0220"], "雨水"),
    (["0304", "0305", "0306"], "惊蛰"),
    (["0319", "0320", "0321"], "春分"),
    (["0419", "0420""0421"], "谷雨"),
    (["0504", "0505", "0506"], "立夏"),
    (["0520", "0521", "0522"], "小满"),
    (["0604", "0605", "0606"], "芒种"),
    (["0620", "0621", "0622"], "夏至"),
    (["0706", "0707", "0708"], "小暑"),
    (["0721", "0722", "0723"], "大暑"),
    (["0806", "0807", "0808"], "立秋"),
    (["0822", "0823", "0824"], "处暑"),
    (["0906", "0907", "0908"], "白露"),
    (["0922", "0923", "0924"], "秋分"),
    (["1007", "1008", "1009"], "寒露"),
    (["1022", "1023", "1024"], "霜降"),
    (["1106", "1107", "1108"], "立冬"),
    (["1121", "1122", "1123"], "小雪"),
    (["1206", "1207", "1208"], "大雪"),
    (["1221", "1222", "1223"], "冬至"),
    (["0104", "0105", "0106"], "小寒"),
    (["0119", "0120", "0121"], "大寒"),
]


def get_lunar_calendar(time):
    """
    :return: 几月几日（农历，字符串）
    """
    lunar = sxtwl.Lunar()
    today = str(time)  # 如 2019-08-08
    today_list = today.split('-')  # ['2019', '08', '08']
    lunar_day = lunar.getDayBySolar((int)(today_list[0]), (int)(today_list[1]), (int)(today_list[2]))  # 输入年月日
    if lunar_day.Lleap:  # 判断是否为润年
        return (ymc[lunar_day.Lmc] + rmc[lunar_day.Ldi]).encode("utf-8")
    else:
        return (ymc[lunar_day.Lmc] + rmc[lunar_day.Ldi]).encode("utf-8")


def get_gregorian_calendar(time):
    data = str(time).split("-")
    return data[1] + data[2]


# 获取节日
def get_festival(time):
    # 获取农历
    n_date = get_lunar_calendar(time)
    # 获取公历
    g_date = get_gregorian_calendar(time)

    # 获取节日
    for d, f in GONG_FESTIVAL:
        if g_date == d:
            return f
    for d, f in NONG_FESTIVAL:
        if n_date == d:
            return f


# 获取节气：
def get_calendaricity(time):
    g_date = get_gregorian_calendar(time)
    for d, c in CALENDARICITY:
        if g_date in d:
            return c


# 获取三个月内的节日加节气
def get_fes_cal():
    res_list = []
    for i in range(90):
        time = (datetime.datetime.now() + datetime.timedelta(i)).strftime("%Y-%m-%d")
        fes = get_festival(time)
        cal = get_calendaricity(time)
        if cal:
            if cal not in res_list:
                res_list.append(cal)
        if fes:
            if fes not in res_list:
                res_list.append(fes)
    return ",".join(res_list)


print('将来三个月内将发生的节日和节气为："%s"' % (get_fes_cal()))  # 直接输出
