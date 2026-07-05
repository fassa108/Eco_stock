from rest_framework.serializers import ModelSerializer

from stock.models import Product, Warehouse

class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id','name', 'localisation', 'capacity']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'quantity', 'expiration_date', 'status','warehouse']
    