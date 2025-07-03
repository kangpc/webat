from django.db import models

# Create your models here.

class DB_href(models.Model):
    name = models.CharField(max_length= 20,null=True,blank=True)
    url = models.CharField(max_length=510,null=True,blank=True)
    def __str__(self):
        return self.name

class DB_duan(models.Model):
    name = models.CharField(max_length= 20,null=True,blank=True)
    monitor_time = models.CharField(max_length=200, null=True,blank=True)
    monitor_host = models.CharField(max_length=200, null=True,blank=True)
    monitor_phone= models.CharField(max_length=200, null=True,blank=True)
    monitor_email = models.CharField(max_length=200, null=True,blank=True)
    monitor_dingtalk = models.CharField(max_length=200, null=True,blank=True)
    host = models.CharField(max_length=100,null=True,blank=True)
    user = models.CharField(max_length=20,null=True,blank=True)
    max_bf = models.IntegerField(default=5)
    def __str__(self):
        return self.name

class DB_case(models.Model):
    name = models.CharField(max_length= 50,null=True,blank=True,default='-')
    duan_id = models.CharField(max_length= 20,null=True,blank=True)
    BF = models.BooleanField(default=True) # 参与并发
    JK = models.BooleanField(default=True) # 参与监控
    py = models.CharField(max_length= 20,null=True,blank=True) #绑定的脚本名字
    counts = models.IntegerField(default=1) # 失败重试次数
    def __str__(self):
        return self.name

class DB_quanxian(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    users = models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return self.name

class DB_object(models.Model):
    duan_id = models.CharField(max_length=10,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    page = models.CharField(max_length=50,null=True,blank=True)
    tmp_method = models.CharField(max_length=30,null=True,blank=True)
    tmp_value = models.CharField(max_length=200,null=True,blank=True)
    tag = models.CharField(max_length=300,null=True,blank=True)
    index = models.IntegerField(default=0) #下标
    def __str__(self):
        return self.name




