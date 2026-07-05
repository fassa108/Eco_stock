from django.contrib import admin

from stock.models import Product, Warehouse
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    class Meta:
        model = Warehouse
        fields = ('id', 'name','location','capacity')
        readonly_fields = ('id',)
        search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta :
        model = Product
        fields = ('id','name', 'quantity', 'expiration_date','status')
        readonly_fields= ('id',)
        search_fields = ('name',)
        
