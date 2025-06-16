import uuid
import pytest
import os
from rest_framework.test import APIClient
from src.core._shared.tests.authentication.jwt_generator import JwtGenerator
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository

@pytest.fixture
def category_documentary()-> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_movie()-> Category:
    return Category(name="Movie")

@pytest.fixture
def encoded_token() -> str:
    token_generator = JwtGenerator()
    token_generator.encode_jwt()
    return token_generator.encoded_jwt

@pytest.fixture
def client(encoded_token: str) -> APIClient:
    return APIClient(headers={"Authorization": f"Bearer {encoded_token}"})

@pytest.fixture(autouse=True, scope="session")
def use_test_public_key():
    os.environ["AUTH_PUBLIC_KEY"] = os.getenv("TEST_PUBLIC_KEY")

@pytest.fixture
def category_repo(category_documentary, category_movie)-> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    repo.save(category_documentary)
    repo.save(category_movie)
    return repo

@pytest.fixture
def genre_drama(category_documentary, category_movie)-> Genre:
    return Genre(name="Drama", is_active=True, categories_ids={category_documentary.id, category_movie.id})

@pytest.fixture
def genre_romance()-> Genre:
    return Genre(name="Romance", is_active=True, categories_ids=set())

@pytest.fixture
def genre_repo() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.mark.django_db
class TestListAPI:
    def test_list_genres(
        self,
        category_documentary,
        category_movie,
        category_repo,
        genre_repo,
        genre_drama,
        genre_romance, 
        client
    ):
        genre_repo.save(genre_romance)
        genre_repo.save(genre_drama)
        
        url = "/api/genres/?order=name"
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.data["data"][0]["id"] == str(genre_drama.id)
        assert response.data["data"][0]["name"] == "Drama"
        assert response.data["data"][0]["is_active"] is True
        assert set(response.data["data"][0]["categories_ids"]) == {
            str(category_documentary.id),
            str(category_movie.id),
        }
        assert response.data["data"][1]["id"] == str(genre_romance.id)
        assert response.data["data"][1]["name"] == "Romance"
        assert response.data["data"][1]["is_active"] is True
        assert response.data["data"][1]["categories_ids"] == []
        assert response.data["meta"] == {
            "current_page": 1,
            "per_page": 2,
            "total": 2
        }
        
@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre(
        self,
        category_documentary,
        category_movie,
        category_repo,
        genre_repo, 
        client
    ):
        url = "/api/genres/"
        data = {
            "name": "Drama",
            "categories_ids": [str(category_documentary.id), str(category_movie.id)],
        }
        
        response = client.post(url, data=data)
        
        assert response.status_code == 201
        assert response.data["id"] is not None
        
        created_genre = genre_repo.get_by_id(response.data["id"])
        
        assert created_genre.name == "Drama"
        assert created_genre.categories_ids == {
            category_documentary.id,
            category_movie.id,
        }
        
    def test_do_not_create_genre_invalid_category(
        self,
        category_repo, 
        client
    ):
        url = "/api/genres/"
        category_id = uuid.uuid4()
        data = {
            "name": "Drama",
            "categories_ids": [str(category_id)],
        }
        
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data["error"] is not None
        
    def test_do_not_create_genre_invalid_genre_data(
        self,
        category_documentary,
        category_repo, 
        client
    ):
        url = "/api/genres/"
        data = {
            "name": "",
            "categories_ids": [str(category_documentary.id)],
        }
        
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}
        
@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_genre(
        self,
        category_repo,
        genre_drama,
        genre_repo, 
        client
    ):
        genre_repo.save(genre_drama)
        url = f"/api/genres/{genre_drama.id}/"
        
        response = client.delete(url)
        
        assert response.status_code == 200
        
        genre = genre_repo.get_by_id(genre_drama.id)
        
        assert genre is None
        
    def test_delete_fail_genre_not_found(
        self,
        client):
        url = f"/api/genres/{uuid.uuid4()}/"
        
        response = client.delete(url)
        
        assert response.status_code == 404
        
    def test_delete_fail_genre_id_not_valid(
        self,
        client):
        url = "/api/genres/1/"
        
        response = client.delete(url)
        
        assert response.status_code == 400
        
@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_movie,
        category_repo,
        genre_drama,
        genre_repo,
        client
    ):
        genre_repo.save(genre_drama)
              
        url = f"/api/genres/{genre_drama.id}/"
        data = {
            "name": "Action",
            "is_active": False,
            "categories_ids": [str(category_movie.id)],
        }
        
        response = client.put(url, data=data)
        
        assert response.status_code == 204
        
        updated_genre = genre_repo.get_by_id(genre_drama.id)
        
        assert updated_genre.name == "Action"
        assert updated_genre.is_active == False
        assert updated_genre.categories_ids == {
            category_movie.id
        }
        
    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_repo,
        genre_drama,
        client
    ):
        genre_repo.save(genre_drama)
        url = f"/api/genres/{genre_drama.id}/"
        data = {
            "name": "",
        }
        
        response = client.put(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
            "categories_ids": ["This field is required."]
            }
        
    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repo,
        genre_drama,
        genre_repo,
        client
    ):
        genre_repo.save(genre_drama)
        url = f"/api/genres/{genre_drama.id}/"
        data = {
            "name": "Action",
            "is_active": True,
            "categories_ids": [str(uuid.uuid4())],
        }
        
        response = client.put(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"error": "Some of the categories could no be found!"}
        
    def test_when_genre_does_not_exist_then_return_404(
        self,
        client):
        test_id = uuid.uuid4()
        url = f"/api/genres/{test_id}/"
        data = {
            "name": "Action",
            "is_active": True,
            "categories_ids": [str(uuid.uuid4())],
        }
        
        response = client.put(url, data=data)
        
        assert response.status_code == 404
        assert response.data == {"error": f"Genre with id {test_id} was not found!"}
        
    def test_when_id_is_not_valid_uuid(
        self,
        client):
        url = "/api/genres/1/"
        data = {
            "name": "Action",
            "is_active": True,
            "categories_ids": [str(uuid.uuid4())],
        }
        
        response = client.put(url, data=data)
        
        assert response.status_code == 400