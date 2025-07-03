# coding:utf-8
# 创建者:
# 意义作用: 脚本的公共函数部分
# 更新时间: 2021.7.4
import time
import unittest
import requests
import re

try: #本地调用
    from MyClient.client_47.public.htmlRunner import HTMLTestRunner
    from public.mynium import getelement
except: # 平台调用
    exec('from MyClient.%s.public.myhtmlRunner import HTMLTestRunner'% str(__file__).split('/')[-3])
    exec('from MyClient.%s.public.mynium import getelement' % str(__file__).split('/')[-3])
# ------------------------------------------工具函数
# 注意事项: 不可随意更改,要时刻和平台上的保持一致,有了更改请及时上传
# 命名规范: 全部已tool_开头,以便在脚本中使用联想
# 函数规范: 结构清晰且有注释,建议写明函数的作用和返回体格式
# 入参规则: 第一个参数必须为self,意为接受用例类本身,方便使用内部类变量
# 调用规则: 第一个参数必须为cls/self
# 路径问题: 因启动方式为俩种(本地调试,平台调用),所以要写两套,可参考其他函数

def tool_get_url(self,url) -> None:
    '跳转到初始页面'
    self.driver.get(url)
    time.sleep(1)
    self.driver.implicitly_wait(5)

def tool_run(self,par)->None:
    '启动器'
    ## 平台启动
    if par['which'] == 'P':
        with open("MyClient/%s/reports/"%str(__file__).split('/')[-3]+par['report_name'],'wb') as fp:
            runner = HTMLTestRunner(fp,title='WEB自动化测试报告',description='这是ui自动化测试平台生产',which='P')
            runner.run(unittest.makeSuite(self))
    else:
        ## 本地调试
        with open("../reports/"+par['report_name'],'wb') as fp:
            runner = HTMLTestRunner(fp, title='WEB自动化测试报告', description='这是ui自动化测试平台生产')
            runner.run(unittest.makeSuite(self))

def tool_login(self)->None:
    '登录脚本,请自行修改成自己端的登录脚本'
    # self.driver.find_element_by_id("username").send_keys("您的用户名")
    # self.driver.find_element_by_id("password").send_keys("您的密码")
    # self.driver.find_element_by_id("login").click()
    # time.sleep(3)

def tool_classlink(self,class_name,link_text):
    '根据className 找到目标文案的元素'
    els = self.driver.find_elements_by_class_name(class_name)
    for i in els:
        if i.text == link_text:
            return i
    raise Exception('【没找到: %s 下且文案为: %s 的元素】'%(class_name,link_text))

def tool_iframe(self,index=0):
    '自定跳转到内部iframe,index是序号,默认0,即第一个'
    iframe = self.driver.find_elements_css_selector('iframe')[index]
    self.driver.switch_to.frame(iframe)

def tool_assert_exit(self,*args):
    '检查args内所有元素是否存在,可以写class_name,name,id,'
    for i in args:
        a = len(self.driver.find_elements_by_class_name(i))
        b = len(self.driver.find_elements_by_name(i))
        c = len(self.driver.find_elements_by_id(i))
        if a+b+c == 0:
            raise Exception('【没找到:%s】'%i)

def tool_rerun(s,t,n):
    's:setup,t:teardown,n:counts'
    def decorator(xingfangfa):
        def wrapper(*a, **w):
            for i in range(n):
                try:
                    print('-------------------\nNum:', i)
                    re = xingfangfa(*a, **w)
                    print('success \n-------------------')
                    return re
                except Exception:
                    print('have a error ')
                    t(*a)
                    s(*a)
                    print('\n-------------------')
            raise Exception
        return wrapper
    return decorator

def tool_get_obejct(self,oid):
    res = requests.get('http://127.0.0.1:8000/waibu_get_object/%s/'%int(oid)) #地址别忘替换平台服务器地址和端口
    print(res.json())
    try:### 定位成功，就返回这个元素
        obj = self.driver.find_elements(res.json()['tmp_method'].replace('_',' '),res.json()['tmp_value'])[res.json()['index']]
        return obj
    except:### 定位不成功，调用mynium
        obj = getelement(self.driver,res.json())
        return obj


def tool_screen(self,png_name,which):
    if which == 'C':
        self.driver.get_screenshot_as_file('../reports/'+png_name)
    else:
        self.driver.get_screenshot_as_file("Myapp/static/reports_png/"+png_name)
