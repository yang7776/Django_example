"""
动态页面获取：（phantomjs，selenium）
1. 下载phantomjs
2. selenium 是一个用于Web应用程序测试的工具。Selenium测试直接运行在浏览器中,就像真正的用户在操作一样。
3. 配置环境变量
4. cmd管理员下 pip install selenium
"""
from selenium import webdriver
import time
# 构建无头浏览器对象
browser = webdriver.PhantomJS()
# 直接使用浏览器对象渲染页面
browser.get('https://www.jd.com/')
result = browser.find_elements_by_xpath('//img')
# 点击网页中的button按钮
# browser.find_element_by_xpath('//button').click()
# 想网页中输入框输入内容
# browser.find_element_by_xpath('//input').send_keys('yyy')
# 设置网页向上滚动500px
print(len(browser.page_source))
for i in range(47):
    time.sleep(5)
    browser.execute_script('document.body.scrollTop={}'.format(1200+i*299))
# print(result)
    print(i,len(browser.page_source))