from django.contrib import admin
from django.utils.html import format_html

from app.models import (
    Warehouse, HouseImport, HouseExport, Linkman, OrderForm
)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):

    list_display_links = ('id', 'name')
    list_display = ('id', 'name', 'area', 'has_empty')


@admin.register(HouseImport)
class HouseImportAdmin(admin.ModelAdmin):

    search_fields = ('number', 'name')
    readonly_fields = ('date_joined', 'date_updated')
    list_filter = (
        'unit', 'date_expiry', 'date_joined', 'date_updated'
    )
    list_display_links = ('id', 'number', 'name')
    list_display = (
        'id', 'number', 'name', 'quantity', 'unit', 'price', 'remain', 'user',
        'date_produced', 'date_expiry', 'photo_preview'
    )

    def photo_preview(self, obj):
        return format_html('<img src="{}">', obj.photo.thumbnail['300x300'].url)
    photo_preview.short_description = '预览'

    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            return ['user']
        return super(HouseImportAdmin, self).get_exclude(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser or request.user.id == obj.user.id:
            return super(HouseImportAdmin, self).get_readonly_fields(request, obj)
        return (
            'number', 'name', 'quantity', 'unit', 'price', 'remain',
            'remark', 'photo', 'ppoi', 'date_produced', 'date_expiry'
        )

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super(HouseImportAdmin, self).save_model(request, obj, form, change)


@admin.register(HouseExport)
class HouseExportAdmin(admin.ModelAdmin):
    pass


@admin.register(Linkman)
class LinkmanAdmin(admin.ModelAdmin):

    list_filter = ('type', )
    list_display_links = ('id', 'name')
    list_display = ('id', 'name', 'company', 'telephone', 'type', 'user')

    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            return ['id', 'user']
        return super(LinkmanAdmin, self).get_exclude(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user.id == obj.user.id:
            return super(LinkmanAdmin, self).get_readonly_fields(request, obj)
        return ['name', 'company', 'telephone', 'type']

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super(LinkmanAdmin, self).save_model(request, obj, form, change)


@admin.register(OrderForm)
class OrderFormAdmin(admin.ModelAdmin):

    search_fields = ('contract', 'owner', 'party', 'people')
    list_filter = ('type', 'date_demand', 'date_joined')
    list_display_links = ('number', 'contract')
    list_display = (
        'number', 'contract', 'type', 'owner', 'party', 'price', 'count', 'user',
        'date_demand', 'date_joined'
    )

    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            if request.user.id == obj.user.id:
                return ['user']
            else:
                return ['user', 'detail']
        return super(OrderFormAdmin, self).get_exclude(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user.id == obj.user.id:
            return super(OrderFormAdmin, self).get_readonly_fields(request, obj)
        return (
            'number', 'contract', 'type', 'owner', 'party', 'price', 'count',
            'special', 'remark', 'date_demand'
        )

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super(OrderFormAdmin, self).save_model(request, obj, form, change)