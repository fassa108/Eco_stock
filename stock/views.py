from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework  import status

from django.shortcuts import get_object_or_404

from stock.models import Product, Warehouse
from stock.serializers import ProductSerializer, WarehouseSerializer



class WarehouseModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.all()

    @action(detail = True, methods = ['get'])
    def audit(self, request, pk = None):
        warehouse = self.get_object()
        product_count = warehouse.products.count()

        return Response({'nb_product' : product_count},status = status.HTTP_200_OK)
    



class ProductModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
    
    @action(detail=True, methods=['post'])
    def move(self, request, pk):
        product = self.get_object()

        if product.status == 'perime':
            return Response(
                {'error': 'Impossible de déplacer un produit périmé'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data
        warehouse_id = data.get('warehouse', None)

        if warehouse_id is None:
            return Response(
                {'error': 'le champ warehouse est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        target_warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        aggregation_result = target_warehouse.products.aggregate(Sum('quantity'))
        current_total_quantity = aggregation_result['quantity__sum'] or 0

        if current_total_quantity + product.quantity > target_warehouse.capacity:
            return Response(
                {'error': "Capacité de l'entrepôt cible dépassée"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.warehouse = target_warehouse
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
