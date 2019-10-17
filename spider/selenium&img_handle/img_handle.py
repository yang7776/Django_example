# http://www.ztbu.edu.cn/captcha/0.4799088653558454
from PIL import Image
from pytesseract import image_to_string
import urllib3,os

# 创建网络请求
http = urllib3.PoolManager()
header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36','Content-type':'text/json'}

res = http.request('get','http://www.ztbu.edu.cn/captcha/1',headers=header)
# 将下载的验证码，存储到指定路径
f = open('yzm/ys.png','wb+')
f.write(res.data)
f.close()

# 打开文件中的验证码
img = Image.open('yzm/ys.png')
# 图像灰度处理
# 获取图像所有的像素点(pix是一个二维列表)
pix = img.load()
# 获取图片的宽度和高度
w,h = img.size
for i in range(w):
    for j in range(h):
        # 把每一个像素点求RGB平均值。pix[像素点1,像素点2，...]，像素点1（R,G,B）
        val = (pix[i,j][0]+pix[i,j][1]+pix[i,j][2])//3
        pix[i,j] = (val,val,val,255)
img.save('yzm/yz1.png','png')
# 将经过灰度处理之后的图片进行二值化处理
img = Image.open('yzm/yz1.png')
pix = img.load()
for i in range(w):
    for j in range(h):
        if pix[i,j][0] <= 100:
            pix[i,j] = (0,0,0)
        else:
            pix[i,j] = (255,255,255)
img.save('yzm/yz2.png','png')
# 图片转变为黑白图片
img.convert('L')
# 开始识别图片中的验证码
# -psm 7代表将整个验证码视为一行文本
txt = image_to_string(img,config='-psm 7')
print(txt)