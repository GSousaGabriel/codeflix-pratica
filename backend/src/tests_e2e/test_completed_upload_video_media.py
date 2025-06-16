
import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from src.core._shared.tests.authentication.jwt_generator import JwtGenerator
import os

@pytest.fixture
def encoded_token() -> str:
    tokenGenerator = JwtGenerator()
    tokenGenerator.encode_jwt()
    return tokenGenerator.encoded_jwt

@pytest.fixture(autouse=True, scope="session")
def use_test_public_key():
    os.environ["AUTH_PUBLIC_KEY"] = os.getenv("TEST_PUBLIC_KEY")

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_edit_patch_and_delete_category(self, encoded_token)->None:
        api_client = APIClient()
        
        create_category_response = api_client.post(
            "/api/categories/",
            headers={"Authorization": f"Bearer {encoded_token}"},
            data = {"name": "Movie", "description": "Movie category"},
        )
        assert create_category_response.status_code == 201
        
        create_genre_response = api_client.post(
            "/api/genres/",
            headers={"Authorization": f"Bearer {encoded_token}"},
            data = {"name": "Drama", "categories_ids": [create_category_response.data["id"]]}
        )
        assert create_genre_response.status_code == 201
        
        create_cast_member_response = api_client.post(
            "/api/cast_members/",
            headers={"Authorization": f"Bearer {encoded_token}"},
            data = {"name": "Movie", "type": "ACTOR"}
        )
        assert create_cast_member_response.status_code == 201
        
        data_video = {
            "title": "A drama video",
            "description": "A drama video description",
            "launch_year": 2000,
            "duration": 123,
            "published": False,
            "opened": False,
            "rating": "ER",
            "categories": [create_category_response.data["id"]],
            "genres": [create_genre_response.data["id"]],
            "cast_members": [create_cast_member_response.data["id"]]
        }
        
        create_video_response = api_client.post("/api/videos/",
            headers={"Authorization": f"Bearer {encoded_token}"},
            data=data_video)
        
        assert create_video_response.status_code == 201
        
        
        url = f"/api/videos/{create_video_response.data["id"]}/"
        mock_file = SimpleUploadedFile(
            "test_video.mp4",
            b"fake_mp4_content",
            content_type="video/mp4"
        )
        
        updated_video_response = APIClient().patch(
            url,
            {"video_file": mock_file},
            headers={"Authorization": f"Bearer {encoded_token}"},
            format="multipart"
        )
        
        assert updated_video_response.status_code == 200