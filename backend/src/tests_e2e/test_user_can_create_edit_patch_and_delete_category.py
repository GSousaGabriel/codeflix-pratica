
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_edit_patch_and_delete_category(self)->None:
        api_client = APIClient()
        
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}
        
        create_response = api_client.post(
            "/api/categories/",
            data = {"name": "Movie", "description": "Movie category"}
        )
        assert create_response.status_code == 201
        
        created_category_id= create_response.data["id"]
        
        get_response = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response.data["data"] == {
            "id": str(created_category_id),
            "name": "Movie",
            "description": "Movie category",
            "is_active": True
        }
        assert get_response.status_code == 200
        
        update_response = api_client.put(
            f"/api/categories/{created_category_id}/",
            data = {
            "name": "Serie",
            "description": "Serie category",
            "is_active": False
        }
        )
        assert update_response.status_code == 204
        
        patch_response = api_client.patch(
            f"/api/categories/{created_category_id}/",
            data = {
            "is_active": True
        }
        )
        assert patch_response.status_code == 204
        
        get_response_updated = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response_updated.data["data"] == {
            "id": str(created_category_id),
            "name": "Serie",
            "description": "Serie category",
            "is_active": True
        }
        assert get_response_updated.status_code == 200
        
        delete_response = api_client.delete(f"/api/categories/{created_category_id}/")
        assert delete_response.status_code == 200
        
        
        