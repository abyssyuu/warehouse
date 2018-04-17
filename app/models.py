from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField
from versatileimagefield.fields import PPOIField, VersatileImageField

class Warehouse(models.Model):

    class Meta:
        db_table = 'warehouse'
        verbose_name = '仓库'
        verbose_name_plural = '仓库'

    name = models.CharField(null=True, blank=True, max_length=32, verbose_name='名称')
    area = models.FloatField(null=True, blank=True, verbose_name='面积')
    has_empty = models.BooleanField(default=True, verbose_name='存在空位')

    def __str__(self):
        return self.name


class HouseImport(models.Model):
    UNIT_CHOICES = (
        (0, '米(m)'),
        (1, '平方米(m^2)'),
        (2, '立方米(m^3)'),
        (3, '千克(kg)'),
        (4, '计数包装')
    )

    class Meta:
        db_table = 'house_import'
        verbose_name = '入库'
        verbose_name_plural = '入库'

    number = models.CharField(null=True, blank=True, max_length=32, verbose_name='编号')
    name = models.CharField(null=True, blank=True, max_length=32, verbose_name='名称')
    quantity = models.FloatField(null=True, blank=True, verbose_name='数量')
    unit = models.SmallIntegerField(null=True, blank=True, choices=UNIT_CHOICES, verbose_name='计量单位')
    price = models.FloatField(null=True, blank=True, verbose_name='总价')
    remain = models.FloatField(null=True, blank=True, verbose_name='剩余')
    remark = models.CharField(null=True, blank=True, max_length=256, verbose_name='备注')
    photo = VersatileImageField(null=True, blank=True, upload_to='photo', ppoi_field='ppoi', verbose_name='照片')

    ppoi = PPOIField(null=True, blank=True, verbose_name='关键点')

    date_produced = models.DateField(null=True, blank=True, verbose_name='生产日期')
    date_expiry = models.DateField(null=True, blank=True, verbose_name='过期时间')

    date_joined = models.DateField(auto_now_add=True, verbose_name='创建日期')
    date_updated = models.DateField(auto_now=True, verbose_name='最近修改')

    warehouse = models.ForeignKey(Warehouse, null=True, blank=True,on_delete=models.SET_NULL, verbose_name='仓库')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='经办')

    def __str__(self):
        return self.name


class HouseExport(models.Model):

    class Meta:
        db_table = 'house_export'
        verbose_name = '出库'
        verbose_name_plural = '出库'

    number = models.CharField(null=True, blank=True, max_length=32, verbose_name='编号')
    name = models.CharField(null=True, blank=True, max_length=32, verbose_name='名称')
    quantity = models.FloatField(null=True, blank=True, verbose_name='数量')
    date_joined = models.DateField(auto_now_add=True, verbose_name='创建日期')

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='经办')

    def __str__(self):
        return self.name

class Linkman(models.Model):

    class Meta:
        db_table = 'linkman'
        verbose_name = '联系人'
        verbose_name_plural = '联系人'

    TYPE_CHOICES = ((0, '客户'), (1, '供应商'))

    name = models.CharField(null=True, blank=True, max_length=32, verbose_name='姓名')
    company = models.CharField(null=True, blank=True, max_length=32, verbose_name='公司')
    telephone = models.CharField(null=True, blank=True, max_length=32, verbose_name='电话')
    type = models.SmallIntegerField(null=True, blank=True, choices=TYPE_CHOICES, verbose_name='类型')

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='经办')

    def __str__(self):
        return self.name


class OrderForm(models.Model):

    class Meta:
        db_table = 'order_form'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    TYPE_CHOICES = ((0, '采购'), (1, '销售'), (2, '技术'))

    number = models.CharField(null=True, blank=True, max_length=32, verbose_name='编号')
    contract = models.CharField(null=True, blank=True, max_length=32, verbose_name='合同')

    type = models.SmallIntegerField(null=True, blank=True, choices=TYPE_CHOICES, verbose_name='类型')

    owner = models.CharField(null=True, blank=True, max_length=32, verbose_name='甲方')
    party = models.CharField(null=True, blank=True, max_length=32, verbose_name='乙方')

    price = models.FloatField(null=True, blank=True, verbose_name='价格')
    count = models.IntegerField(null=True, blank=True, verbose_name='数量')
    special = models.CharField(null=True, blank=True, max_length=32, verbose_name='型号规格')

    remark = models.CharField(null=True, blank=True, max_length=256, verbose_name='备注')
    detail = RichTextUploadingField(null=True, blank=True, verbose_name='详细内容')

    date_demand = models.DateField(null=True, blank=True, verbose_name='需求日期')
    date_joined = models.DateField(auto_now_add=True, verbose_name='创建日期')

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='经办')

    def __str__(self):
        return self.number