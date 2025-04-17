from rest_framework import serializers

from django_project.genre_app.models import Genre

class GenreOutputSerializer(serializers.ModelSerializer):
    categories_ids = serializers.ListField(child=serializers.UUIDField())
    
    class Meta:
        """Meta"""

        model = Genre
        fields = "__all__"

class ListGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)
    
    def to_representation(self, instance):
        return {
            "data": GenreOutputSerializer(instance.data, many=True).data,
            "meta":{
            "current_page": instance.meta.current_page,
            "per_page": instance.meta.per_page,
            "total": instance.meta.total
            }        
        }
    
class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    
    def to_representation(self, value):
        return list(super().to_representation(value))

class CreateGenreInputSerializer(serializers.ModelSerializer):
    categories_ids = SetField(child=serializers.UUIDField())
    
    class Meta:
        """Meta"""

        model = Genre
        fields = "__all__"

class CreateGenreOutputSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = Genre
        fields = ["id"]

class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdateGenreInputSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    is_active = serializers.BooleanField()
    categories_ids = SetField(child=serializers.UUIDField())
    
    class Meta:
        """Meta"""

        model = Genre
        fields = "__all__"
