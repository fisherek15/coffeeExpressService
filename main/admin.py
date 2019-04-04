from django.contrib import admin
from .models import Customer, Order, Comment, Device


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'acceptance_date')


@admin.register(Comment)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('author', 'published_date', 'order')


@admin.register(Device)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('producer', 'type', 'model', 'id_number')

