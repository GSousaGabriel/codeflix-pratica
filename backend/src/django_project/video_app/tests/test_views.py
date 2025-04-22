import pytest
from rest_framework.test import APIClient

from src.core.castMember.domain.castMember import CastMember
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.castMember_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository

@pytest.fixture
def category_documentary() -> Category:
    return Category("Documentary", "Documentary description")

@pytest.fixture
def cast_member() -> CastMember:
    return CastMember("John Doe", "ACTOR")

@pytest.fixture
def genre() -> Genre:
    return Genre("Drama")

@pytest.fixture
def genre_repo(genre) -> DjangoORMGenreRepository:
    repo = DjangoORMGenreRepository()
    repo.save(genre)
    return repo

@pytest.fixture
def category_repo(category_documentary) -> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    repo.save(category_documentary)
    return repo

@pytest.fixture
def cast_member_repo(cast_member) -> DjangoORMCastMemberRepository:
    repo = DjangoORMCastMemberRepository()
    repo.save(cast_member)
    return repo

@pytest.fixture
def video_repo() -> DjangoORMVideoRepository:
    return DjangoORMVideoRepository()

@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre(
        self,
        category_documentary,
        cast_member,
        genre,
        video_repo,
        category_repo,
        genre_repo,
        cast_member_repo
    ):
        url = "/api/videos/"
        data = {
            "title": "A drama video",
            "description": "A drama video description",
            "launch_year": 2000,
            "duration": 123,
            "published": False,
            "rating": "ER",
            "categories_ids": [str(category_documentary.id)],
            "genres_ids": [str(genre.id)],
            "cast_members_ids": [str(cast_member.id)]
        }
        
        response = APIClient().post(url, data=data)
        
        assert response.status_code == 201
        assert response.data["id"] is not None
        
        created_video = video_repo.get_by_id(response.data["id"])
        
        assert created_video.title == "A drama video"
        assert created_video.categories_ids.count() == 1
        assert created_video.genres_ids.count() == 1
        assert created_video.cast_members_ids.count() == 1
        
    def test_fail_create_genre_missing_arguments(
        self,
        category_documentary,
        cast_member,
        genre,
        video_repo,
        category_repo,
        genre_repo,
        cast_member_repo
    ):
        url = "/api/videos/"
        data = {
            "title": "",
            "description": "",
            "launch_year": 2000,
            "duration": 100,
            "published": False,
            "rating": "ER",
            "categories_ids": [str(category_documentary.id)],
            "genres_ids": [str(genre.id)],
            "cast_members_ids": [str(cast_member.id)]
        }
        
        response = APIClient().post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {
                                    "title": ["This field may not be blank."],
                                    "description": ["This field may not be blank."]
                                }