# AT-UI Web 自动化测试管理平台

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Django](https://img.shields.io/badge/Django-2.2+-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一个基于 Django 的 Web 自动化测试管理平台，提供测试用例管理、智能元素定位、并发执行、定时监控等功能。

## 📋 目录

- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [详细说明](#详细说明)
- [API 接口](#api-接口)
- [智能元素维护](#智能元素维护)
- [监控与报告](#监控与报告)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)

## 🚀 功能特性

### 核心功能
- **多端管理**: 支持管理多个测试环境（开发、测试、生产等）
- **用例管理**: 可视化测试用例管理，支持 Python 脚本和 Excel 关键字驱动
- **并发执行**: 支持多线程并发执行测试用例，可配置最大并发数
- **定时监控**: 自动定时执行监控用例，支持邮件和钉钉通知
- **智能维护**: 内置 mynium 智能元素定位算法，自动维护失效元素
- **测试报告**: 自动生成 HTML 测试报告，支持 Word 格式导出

### 高级特性
- **元素库管理**: 统一管理页面元素，支持云端同步
- **权限控制**: 基于用户的权限管理系统
- **客户端下载**: 支持打包下载独立测试客户端
- **工具上传**: 支持上传自定义工具函数脚本
- **失败重试**: 可配置用例失败重试次数
- **截图记录**: 自动截图记录测试过程

## 🏗️ 技术架构

```
at-ui/
├── MyProject/          # Django 项目主目录
│   ├── settings.py     # 项目配置
│   ├── urls.py         # 路由配置
│   └── wsgi.py         # WSGI 配置
├── Myapp/              # 主应用
│   ├── models.py       # 数据模型
│   ├── views.py        # 视图逻辑
│   ├── monitor.py      # 监控模块
│   ├── templates/      # HTML 模板
│   └── static/         # 静态资源
├── MyClient/           # 测试客户端
│   └── demo_client/    # 客户端模板
│       ├── cases/      # 测试用例
│       ├── public/     # 公共工具
│       └── reports/    # 测试报告
└── db.sqlite3          # SQLite 数据库
```

**技术栈：**
- 后端：Django 2.2+ + SQLite
- 前端：HTML + CSS + JavaScript + Vue.js
- 测试：Selenium WebDriver + unittest
- 其他：Python 3.7+, Bootstrap

## 🛠️ 快速开始

### 环境要求

```bash
Python >= 3.7
Django >= 2.2
selenium
requests
Levenshtein
python-docx
```

### 安装部署

1. **克隆项目**
```bash
git clone <repository-url>
cd at-ui
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **初始化数据库**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **创建超级用户**
```bash
python manage.py createsuperuser
```

5. **启动服务**
```bash
python manage.py runserver 0.0.0.0:8000
```

6. **访问平台**
打开浏览器访问 `http://localhost:8000`

### 基本配置

1. **配置 Chrome 驱动**
   - 下载对应版本的 ChromeDriver
   - 确保 chromedriver 在系统 PATH 中

2. **配置通知服务**（可选）
   - 邮件服务：修改 `monitor.py` 中的邮件配置
   - 钉钉机器人：配置钉钉机器人 webhook 地址

## 📖 详细说明

### 用户管理

**注册/登录**
- 支持用户注册和登录功能
- 基于 Django 内置认证系统
- 支持密码修改功能

**权限管理**
- 端的创建者拥有完全权限
- 支持特殊权限配置（删除端、删除用例等）

### 端管理

**创建测试端**
```python
# 在首页点击"新增端"
端名: 测试环境A
host: http://test.example.com,http://test2.example.com
```

**端配置**
- **监控设置**: 配置监控主机、执行时间、通知方式
- **并发设置**: 设置最大并发数（默认5）
- **权限设置**: 管理端的访问权限

### 用例管理

**上传测试脚本**
```python
# 示例测试用例结构
import unittest
from selenium import webdriver
from public.tools import *

class TEST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
    
    @tool_rerun(setUp, tearDown, 3)  # 失败重试3次
    def test_001(self):
        '测试用例描述'
        tool_get_url(self, par['host'])
        tool_get_object(self, 1).send_keys('测试内容')
```

**用例配置**
- **BF（并发）**: 是否参与并发执行
- **JK（监控）**: 是否参与定时监控
- **重试次数**: 失败重试次数设置

### 执行方式

**单个执行**
```bash
# 选择主机执行单个用例
Host: http://test.example.com
```

**并发执行**
```bash
# 执行所有标记为BF的用例
最大并发数: 5（可配置）
```

**定时监控**
```bash
# 自动执行所有标记为JK的用例
监控间隔: 30分钟（可配置）
```

## 🔌 API 接口

### 外部调用接口

**执行用例**
```bash
GET /waibu_run_case/?case_id=1&host=http://test.com
```

**获取元素**
```bash
GET /waibu_get_object/1/
```

**更新元素**
```bash
POST /waibu_update_object/1/
```

### 响应格式
```json
{
    "errcode": 200,
    "errmsg": "",
    "content": {}
}
```

## 🧠 智能元素维护

### Mynium 算法

当元素定位失败时，mynium 会自动执行以下步骤：

1. **属性提取**: 从原始元素 HTML 中提取关键属性
2. **相似元素查找**: 根据标签名查找所有同类型元素
3. **相似度计算**: 使用 Levenshtein 距离算法计算相似度
4. **最优匹配**: 选择相似度最高的元素
5. **自动更新**: 更新云端元素库

### 支持的属性
- id, name, class
- text, value, placeholder
- onclick, style, href, type

### 使用示例
```python
# 自动调用 mynium 进行元素维护
element = tool_get_object(self, element_id)
```

## 📊 监控与报告

### 监控功能

**配置监控**
```python
监控主机: http://test.example.com
监控时间: 30  # 分钟
监控手机: 13800138000
监控邮箱: test@example.com
钉钉机器人: https://oapi.dingtalk.com/robot/send?access_token=xxx
```

**监控流程**
1. 定时执行标记为 JK 的用例
2. 生成执行结果统计
3. 发送通知（邮件/钉钉/短信）

### 报告系统

**HTML 报告**
- 自动生成详细的 HTML 测试报告
- 包含用例执行状态、截图、错误信息

**Word 报告**
- 支持导出 Word 格式的测试报告
- 包含报告概览和详细链接

**报告统计**
```
小用例总数: 15
通过的小用例总数: 12
失败和报错的小用例总数: 3
出错或失败的用例: 登录测试,支付测试
```

## 🔧 工具函数

### 常用工具函数

```python
# URL 跳转
tool_get_url(self, url)

# 元素获取（智能定位）
tool_get_object(self, object_id)

# 断言检查
tool_assert_exit(self, *elements)

# 截图
tool_screen(self, filename, mode)

# iframe 切换
tool_iframe(self, index=0)

# 根据文案查找元素
tool_classlink(self, class_name, link_text)

# 失败重试装饰器
@tool_rerun(setUp, tearDown, retry_count)
```

### 自定义工具函数
- 支持上传自定义 tools.py 文件
- 统一的命名规范（tool_ 前缀）
- 自动同步到测试客户端

## ❓ 常见问题

### Q: 如何配置 Chrome 驱动？
A: 下载对应版本的 ChromeDriver，放置在系统 PATH 或项目目录中。

### Q: 元素定位失败怎么办？
A: 平台内置 mynium 智能维护功能，会自动寻找最相似的元素并更新元素库。

### Q: 如何设置并发数？
A: 在端管理页面可以设置最大并发数，默认为5。

### Q: 监控通知不生效？
A: 检查邮件服务器配置和钉钉机器人 webhook 地址是否正确。

### Q: 如何编写测试用例？
A: 参考 `demo_linear.py` 示例，使用提供的工具函数编写测试脚本。

### Q: 支持哪些文件格式？
A: 支持 Python 脚本（.py）和 Excel 关键字表（.xls）。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发规范
- 工具函数必须以 `tool_` 开头
- 代码注释要清晰完整
- 提交前进行充分测试

### 目录规范
- 新功能在 `Myapp/views.py` 中添加
- 静态资源放在 `Myapp/static/` 下
- 模板文件放在 `Myapp/templates/` 下

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

---

**项目维护**: yiyan  
**最后更新**: 2022年12月  
**官方网站**: [项目地址](https://github.com/yourorg/at-ui) 