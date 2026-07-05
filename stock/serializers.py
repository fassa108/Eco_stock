from datetime import date

from rest_framework.serializers import ModelSerializer, ValidationError

from stock.models import Product, Warehouse

class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id','name', 'localisation', 'capacity']

    def validate_capacity(self,value):
        if value <= 0:
            raise ValidationError("La capacité doit etre un entier positif non nul")
        return value
    def validate_name(self, value):
        if value.isnumeric():
            raise ValidationError("Le nom doit contenir au moins une lettre alphabetique")
        return value

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'quantity', 'expiration_date', 'status','warehouse']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("La quantité doit être un entier positif non nul")
        return value

    def validate_name(self, value):
        if value.isnumeric():
            raise ValidationError("Le nom doit contenir au moins une lettre alphabétique")
        return value

    def validate_expiration_date(self, value):
        if self.instance is None and value < date.today():
            raise ValidationError("La date d'expiration ne peut pas être dans le passé")
        return value