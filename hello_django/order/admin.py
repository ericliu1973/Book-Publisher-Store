from django.contrib import admin
from .models import Order,OrderItem
from django.http import HttpResponse
import datetime
import csv
from django.shortcuts import reverse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')   #声明HttpResponse返回的是一个csv文件
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write the header row   上一句利用列表生成式创建一个针对model 非多对多和非一对多的字段列表：含数据库名表名字段名
    writer.writerow([field.verbose_name for field in fields])
    # write data rows   提取字段的真正名称填入CSV文件的头行
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)   #提取每个字段对应的数值
            if isinstance(value, datetime.datetime):  #如果为日期数据类型则格式化之
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)  #加入记录的列表
        writer.writerow(data_row)   #完成一个记录则写入的CSV文件中
    return response
export_to_csv.short_description = 'Export to CSV'   #在admin管理界面中进行说明

def order_detail(obj):
    return '<a href="{}">View</a>'.format(reverse('order:admin_order_detail',
                                                  args=[obj.id]))  #其返回的是一个HTML字符串
order_detail.allow_tags = True

def order_pdf(obj):
    return '<a href="{}">PDF</a>'.format(reverse('order:admin_order_pdf',
                                                 args=[obj.id]))
order_pdf.allow_tags = True
order_pdf.short_description = 'PDF bill'



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','post_code','city','paid','created','updated',order_detail,order_pdf]
    list_filter = ['paid','created','updated']
    inlines=[OrderItemInline]
    actions = [export_to_csv]
admin.site.register(Order,OrderAdmin)


# Register your models here.
