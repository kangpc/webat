import xlrd
import unittest
from selenium import webdriver
import os,sys
try:
    from public.tools import *
except:
    exec('from MyClient.%s.public.tools import *' % str(__file__).split('/')[-3])

par = {}

try:
    fname = sys.argv[1].split('/')[-1]
    par['host'] = sys.argv[2]
    counts = int(sys.argv[3])
    tmp_path = 'MyClient/%s/cases/'%str(__file__).split('/')[-3]
    ...
except:
    fname = '第十周六关键字表.xls'
    par['host'] = 'http://www.baidu.com' #本地调试请手动填写主页
    counts = 3
    tmp_path = '../cases/'
    ...
par['report_name'] = fname.replace('.xls','.html')

class TEST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        tool_get_url(self,par['host'])

    def tearDown(self):
        time.sleep(1)

    @tool_rerun(setUp,tearDown,counts)
    def begin_demo(self,case_datas): #这是用例的母体
        '这是用例demo的描述'
        print(case_datas)
        steps =case_datas['steps']
        for step in steps:
            if step['act'] == '输入':
                tool_get_obejct(self,step['object_id']).send_keys(step['content'])
            elif step['act'] == '点击':
                tool_get_obejct(self,step['object_id']).click()
            elif step['act'] == '断言':
                self.assertEqual(tool_get_obejct(self,step['object_id']).text,step['content'])
            elif step['act'] == '清空':
                tool_get_obejct(self,step['object_id']).clear()
            elif step['act'] == '时间等待':
                time.sleep(int(step['content']))
            # 这里可以添加各种动作
            else:
                print('请检查该元素【%s】的act动作！'%(step['name']))
            time.sleep(1)


def make_demo(case_datas):
    def demo(self):
        TEST.begin_demo(self,case_datas)
    setattr(demo,'__doc__',str(case_datas['CASE_NAME']+':'+case_datas['CASE_DES']))
    return demo

def make_test(excel_datas):
    for i in range(len(excel_datas)):
        setattr(TEST,'test_%s'%str(i+1),make_demo(excel_datas[i]))


def read_excel(fname):
    SZ = xlrd.open_workbook(fname)
    sheet = SZ.sheet_by_index(0)
    datas = []
    rows = sheet.nrows
    CASE_tmp = {}
    for i in range(rows):
        if sheet.cell_value(i,0) == 'CASE': #说明这行是用例
            datas.append(CASE_tmp)
            CASE_tmp = {}
            CASE_tmp['CASE_NAME'] = sheet.cell_value(i,1)
            CASE_tmp['CASE_DES'] = sheet.cell_value(i,2)
            CASE_tmp['steps'] = []
        else: # 说明这行是具体步骤
            step_tmp = {}
            step_tmp["name"] = sheet.cell_value(i,1)
            step_tmp["act"] = sheet.cell_value(i,2)
            step_tmp["content"] = sheet.cell_value(i,3)
            step_tmp["object_id"] = sheet.cell_value(i,4)
            CASE_tmp['steps'].append(step_tmp)
    datas.append(CASE_tmp)
    datas.pop(0)
    return datas

if __name__ == '__main__':
    # 读取Excel表
    excel_datas = read_excel(tmp_path+fname)
    # 根据表内容给TEST生成子函数
    make_test(excel_datas)

    # 调用启动器
    tool_run(TEST, par)