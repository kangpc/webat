import sys,os

path = '/Users/zijiawang/Downloads/MyProject'
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyProject.settings'
import django
django.setup()
from Myapp.models import *
import time,subprocess
from Myapp.views import look_reports
import requests
import json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_report():
    '发送执行结果'
    httpresponse = look_reports({}, did=duan_id)
    content = httpresponse.content.decode()
    # 拿到端的所有数据
    duan = DB_duan.objects.filter(id=duan_id)[0]
    # # 邮件报告
    mail_to = duan.monitor_email.split(',')[0] # 发送给谁
    mail_host = "smtp.qq.com" #发送服务器是什么
    mail_user = "xxxxxxxx@qq.com" #发送者的qq邮箱
    mail_pass = "qjwoirjqoirj23123" # smtp的授权码
    c = MIMEText(content,'html','utf-8')
    msg = MIMEMultipart('related')
    msg['From'] = mail_user
    msg['To'] = mail_to
    msg['Subject'] = '自动化测试报告'
    msg.attach(c)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host,25)
        server.login(mail_user,mail_pass)
        server.sendmail(mail_user, mail_to, msg.as_string())
        print('邮件发送:success!')
        server.close()
    except Exception as e:
        print(e)
        print('邮件发送:fail!')
    # # 钉钉/飞书/企业微信机器人
    fei_url = duan.monitor_dingtalk
    data = {"msg_type":"text","content":{"text":content+"\nby.我去热饭"}}
    re = requests.post(fei_url,data=json.dumps(data))
    print(re.text)

    # 发送短信、电话
    # 先判断content 失败的多不多,有无必要报警
    # 俩种方案,1.你去第三方的云片网,你去买服务,客服会给你说明书,通过https请求来触发
    # 2.公司自己已经买过打电话发短信的服务,你让开发给你脚本或接口
    # 可能没必要这种紧急方式。




def monitor():
    while True:
        duan = DB_duan.objects.filter(id=duan_id)[0]
        host = duan.monitor_host
        cases = DB_case.objects.filter(duan_id = duan_id,JK=True)
        print('即将开始新一轮监控！')
        for case in cases:
            if case.py not in ['',None,' ','None']:
                if '.py' in case.py:
                    subprocess.call('python3 MyClient/client_%s/cases/%s %s %s' % (duan_id, case.py,host,case.counts), shell=True)
                elif '.xls' in case.py:
                    subprocess.call('python3 MyClient/client_%s/public/make_script.py %s %s %s' % (duan_id, case.py, host, case.conuts), shell=True)
        print('本轮监控执行完毕！')
        send_report()
        time.sleep(int(duan.monitor_time)*60)  # 间隔分钟

if __name__ == '__main__':
    duan_id = sys.argv[1]
    monitor()
