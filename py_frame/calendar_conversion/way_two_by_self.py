# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/9/19 17:44
# file_name     way_two_by_self.py
"""
	公历农历互相转换，获取节日，节气等信息
	方法一： 自己实现的公历和农历互转，以及获取相关数据
"""
import datetime

MONTH_NAME = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
			  "November", "December"]
MONTH_DAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

LUNAR_CALENDAR_TABLE = [
	0x04AE53, 0x0A5748, 0x5526BD, 0x0D2650, 0x0D9544, 0x46AAB9, 0x056A4D, 0x09AD42, 0x24AEB6, 0x04AE4A,
	# //*1901-1910*/
	0x6A4DBE, 0x0A4D52, 0x0D2546, 0x5D52BA, 0x0B544E, 0x0D6A43, 0x296D37, 0x095B4B, 0x749BC1, 0x049754,
	# //*1911-1920*/
	0x0A4B48, 0x5B25BC, 0x06A550, 0x06D445, 0x4ADAB8, 0x02B64D, 0x095742, 0x2497B7, 0x04974A, 0x664B3E,
	# //*1921-1930*/
	0x0D4A51, 0x0EA546, 0x56D4BA, 0x05AD4E, 0x02B644, 0x393738, 0x092E4B, 0x7C96BF, 0x0C9553, 0x0D4A48,
	# //*1931-1940*/
	0x6DA53B, 0x0B554F, 0x056A45, 0x4AADB9, 0x025D4D, 0x092D42, 0x2C95B6, 0x0A954A, 0x7B4ABD, 0x06CA51,
	# //*1941-1950*/
	0x0B5546, 0x555ABB, 0x04DA4E, 0x0A5B43, 0x352BB8, 0x052B4C, 0x8A953F, 0x0E9552, 0x06AA48, 0x6AD53C,
	# //*1951-1960*/
	0x0AB54F, 0x04B645, 0x4A5739, 0x0A574D, 0x052642, 0x3E9335, 0x0D9549, 0x75AABE, 0x056A51, 0x096D46,
	# //*1961-1970*/
	0x54AEBB, 0x04AD4F, 0x0A4D43, 0x4D26B7, 0x0D254B, 0x8D52BF, 0x0B5452, 0x0B6A47, 0x696D3C, 0x095B50,
	# //*1971-1980*/
	0x049B45, 0x4A4BB9, 0x0A4B4D, 0xAB25C2, 0x06A554, 0x06D449, 0x6ADA3D, 0x0AB651, 0x093746, 0x5497BB,
	# //*1981-1990*/
	0x04974F, 0x064B44, 0x36A537, 0x0EA54A, 0x86B2BF, 0x05AC53, 0x0AB647, 0x5936BC, 0x092E50, 0x0C9645,
	# //*1991-2000*/
	0x4D4AB8, 0x0D4A4C, 0x0DA541, 0x25AAB6, 0x056A49, 0x7AADBD, 0x025D52, 0x092D47, 0x5C95BA, 0x0A954E,
	# //*2001-2010*/
	0x0B4A43, 0x4B5537, 0x0AD54A, 0x955ABF, 0x04BA53, 0x0A5B48, 0x652BBC, 0x052B50, 0x0A9345, 0x474AB9,
	# //*2011-2020*/
	0x06AA4C, 0x0AD541, 0x24DAB6, 0x04B64A, 0x69573D, 0x0A4E51, 0x0D2646, 0x5E933A, 0x0D534D, 0x05AA43,
	# //*2021-2030*/
	0x36B537, 0x096D4B, 0xB4AEBF, 0x04AD53, 0x0A4D48, 0x6D25BC, 0x0D254F, 0x0D5244, 0x5DAA38, 0x0B5A4C,
	# //*2031-2040*/
	0x056D41, 0x24ADB6, 0x049B4A, 0x7A4BBE, 0x0A4B51, 0x0AA546, 0x5B52BA, 0x06D24E, 0x0ADA42, 0x355B37,
	# //*2041-2050*/
	0x09374B, 0x8497C1, 0x049753, 0x064B48, 0x66A53C, 0x0EA54F, 0x06B244, 0x4AB638, 0x0AAE4C, 0x092E42,
	# //*2051-2060*/
	0x3C9735, 0x0C9649, 0x7D4ABD, 0x0D4A51, 0x0DA545, 0x55AABA, 0x056A4E, 0x0A6D43, 0x452EB7, 0x052D4B,
	# //*2061-2070*/
	0x8A95BF, 0x0A9553, 0x0B4A47, 0x6B553B, 0x0AD54F, 0x055A45, 0x4A5D38, 0x0A5B4C, 0x052B42, 0x3A93B6,
	# //*2071-2080*/
	0x069349, 0x7729BD, 0x06AA51, 0x0AD546, 0x54DABA, 0x04B64E, 0x0A5743, 0x452738, 0x0D264A, 0x8E933E,
	# //*2081-2090*/
	0x0D5252, 0x0DAA47, 0x66B53B, 0x056D4F, 0x04AE45, 0x4A4EB9, 0x0A4D4C, 0x0D1541, 0x2D92B5  # //*2091-2099*/
]
ymc = [u"正月", u"二月", u"三月", u"四月", u"五月", u"六月", u"七月", u"八月", u"九月", u"十月", u"十一月", u"腊月"]
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


# 获取月份天数
def get_month_days(year, month):
	global MONTH_DAYS
	if (month == 2):
		if (((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)):
			return 29
		else:
			return 28
	else:
		return (MONTH_DAYS[month])


# 获取年份天数
def get_syear_days(syear):
	if (((syear % 4 == 0) and (syear % 100 != 0)) or (syear % 400 == 0)):
		return 366
	else:
		return 365


# 获取太阳年天数
def get_days_of_syear(syear, smonth, sday):
	""" get given day's number of sun year """
	days = 0
	for i in range(1, smonth):
		days += get_month_days(syear, i)
	days += sday
	return days


# 获取农历年天数
def get_days_of_lyear(syear, smonth, sday):
	""" get given day's number of the lunar year """
	global LUNAR_CALENDAR_TABLE
	lyear = syear
	spring_month = (LUNAR_CALENDAR_TABLE[syear - 1901] & 0x60) >> 5
	spring_day = (LUNAR_CALENDAR_TABLE[syear - 1901] & 0x1F)
	if ((spring_month > smonth) or ((spring_month == smonth) and (spring_day > sday))):
		# the day is before spring festival day, and is previous day in lunar year
		spring_month = (LUNAR_CALENDAR_TABLE[syear - 1901 - 1] & 0x60) >> 5
		spring_day = (LUNAR_CALENDAR_TABLE[syear - 1901 - 1] & 0x1F)
		lyear -= 1
		lunar_days = get_syear_days(lyear) + get_days_of_syear(syear, smonth, sday) \
					 - get_days_of_syear(lyear, spring_month, spring_day)
	else:
		lunar_days = get_days_of_syear(syear, smonth, sday) \
					 - get_days_of_syear(syear, spring_month, spring_day)
	lunar_days += 1  # consider current day
	return (lyear, lunar_days)


# 获取农历日期   八月十五
def get_lunar_calendar(time):
	today = str(time)  # 如 2019-08-08
	today_list = today.split('-')  # ['2019', '08', '08']
	syear, smonth, sday = int(today_list[0]), int(today_list[1]), int(today_list[2])
	if syear < 1901 or syear > 2099:
		return
	# lunar year, lunar days to spring festival
	lyear, lunar_days = get_days_of_lyear(syear, smonth, sday)
	l_double_month = (LUNAR_CALENDAR_TABLE[lyear - 1901] >> 20) & 0xF
	
	lmonth = lday = 1
	bits = 19
	month_begin_day = 0
	for lmonth in range(1, 14):
		l_month_big = (LUNAR_CALENDAR_TABLE[lyear - 1901] >> bits) & 0x1
		if month_begin_day + 29 + l_month_big < lunar_days:
			lmonth += 1
			month_begin_day += 29 + l_month_big
		else:
			lday = lunar_days - month_begin_day
			break
		bits -= 1
	if l_double_month:
		# lunar double month adjust
		if l_double_month == lmonth - 1:
			lmonth -= 1
			lmonth += 100  # double month
		elif l_double_month < lmonth - 1:
			lmonth -= 1
	# print (lyear, lmonth, lday)  # 农历日期
	return (ymc[lmonth - 1] + rmc[lday - 1]).encode("utf-8")


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
	cal_list = []
	fes_list = []
	for i in range(90):
		time = (datetime.datetime.now() + datetime.timedelta(i)).strftime("%Y-%m-%d")
		fes = get_festival(time)
		cal = get_calendaricity(time)
		if cal:
			if cal not in cal_list:
				cal_list.append(cal)
		if fes:
			if fes not in fes_list:
				fes_list.append(fes)
	res_list = fes_list + cal_list
	return ",".join(res_list)

print('将来三个月内将发生的节日和节气为："%s"'%(get_fes_cal()))  # 直接输出