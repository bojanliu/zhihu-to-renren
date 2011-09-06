# -*- coding:utf-8 -*-
#filename:zhihu_to_renren.py
#自动登录知乎网站,抓取explore页面,自动登录人人网发表日志
import cookielib
import urllib2
import urllib
from pyquery import PyQuery as pq

cj=cookielib.CookieJar()#建立Cookie实例
cookies=urllib2.HTTPCookieProcessor(cj)
opener=urllib2.build_opener(cookies)#建立opener与cookie关联
urllib2.install_opener(opener)
post_data=urllib.urlencode({
            'email':'******@gmail.com',
            'password':'******',
            })#登录知乎的表单数据
headers={'User-Agent':'IE',}#伪装成浏览器访问
req=urllib2.Request(url='http://www.zhihu.com/login',#zhihu的登录url
                    data=post_data,
                    headers=headers,
                    )
result=urllib2.urlopen(req)#发送http请求
#--------------------------------------------------------------------#
html_source=pq(url='http://www.zhihu.com/explore')#抓取知乎热门问答页面内容
html_source=html_source(".xvq.xaq").html()#根据类名得到排名第一的问答块HTML内容
result=pq(html_source)
title=result('.xmq').text() #提取出题目
content=result('.xbq').html()#提取出回答内容，保留html标签，以保证日志格式
link=result('.xmq').find('a').attr('href')#提取出原文链接
author=result('.xrq').find('img').attr('title')#提取出作者
#--------------------------------------------------------------------#
if all((html_source,title,content,link,author,),):#判断是否有值为None
    link='www.zhihu.com'+link
    post_data=urllib.urlencode({ 
                'email':'******',
                'password':'******',
                'domain':'renren.com',
                })#登录人人的表单数据
    req=urllib2.Request(url='http://www.renren.com/PLogin.do',#人人的登录url
                        data=post_data,
                        headers=headers,
                        )
    result=urllib2.urlopen(req)#发送http请求
    html_source=pq(url='http://blog.renren.com/NewEntry.do')
    post_id=html_source('#postFormId').attr('value')#获得postFormId值
    post_data=urllib.urlencode({
        'title':'知乎每日热门问答——%s'%title.encode("utf-8"),#日志标题
        'body':"<p>回答者：%s</p>%s<p>原地址：%s</p>"#日志内容
            %(author.encode("utf-8"),
              content.encode("utf-8"),
              link.encode("utf-8"),),
        'categoryId':'0',
        'blogControl':'99',
        'postFormId':post_id,
        'relative_optype':'saveDraft',
                            })
    req=urllib2.Request(url='http://blog.renren.com/NewEntry.do',#发表日志url
                         data=post_data,
                         headers=headers,)
    result=urllib2.urlopen(req)
    print 'it is over!'
else:
    print 'sorry, but there is an error!'

