from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.core._shared.listEntity import ListPaginationInput
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.list_genre import ListGenre
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.genre_app.seriealizers import CreateGenreInputSerializer, CreateGenreOutputSerializer, DeleteGenreInputSerializer, ListGenreOutputSerializer, UpdateGenreInputSerializer
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.permissions import IsAuthenticated

class GenreViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request: Request)-> Response:
        page = request.query_params.get("page", 1)
        order = request.query_params.get("order", "id")
        
        input = ListPaginationInput(order, page)
        use_case = ListGenre(DjangoORMGenreRepository())
        output = use_case.execute(input)
        
        serializer = ListGenreOutputSerializer(output)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
        
    def create(self, request: Request)->Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(DjangoORMGenreRepository(), DjangoORMCategoryRepository())
       
        try:
            output = use_case.execute(input)
            final_output = CreateGenreOutputSerializer(output)
        except(InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(err)})
        
        return Response(status=status.HTTP_201_CREATED, data=final_output.data)
    
    def update(self, request: Request, pk=None)->Response:
        serializer = UpdateGenreInputSerializer(
            data = {**request.data, "id": pk},
        )
        serializer.is_valid(raise_exception=True)
        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(DjangoORMGenreRepository(), DjangoORMCategoryRepository())
        
        try:
            use_case.execute(input)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RelatedCategoriesNotFound as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(err)})
        except GenreNotFound as err:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": str(err)})
            
        
    def destroy(self, request: Request, pk=None)->Response:
        serializer = DeleteGenreInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        input = DeleteGenre.Input(**serializer.validated_data)
        use_case = DeleteGenre(DjangoORMGenreRepository())
          
        try:
            use_case.execute(input)
            return Response(status=status.HTTP_200_OK)
        except GenreNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
            