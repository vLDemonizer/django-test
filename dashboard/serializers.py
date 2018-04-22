from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'cod')


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductType
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = models.Store
        fields = ('name', 'owner', 'cod')
        depth = 1
        

class SaleSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    
    class Meta:
        model = models.Sale
        fields = (
            'product_type', 'client', 'date', 'amount',
            'total_local', 'total_usd', 'store'
        )
