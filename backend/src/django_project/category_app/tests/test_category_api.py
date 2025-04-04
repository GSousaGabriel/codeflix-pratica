import uuid
import pytest
from rest_framework.test import APIClient
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category

@pytest.fixture
def category_movie():
    return Category(name="Movie", description="Movie category")

@pytest.fixture
def category_serie():
    return Category(name="Serie", description="Serie category")

@pytest.fixture
def category_repo() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListCategoryAPI:
    def test_list_categories(
            self,
            category_movie: Category,
            category_serie: Category,
            category_repo: DjangoORMCategoryRepository   
        ) -> None:        
        category_repo.save(category_movie)
        category_repo.save(category_serie)
        url = "/api/categories/"
        response = APIClient().get(url)
        
        expected_data =  {
            "data": [
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
        }
        
        assert response.status_code == 200
        assert len(response.data["data"]) == 2
        assert response.data == expected_data

@pytest.mark.django_db
class TestRetrieveAPI:
    def test_return_error_when_id_is_invalid(self) -> None: 
        url = "/api/categories/123/"
        response = APIClient().get(url)
        
        assert response.status_code == 400
        
    def test_return_category_when_exists(
            self,
            category_movie: Category,
            category_serie: Category,
            category_repo: DjangoORMCategoryRepository   
        ) -> None:        
        category_repo.save(category_movie)
        category_repo.save(category_serie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().get(url)
        
        expected_data = {
            "id": str(category_movie.id),
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": category_movie.is_active
        }
        
        assert response.status_code == 200
        assert response.data["data"] == expected_data
    
    def test_return_error_when_id_is_not_found(self) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)
        
        assert response.status_code == 404
        
@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid(self) -> None: 
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={"name": "", "description": "Movie category"}
        )
        
        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}
        
    def test_when_payload_is_valid(
            self,
            category_repo: DjangoORMCategoryRepository   
        ) -> None:        
        url = f"/api/categories/"
        response = APIClient().post(
            url,
            data = {"name": "Movie", "description": "Movie category"}
            )
        
        assert response.status_code == 201
        assert category_repo.list() == [Category(
            id=uuid.UUID(response.data["id"]),
            name = "Movie",
            description = "Movie category"
        )]
    
    def test_return_error_when_id_is_invalid(self) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)
        
        assert response.status_code == 404
        
@pytest.mark.django_db
class TestUpdateAPI:
    def test_return_error_when_upload_is_invalid(self) -> None: 
        url = "/api/categories/123/"
        response = APIClient().put(
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
            category_repo: DjangoORMCategoryRepository   
        ) -> None:        
        category_repo.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            url,
            data={"name": "Serie", "description": "Serie category", "is_active": True}
            )
        
        assert response.status_code == 204
        assert category_repo.list()[0].id == category_movie.id
        assert category_repo.list()[0].name == "Serie"
        assert category_repo.list()[0].description == "Serie category"
        assert category_repo.list()[0].is_active == True
    
    def test_return_error_when_category_is_not_found(self) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().put(
            url,
            data={"name": "Serie", "description": "Serie category", "is_active": True}
        )
        
        assert response.status_code == 404

@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_return_error_when_upload_is_invalid(self) -> None: 
        url = "/api/categories/123/"
        response = APIClient().patch(
            url,
            data={"description": "Movie category"})
        
        assert response.status_code == 400
        assert response.data == {
            "id": ["Must be a valid UUID."]
        }
        
    def test_partially_update_successfully_when_exists(
            self,
            category_movie: Category,
            category_repo: DjangoORMCategoryRepository   
        ) -> None:        
        category_repo.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={"description": "Serie category"}
            )
        
        assert response.status_code == 204
        assert category_repo.list()[0].id == category_movie.id
        assert category_repo.list()[0].name == category_movie.name
        assert category_repo.list()[0].description == "Serie category"
        assert category_repo.list()[0].is_active == True
    
    def test_return_error_when_category_is_not_found(self) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().patch(
            url,
            data={"name": "Serie"}
        )
        
        assert response.status_code == 404        

@pytest.mark.django_db
class TestDeleteAPI:
    def test_return_error_when_id_is_invalid(self) -> None: 
        url = "/api/categories/123/"
        response = APIClient().delete(url)
        
        assert response.status_code == 400
        
    def test_return_category_when_exists(
            self,
            category_movie: Category,
            category_repo: DjangoORMCategoryRepository   
        ) -> None:        
        category_repo.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)
        
        assert response.status_code == 200
        assert len(category_repo.list()) == 0
    
    def test_return_error_when_category_is_not_found(self) -> None: 
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().delete(url)
        
        assert response.status_code == 404
    