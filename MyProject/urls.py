"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from Myapp.views import *


urlpatterns = [
    path('index/',index),# 进入登录页面
    path('index_error/', index_error),  # 进入登录页面 输入错误密码后
    path('login_action/',login_action),#登录功能
    path('login_action/None/', login_action),  # 登录功能
    path('register_action/', register_action),  # 注册功能
    path('accounts/login/',index), #自动跳转
    path('logout/',logout),#退出

    path('admin/', admin.site.urls),
    path('home/', home), # 进入首页
    path('', home), # 进入首页
    path('save_duan/', save_duan) ,#保存新端
    re_path('del_duan/(?P<did>.+)/',del_duan),#删除端
    re_path('case_list/(?P<did>.+)/', case_list),  # 进入列表页面
    re_path('add_case/(?P<did>.+)/', add_case),  # 添加用例
    re_path('del_case/(?P<cid>.+)/', del_case),  # 删除用例
    path('set_case/',set_case),# 获取用例数据
    path('save_case/', save_case),  # 保存用例
    path('save_monitor/',save_monitor),#保存监控设置
    path('save_old_duan/', save_old_duan),  # 保存旧端
    re_path('upload_py/(?P<cid>.+)/',upload_py),# 上传脚本
    path('run_case/',run_case), #执行脚本
    path('waibu_run_case/',waibu_run_case), #外部接口调用
    re_path('bf_case/(?P<did>.+)/', bf_case),  # 并发用例
    re_path('start_monitor/(?P<did>.+)/',start_monitor), # 启动监控
    re_path('stop_monitor/(?P<did>.+)/', stop_monitor),  # 关闭监控
    re_path('look_report/(?P<cid>.+)/', look_report), #查看报告
    re_path('download_client/(?P<did>.+)/',download_client), #下载本地调试包
    path('look_reports/',look_reports),#查看多个报告的总结
    re_path('download_reports/(?P<did>.+)/', download_reports),  # 下载测试报告
    re_path('upload_tools/(?P<did>.+)/',upload_tools),# 上传tools.py等工具函数脚本
    re_path('object_in/(?P<did>.+)/',object_in) , # 打开元素库
    re_path('add_object/(?P<did>.+)/', add_object),  # 新增元素
    path('save_object/', save_object),  # 保存元素
    re_path('del_object/(?P<oid>.+)/', del_object),  # 删除元素

    re_path('waibu_get_object/(?P<oid>.+)/',waibu_get_object), #外部获取元素信息
    re_path('waibu_update_object/(?P<oid>.+)/', waibu_update_object),  # 外部更新元素信息

]
