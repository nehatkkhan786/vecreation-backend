from django.contrib import admin
from .models import Category, ProductImages, Product, Order, Shipping, OrderItem, Contact

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class ShippingInline(admin.TabularInline):
    model= Shipping
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customId', 'totalPrice', 'status', 'isPaid', 'transactionId') 
    search_fields = ('customId', )
    list_filter = ('status', 'isPaid')

    inlines = [OrderItemInline, ShippingInline]

class ContactAdmin(admin.ModelAdmin):
    list_display= ('supportId', 'name', 'email', 'phone',)
    search_fields = ('supportId', )
    list_filter = ('created_at','status')
    



admin.site.register(Category)
admin.site.register(ProductImages)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shipping)
admin.site.register(OrderItem)
admin.site.register(Contact, ContactAdmin)
