from rest_framework import serializers

from django_project.castMember_app.models import CastMember

class CastMemberOutputSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = CastMember
        fields = "__all__"
        
class ListCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(many=True)

class CreateCastMemberInputSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = CastMember
        fields = "__all__"

class CreateCastMemberOutputSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta"""

        model = CastMember
        fields = ["id"]
        
class UpdateCastMemberInputSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    
    class Meta:
        """Meta"""

        model = CastMember
        fields = "__all__"
        
class DeleteCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()