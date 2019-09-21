# -*- coding: utf-8 -*-
# writer        Yang   
# create_time   2019/9/21 9:40
# file_name     pillow_test.py
from PIL import Image
import os
import pytesseract

"""
爬取验证码：

# 创建网络请求
http = urllib3.PoolManager()
header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36','Content-type':'text/json'}

res = http.request('get','http://www.ztbu.edu.cn/captcha/1',headers=header)
# 将下载的验证码，存储到指定路径
f = open('yzm/ys.png','wb+')
f.write(res.data)
f.close()
"""
# 打开图片
img_path = os.path.join(os.path.abspath('../source/img'),"pil_img.jpg")
img = Image.open(img_path)
# 获取图像所有的像素点(pix是一个二维列表)
pix = img.load()
# 获取图片的宽度和高度
w,h = img.size
# 把每一个像素点求RGB平均值。pix[像素点1,像素点2，...]，像素点1（R,G,B）
for i in range(w):
    for j in range(h):
        val = (pix[i,j][0]+pix[i,j][1]+pix[i,j][2])//3
        pix[i,j] = (val,val,val,255)
img.save('2.jpg')
# 将经过灰度处理之后的图片进行二值化处理
img = Image.open('2.jpg')
pix = img.load()
for i in range(w):
    for j in range(h):
        if pix[i,j][0] <= 100:
            pix[i,j] = (0,0,0)
        else:
            pix[i,j] = (255,255,255)
img.save('3.jpg')
# 图片转变为黑白图片
img.convert('L')
# 识别图片文字（注意：安装 Tesseract-OCR 以及 对应中文包)
txt = pytesseract.image_to_string(img,config='chi_sim')
print(txt)