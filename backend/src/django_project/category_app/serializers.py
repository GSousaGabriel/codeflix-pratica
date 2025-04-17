from rest_framework import serializers
from django_project.category_app.models import Category

class  CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = Category
        fields = "__all__"
        
class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()
        
class  ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()
    
    def to_representation(self, instance):
        return {
                "data": CategoryResponseSerializer(instance.data, many=True).data,
                "meta": {
                    "current_page": instance.meta.current_page,
                    "per_page": instance.meta.per_page,
                    "total": instance.meta.total
                }
        }

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
