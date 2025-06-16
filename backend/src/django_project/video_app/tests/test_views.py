import pytest
import os
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from src.core._shared.tests.authentication.jwt_generator import JwtGenerator
from src.core.castMember.domain.castMember import CastMember
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.video import Video
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

@pytest.fixture
def encoded_token() -> str:
    token_generator = JwtGenerator()
    token_generator.encode_jwt()
    return token_generator.encoded_jwt

@pytest.fixture
def client(encoded_token: str) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {encoded_token}")
    return client

@pytest.fixture(autouse=True, scope="session")
def use_test_public_key() -> None:
    os.environ["AUTH_PUBLIC_KEY"] = os.getenv("TEST_PUBLIC_KEY")

@pytest.mark.django_db
class TestCreateAPI:
    def test_create_video(
        self,
        category_documentary,
        cast_member,
        genre,
        video_repo,
        category_repo,
        genre_repo,
        cast_member_repo,
        client
    ):
        url = "/api/videos/"
        data = {
            "title": "A drama video",
            "description": "A drama video description",
            "launch_year": 2000,
            "duration": 123,
            "published": False,
            "opened": False,
            "rating": "ER",
            "categories": [str(category_documentary.id)],
            "genres": [str(genre.id)],
            "cast_members": [str(cast_member.id)]
        }
        
        response = client.post(url, data=data)
        
        assert response.status_code == 201
        assert response.data["id"] is not None
        
        created_video = video_repo.get_by_id(response.data["id"])
        
        assert created_video.title == "A drama video"
        assert len(created_video.categories) == 1
        assert len(created_video.genres) == 1
        assert len(created_video.cast_members) == 1
        
    def test_fail_create_video_missing_arguments(
        self,
        category_documentary,
        cast_member,
        genre,
        video_repo,
        category_repo,
        genre_repo,
        cast_member_repo,
        client
    ):
        url = "/api/videos/"
        data = {
            "title": "",
            "description": "",
            "launch_year": 2000,
            "duration": 100,
            "published": False,
            "opened": False,
            "rating": "ER",
            "categories": [str(category_documentary.id)],
            "genres": [str(genre.id)],
            "cast_members": [str(cast_member.id)]
        }
        
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {
                                    "title": ["This field may not be blank."],
                                    "description": ["This field may not be blank."]
                                }

@pytest.mark.django_db()   
class TestUpdateAPI:
    def test_update_video_media(
        self,
        video_repo,
        category_repo,
        genre_repo,
        cast_member_repo,
        client
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video_repo.save(video)
        url = f"/api/videos/{video.id}/"
        mock_file = SimpleUploadedFile(
            "test_video.mp4",
            b"fake_mp4_content",
            content_type="video/mp4"
        )
        
        response = client.patch(
            url,
            {"video_file": mock_file},
            format="multipart"
        )
        
        assert response.status_code == 200
        assert video_repo.get_by_id(video.id).video is not None
        
    def test_fail_update_video_media_when_can_not_find_video(
        self,
        video_repo,
        category_repo,
        genre_repo,
        cast_member_repo,
        client
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )

        url = f"/api/videos/{video.id}/"
        mock_file = SimpleUploadedFile(
            "test_video.mp4",
            b"fake_mp4_content",
            content_type="video/mp4"
        )
        
        response = client.patch(
            url,
            {"video_file": mock_file},
            format="multipart"
        )
        
        assert response.status_code == 404