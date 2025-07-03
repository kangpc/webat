import unittest
from selenium import webdriver
import time
import sys,os
try:
    from public.tools import *
except:
    exec('from MyClient.%s.public.tools import *' % str(__file__).split('/')[-3])

par = {}
par['report_name'] = str(os.path.basename(__file__)).replace('.py','.html')
try:
    par['host'] = sys.argv[1]
    counts = int(sys.argv[2])
    par['which'] = 'P'
    ...
except Exception as e:
    par['host'] = 'http://www.baidu.com' #本地调试请手动填写主页
    counts = 3
    par['which'] = 'C'
    ...


class TEST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        tool_get_url(self,par['host'])

    def tearDown(self,def_name='NONE'):
        tool_screen(self,'%s-%s.png'%(str(__file__).split('/')[-1].split('.')[0],def_name),par['which'])

    @tool_rerun(setUp,tearDown,counts)
    def test_001(self): #这是第一条用例
        '这是小用例的描述'
        print('第一条用例运行过了！')
        tool_get_obejct(self,1).send_keys('测试开发干货')



if __name__ == '__main__':
    tool_run(TEST,par)




