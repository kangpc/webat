from django.contrib import admin

# Register your models here.

from Myapp.models import *

admin.site.register(DB_href)
admin.site.register(DB_duan)
admin.site.register(DB_case)
admin.site.register(DB_quanxian)
admin.site.register(DB_object)
