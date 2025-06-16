import uuid
import pytest
from rest_framework.test import APIClient
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core._shared.tests.authentication.jwt_generator import JwtGenerator
from src.core.category.domain.category import Category
import os

@pytest.fixture
def category_movie():
    return Category(name="Movie", description="Movie category")

@pytest.fixture
def category_serie():
    return Category(name="Serie", description="Serie category")

@pytest.fixture
def category_repo() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.fixture
def encoded_token() -> str:
    tokenGenerator = JwtGenerator()
    tokenGenerator.encode_jwt()
    return tokenGenerator.encoded_jwt

@pytest.fixture
def client(encoded_token: str) -> str:
    return APIClient(headers={"Authorization": f"Bearer {encoded_token}"})


@pytest.fixture(autouse=True, scope="session")
def use_test_public_key():
    os.environ["AUTH_PUBLIC_KEY"] = os.getenv("TEST_PUBLIC_KEY")
    
@pytest.mark.django_db
class TestListCategoryAPI:
    def test_list_categories(
            self,
            category_movie: Category,
            category_serie: Category,
            category_repo: DjangoORMCategoryRepository,
            client: APIClient
        ) -> None:        
        category_repo.save(category_movie)
        category_repo.save(category_serie)
        url = "/api/categories/?page=1&order=name"
        response = client.get(url)
        
        expected_data =  [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active
            },{
                "id": str(category_serie.id),
                "name": category_serie.name,
                "description": category_serie.description,
                "is_active": category_serie.is_active
            }
        ]
        
        assert response.status_code == 200
        assert len(response.data["data"]) == 2
        assert response.data["data"] == expected_data
        assert response.data["meta"] == {
            "current_page": 1,
            "per_page": 2,
            "total": 2
        }

@pytest.mark.django_db
class TestRetrieveAPI:
    def test_return_error_when_id_is_invalid(
            self,
            client: APIClient) -> None: 
        url = "/api/categories/123/"
        response = client.get(url)
        
        assert response.status_code == 400
        
    def test_return_category_when_exists(
            self,
            category_movie: Category,
            category_serie: Category,
            category_repo: DjangoORMCategoryRepository, 
            client: APIClient
        ) -> None:        
        category_repo.save(category_movie)
        category_repo.save(category_serie)
        url = f"/api/categories/{category_movie.id}/"
        response = client.get(url)
        
        expected_data = {
            "id": str(category_movie.id),
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": category_movie.is_active
        }
        
        assert response.status_code == 200
        assert response.data["data"] == expected_data
    
    def test_return_error_when_id_is_not_found(
        self,
        client: APIClient) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = client.get(url)
        
        assert response.status_code == 404
        
@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid(
        self,
        client: APIClient) -> None: 
        url = "/api/categories/"
        response = client.post(
            url,
            data={"name": "", "description": "Movie category"}
        )
        
        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}
        
    def test_when_payload_is_valid(
            self,
            category_repo: DjangoORMCategoryRepository,
            client: APIClient
        ) -> None:        
        url = f"/api/categories/"
        response = client.post(
            url,
            data = {"name": "Movie", "description": "Movie category"}
            )
        
        assert response.status_code == 201
        assert category_repo.list() == [Category(
            id=uuid.UUID(response.data["id"]),
            name = "Movie",
            description = "Movie category"
        )]
    
    def test_return_error_when_id_is_invalid(
            self,
            client: APIClient) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = client.get(url)
        
        assert response.status_code == 404
        
@pytest.mark.django_db
class TestUpdateAPI:
    def test_return_error_when_upload_is_invalid(
        self,
        client: APIClient) -> None: 
        url = "/api/categories/123/"
        response = client.put(
            url,
            data={"name": "", "description": "Movie category"})
        
        assert response.status_code == 400
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."]
        }
        
    def test_update_successfully_when_exists(
            self,
            category_movie: Category,
            category_repo: DjangoORMCategoryRepository,
            client: APIClient
        ) -> None:        
        category_repo.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = client.put(
            url,
            data={"name": "Serie", "description": "Serie category", "is_active": True}
            )
        
        assert response.status_code == 204
        assert category_repo.list()[0].id == category_movie.id
        assert category_repo.list()[0].name == "Serie"
        assert category_repo.list()[0].description == "Serie category"
        assert category_repo.list()[0].is_active == True
    
    def test_return_error_when_category_is_not_found(
        self,
        client: APIClient) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = client.put(
            url,
            data={"name": "Serie", "description": "Serie category", "is_active": True}
        )
        
        assert response.status_code == 404

@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_return_error_when_upload_is_invalid(
        self,
        client: APIClient) -> None: 
        url = "/api/categories/123/"
        response = client.patch(
            url,
            data={"description": "Movie category"})
        
        assert response.status_code == 400
        assert response.data == {
            "id": ["Must be a valid UUID."]
        }
        
    def test_partially_update_successfully_when_exists(
            self,
            category_movie: Category,
            category_repo: DjangoORMCategoryRepository,
            client: APIClient   
        ) -> None:        
        category_repo.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = client.patch(
            url,
            data={"description": "Serie category"}
            )
        
        assert response.status_code == 204
        assert category_repo.list()[0].id == category_movie.id
        assert category_repo.list()[0].name == category_movie.name
        assert category_repo.list()[0].description == "Serie category"
        assert category_repo.list()[0].is_active == True
    
    def test_return_error_when_category_is_not_found(
        self,
        client: APIClient) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = client.patch(
            url,
            data={"name": "Serie"}
        )
        
        assert response.status_code == 404        

@pytest.mark.django_db
class TestDeleteAPI:
    def test_return_error_when_id_is_invalid(
        self,
        client: APIClient) -> None: 
        url = "/api/categories/123/"
        response = client.delete(url)
        
        assert response.status_code == 400
        
    def test_return_category_when_exists(
            self,
            category_movie: Category,
            category_repo: DjangoORMCategoryRepository,
            client: APIClient   
        ) -> None:        
        category_repo.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = client.delete(url)
        
        assert response.status_code == 200
        assert len(category_repo.list()) == 0
    
    def test_return_error_when_category_is_not_found(
        self,
        client: APIClient) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = client.delete(url)
        
        assert response.status_code == 404
    