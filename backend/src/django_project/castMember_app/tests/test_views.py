import uuid
import pytest
from rest_framework.test import APIClient

from src.core.castMember.domain.castMember import CastMember
from django_project.castMember_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def castMember() -> CastMember:
    return CastMember(name="Test CastMember", type="ACTOR")
    
@pytest.fixture
def castMember_repo() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()

@pytest.mark.django_db
class TestGetAllCastMember:
    def test_call_api_get_all(
            self,
            castMember_repo,
            castMember
        ):
        
        castMember_repo.save(castMember)
        url = "/api/cast_members/"
        response = APIClient().get(url)
        
        assert response.status_code == 200
        assert len(response.data["data"]) == 1
        
@pytest.mark.django_db
class TestCreateCastMember:
    def test_crete_castMember_successfully(
        self,
        castMember_repo
    ):
        url = "/api/cast_members/"
        data = {
            "name": "Test CastMember",
            "type": "ACTOR"
        }
        response = APIClient().post(url, data=data)
        
        assert response.status_code == 201
        assert response.data["id"] is not None
        assert castMember_repo.get_by_id(response.data["id"]) is not None
        
    def test_fail_on_create_castMember_with_invalid_type(self):
        url = "/api/cast_members/"
        data = {
            "name": "Test CastMember",
            "type": "INVALID"
        }
        
        response = APIClient().post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"type": ['"INVALID" is not a valid choice.']}
        
    def test_fail_on_create_castMember_with_invalid_name(self):
        url = "/api/cast_members/"
        data = {
            "name": "",
            "type": "ACTOR"
        }
        
        response = APIClient().post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}
        
@pytest.mark.django_db
class TestUpdateCastMember:
    def test_update_castMember_successfully(
        self,
        castMember_repo,
        castMember
    ):
        castMember_repo.save(castMember)
        url = f"/api/cast_members/{castMember.id}/"
        
        response = APIClient().put(url, data={"name": "Updated CastMember", "type": "DIRECTOR"})
        
        assert response.status_code == 204
        assert castMember_repo.get_by_id(castMember.id).name == "Updated CastMember"
        assert castMember_repo.get_by_id(castMember.id).type == "DIRECTOR"
        
    def test_update_cast_member_fail_invalid_id(self):
        url = "/api/cast_members/123/"
        
        response = APIClient().put(url, data={"name": "Updated CastMember", "type": "DIRECTOR"})
        
        assert response.status_code == 400
        assert response.data == {"id": ["Must be a valid UUID."]}
        
    def test_update_cast_member_fail_invalid_type(
            self,
            castMember_repo,
            castMember
        ):
            castMember_repo.save(castMember)
            url = f"/api/cast_members/{castMember.id}/"
            
            response = APIClient().put(url, data={"name": "Updated CastMember", "type": "invalid"})
            
            assert response.status_code == 400
            assert response.data == {"type": ['"invalid" is not a valid choice.']}
        
    def test_update_cast_member_fail_invalid_name(
            self,
            castMember_repo,
            castMember
        ):
            castMember_repo.save(castMember)
            url = f"/api/cast_members/{castMember.id}/"
            
            response = APIClient().put(url, data={"name": "", "type": "ACTOR"})
            
            assert response.status_code == 400
            assert response.data == {"name": ["This field may not be blank."]}
        
        
@pytest.mark.django_db
class TestDeleteCastMember:
    def test_delete_castMember(
        self,
        castMember_repo,
        castMember
    ):
        castMember_repo.save(castMember)
        url = f"/api/cast_members/{castMember.id}/"
        
        response = APIClient().delete(url)
        
        assert response.status_code == 204
        assert castMember_repo.get_by_id(castMember.id) is None
        
    def test_fail_on_delete_castMember_invalid_uuid(self):
        url = "/api/cast_members/123/"
        
        response = APIClient().delete(url)
        
        assert response.status_code == 400
        assert response.data == {"id": ["Must be a valid UUID."]}
        
    def test_fail_on_delete_castMember_not_found(self):
        id = uuid.uuid4()
        url = f"/api/cast_members/{id}/"
        
        response = APIClient().delete(url)
        
        assert response.status_code == 400
        assert response.data == {"error": f"Cast member with id {str(id)} was not found!"}