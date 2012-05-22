#coding:utf-8
#file_name:zhihu_to_renren.py
#time:20120518

import cookielib
import urllib2
import urllib
from pyquery import PyQuery as pq
import re


def setup_cookie():
    cj=cookielib.CookieJar()
    cookies=urllib2.HTTPCookieProcessor(cj)
    opener=urllib2.build_opener(cookies)
    urllib2.install_opener(opener)

def auto_post(post_url, post_data):
    header_info={'User-Agent':'IE',}
    req=urllib2.Request(
        url=post_url,
        headers=header_info,
        data=post_data,
        )
    result=urllib2.urlopen(req)

#登录知乎
def login_zhihu():
    login_email='********@gmail.com'
    login_password='********'
    login_url='http://www.zhihu.com/login' 
    post_data=urllib.urlencode({
        'email':login_email,
        'password':login_password,
        })
    auto_post(login_url,post_data)

#解析知乎
def parse_zhihu():
    #待解析页面——知乎“发现”页面
    target_url='http://www.zhihu.com/explore'
    
    data=urllib2.urlopen(target_url).read()
    #得到“发现页面”首篇文章链接
    link_1=re.findall(r'/question/(\d{8})/',data)
    link_2=re.findall(r"""/answer/(\d{8})">""",data)
    link='http://www.zhihu.com/question/%s/answer/%s'%(link_1[0],link_2[0])

    data=urllib2.urlopen(link).read()
    
    #得到文章正文，带HTML标签的。
    p=re.compile(r"""data-action="/answer/content">(.*?)</div>""",re.S)
    content=p.findall(data)

    #得到文章标题
    title=re.findall(r"""<a href="/question/\d{8}">(.*?)</a>""",data)

    #得到文章回答者
    author=re.findall(r"""<a data-tip=".*?" href="/people/.*?">(.*?)</a>""",data)

    #得到回答者自我描述
    about=re.findall(r"""<strong title=".*?" class=".*?">(.*?)</strong>""",data)

    return [title, link, content, author, about]

#登录人人
def login_renren():
    login_renren_email='********'
    login_renren_passwd='*******'
    login_renren_url='http://www.renren.com/PLogin.do'
    domain='renren.com'
    post_data=urllib.urlencode({
        'email':login_renren_email,
        'password':login_renren_passwd,
        'domain':domain,
        })
    auto_post(login_renren_url,post_data)

#发表人人日志
def post_renren_blog():
    post_blog_url='http://blog.renren.com/NewEntry.do'

    #解析得出post_id这个动态生成的值
    html_source=pq(url=post_blog_url)
    post_id=html_source('#postFormId').attr('value')

    #日志内容即来自解析知乎得到的文章数据
    zhihu_data=parse_zhihu()

    #发表人人日志提交的数据
    post_data=urllib.urlencode({
        'title':'知乎每日热门问答——%s'%zhihu_data[0][0],
        'body':"""<p>Posted by zhihu2renren Robot——每天十点，分享知乎精彩问答！</p>
                  <p>原文地址：%s</p>
                  <p>回答者：%s</p>
                  <p>回答者简介：%s</p>%s
               """%(zhihu_data[3][0],
                    zhihu_data[1],
                    zhihu_data[4][0],
                    zhihu_data[2][0],),
        'categoryId':'0',
        'blogControl':'99',
        'postFormId':post_id,
        'relative_optype':'saveDraft',
        })
    auto_post(post_blog_url,post_data)
    

def main():
    setup_cookie()
    login_zhihu()
    login_renren()
    post_renren_blog()
    print 'ok'

if __name__=='__main__':
    main()