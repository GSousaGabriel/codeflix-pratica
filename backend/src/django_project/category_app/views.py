from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.category.application.use_cases.list_category import ListCategory
from django_project.category_app.repository import DjangoORMCategoryRepository
from core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core._shared.listEntity import ListPaginationInput
from src.core.category.application.use_cases.delete_repository import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from django_project.category_app.serializers import CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, DeleteCategoryRequestSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategoryRequestSerializer
from src.django_project.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request: Request)-> Response:
        order_by = request.query_params.get("order_by", "name")
        page = request.query_params.get("page", 1)
        
        input = ListPaginationInput(order_by, page)
        use_case = ListCategory(DjangoORMCategoryRepository())
        output = use_case.execute(input)
        
        serializer = ListCategoryResponseSerializer(output)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def retrieve(self, request: Request, pk=None)-> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        input = GetCategoryRequest(**serializer.validated_data)
        use_case = GetCategory(DjangoORMCategoryRepository())
          
        try:
            output = use_case.execute(input)
            response_serializer = RetrieveCategoryResponseSerializer(output)
            
            return Response(status=status.HTTP_200_OK, data=response_serializer.data)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request: Request)->Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(DjangoORMCategoryRepository())
        output = use_case.execute(input)
        final_output = CreateCategoryResponseSerializer(output)
        
        return Response(status=status.HTTP_201_CREATED, data=final_output.data)
    
    def update(self, request: Request, pk=None)->Response:
        serializer = UpdateCategoryRequestSerializer(
            data = {**request.data, "id": pk},
        )
        serializer.is_valid(raise_exception=True)
        
        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(DjangoORMCategoryRepository())
        
        try:
            use_case.execute(input)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request: Request, pk=None)->Response:
        serializer = UpdateCategoryRequestSerializer(
            data = {**request.data, "id": pk},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        
        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(DjangoORMCategoryRepository())
        
        try:
            use_case.execute(input)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request: Request, pk=None)->Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        input = DeleteCategoryRequest(**serializer.validated_data)
        use_case = DeleteCategory(DjangoORMCategoryRepository())
          
        try:
            use_case.execute(input)
            return Response(status=status.HTTP_200_OK)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
            