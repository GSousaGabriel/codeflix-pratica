from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request

from src.core.castMember.application.use_cases.create_castMember import CreateCastMember
from src.core.castMember.application.use_cases.delete_castMember import DeleteCastMember
from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.castMember.application.use_cases.list_castMember import ListCastMember
from django_project.castMember_app.repository import DjangoORMCastMemberRepository
from django_project.castMember_app.serializers import CreateCastMemberInputSerializer, CreateCastMemberOutputSerializer, ListCastMemberOutputSerializer, DeleteCastMemberInputSerializer, UpdateCastMemberInputSerializer
from src.core.castMember.application.use_cases.update_castMember import UpdateCastMember

class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCastMember(DjangoORMCastMemberRepository())
        response = use_case.execute()
        serializer = ListCastMemberOutputSerializer(response)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateCastMember.Input(**serializer.validated_data)
        use_case = CreateCastMember(DjangoORMCastMemberRepository())
        
        try:
            output = use_case.execute(input)
            final_output = CreateCastMemberOutputSerializer(output)
        except InvalidCastMember as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(err)})
        
        return Response(status=status.HTTP_201_CREATED, data=final_output.data)

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCastMemberInputSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)
        
        input = UpdateCastMember.Input(**serializer.validated_data)
        
        try:
            use_case = UpdateCastMember(DjangoORMCastMemberRepository())
            use_case.execute(input)
        except InvalidCastMember as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(err)})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk=None) -> Response:
        seriealizer = DeleteCastMemberInputSerializer(data={"id": pk})
        seriealizer.is_valid(raise_exception=True)
        
        input = DeleteCastMember.Input(**seriealizer.validated_data)
        use_case = DeleteCastMember(DjangoORMCastMemberRepository())
        
        try:
            use_case.execute(input)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CastMemberNotFound as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(err)})