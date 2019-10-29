"""
set_viewport_size(w,h):用来设置浏览器窗口的尺寸，w代表宽度，h代表高度
go(url, baseurl, headers, http_method, body,formdata):完成指定页面的加载
url:需要加载的页面的网址
baseurl:可选参数，默认为空，表示资源加载的相对路径
headers：可选参数，默认为空，用来设置请求的header
http_method:可选参数，默认为get，如果是post此时需要设置
body：可选参数，默认为空，发送POST请求时向服务器传输的参数数据
formdata：可选参数，默认为空，POST的时候对应的表单数据，默认使用form表单默认的编码格式即application/x-www-form-urlencode
wait(time, cancle_on_redirect, cancel_on_error):用来等待网页的加载，对应的时间以秒为单位
time:等待网页加载的时间
cancle_on_redirect：可选参数，默认为false，用来设置当网页发生重定向时是否结束等待
cancle_on_error：可选参数，默认为false，用来设置当网页发生错误时是否结束等待

png():将加载之后的网站截屏，并且以png格式返回
html():将加载之后的网站以html格式返回
jpeg():将加载之后的网站截屏并且以jpg格式返回

jsfunc():将自定的javascript方法转化成lua方法， 但是自定义方法必须包含在[[]]中
autoload():完成第三方资源远程链接加载
"""
lua1='''
    function main(splash,args)
        splash:set_viewport_size(1500,3500)
        splash:go(args.url)
        splash:wait(args.wait)
        
        scrool_top=splash:jsfunc([[
            function(x,y){
            window.scrollTO(x,y)
            }
        ]])
        scrool_top(0,500)
        splash:wait(args.wait/3)
        return {model_name=args.model_name,data=splash:html()}
    end
'''
#定义lua语法模拟用户在英雄页面点击操作
lua_hero='''
        function main(splash,args)
            splash:set_viewport_size(1200,2500)
            splash:autoload("https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js")
            splash:go(args.url)
            splash:wait(args.wait)
            
            click_btn=splash:jsfunc([[
                function(btn_sel){
                    $(btn_sel).click();
                }
            ]])
            result={model_name=args.model_name}
            for key,value in pairs(args.kind_dic) do
                sel=string.format('label[data-id=%s]',key)
                 click_btn(sel)
                 splash:wait(args.wait/2)
                 result[value]=splash:html()  
            end
            return result
        end    
'''