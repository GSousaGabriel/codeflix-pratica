from rest_framework import serializers

from django_project.video_app.models import Video

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    
    def to_representation(self, value):
        return list(super().to_representation(value))

class CreateVideoInputSerializer(serializers.ModelSerializer):
    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())
    
    class Meta:
        """Meta"""

        model = Video
        fields = "__all__"

class CreateVideoOutputSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = Video
        fields = ["id"]