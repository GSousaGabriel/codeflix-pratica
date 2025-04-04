from rest_framework import serializers
from django_project.category_app.models import Category

class  CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = Category
        fields = "__all__"
        
class  ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)

class  RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class  RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source="*")

class  CreateCategoryRequestSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        """Meta"""

        model = Category
        exclude = ["id"]
        
class CreateCategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = Category
        fields = ["id"] 
        
class UpdateCategoryRequestSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    is_active = serializers.BooleanField()
    
    class Meta:
        """Meta"""

        model = Category
        fields = "__all__"

class  DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
