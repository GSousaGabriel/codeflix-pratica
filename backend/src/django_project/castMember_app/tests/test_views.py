import uuid
import pytest
from rest_framework.test import APIClient
from src.core._shared.tests.authentication.jwt_generator import JwtGenerator
import os
from src.core.castMember.domain.castMember import CastMember
from django_project.castMember_app.repository import DjangoORMCastMemberRepository

@pytest.fixture
def cast_member_both() -> CastMember:
    return CastMember(name="Joane John", type="DIRECTOR")

@pytest.fixture
def cast_member_female() -> CastMember:
    return CastMember(name="Joane Doe", type="ACTOR")

@pytest.fixture
def cast_member_male() -> CastMember:
    return CastMember(name="John Doe", type="ACTOR")
    
@pytest.fixture
def castMember_repo() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()

@pytest.fixture
def encoded_token() -> str:
    tokenGenerator = JwtGenerator()
    tokenGenerator.encode_jwt()
    return tokenGenerator.encoded_jwt

@pytest.fixture
def client(encoded_token: str) -> APIClient:
    return APIClient(headers={"Authorization": f"Bearer {encoded_token}"})

@pytest.fixture(autouse=True, scope="session")
def use_test_public_key():
    os.environ["AUTH_PUBLIC_KEY"] = os.getenv("TEST_PUBLIC_KEY")

@pytest.mark.django_db
class TestGetAllCastMember:
    def test_call_api_get_all(
            self,
            castMember_repo,
            cast_member_female,
            cast_member_male,
            client
        ):
        
        castMember_repo.save(cast_member_female)
        castMember_repo.save(cast_member_male)
        
        url = "/api/cast_members/?page=1&order=name"
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.data["data"]) == 2
        assert response.data["data"][0]["name"] == cast_member_female.name
        assert response.data["data"][1]["name"] == cast_member_male.name
        assert response.data["meta"] == {
            "current_page": 1,
            "per_page": 2,
            "total": 2
        }
        
@pytest.mark.django_db
class TestCreateCastMember:
    def test_crete_castMember_successfully(
        self,
        castMember_repo,
        client
    ):
        url = "/api/cast_members/"
        data = {
            "name": "Test CastMember",
            "type": "ACTOR"
        }
        response = client.post(url, data=data)
        
        assert response.status_code == 201
        assert response.data["id"] is not None
        assert castMember_repo.get_by_id(response.data["id"]) is not None
        
    def test_fail_on_create_castMember_with_invalid_type(
        self,
        client):
        url = "/api/cast_members/"
        data = {
            "name": "Test CastMember",
            "type": "INVALID"
        }
        
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"type": ['"INVALID" is not a valid choice.']}
        
    def test_fail_on_create_castMember_with_invalid_name(
        self,
        client):
        url = "/api/cast_members/"
        data = {
            "name": "",
            "type": "ACTOR"
        }
        
        response = client.post(url, data=data)
        
        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}
        
@pytest.mark.django_db
class TestUpdateCastMember:
    def test_update_castMember_successfully(
        self,
        castMember_repo,
        cast_member_male,
        client
    ):
        castMember_repo.save(cast_member_male)
        url = f"/api/cast_members/{cast_member_male.id}/"
        
        response = client.put(url, data={"name": "Updated CastMember", "type": "DIRECTOR"})
        
        assert response.status_code == 204
        assert castMember_repo.get_by_id(cast_member_male.id).name == "Updated CastMember"
        assert castMember_repo.get_by_id(cast_member_male.id).type == "DIRECTOR"
        
    def test_update_cast_member_fail_invalid_id(
        self,
        client):
        url = "/api/cast_members/123/"
        
        response = client.put(url, data={"name": "Updated CastMember", "type": "DIRECTOR"})
        
        assert response.status_code == 400
        assert response.data == {"id": ["Must be a valid UUID."]}
        
    def test_update_cast_member_fail_invalid_type(
            self,
            castMember_repo,
            cast_member_male,
            client
        ):
            castMember_repo.save(cast_member_male)
            url = f"/api/cast_members/{cast_member_male.id}/"
            
            response = client.put(url, data={"name": "Updated CastMember", "type": "invalid"})
            
            assert response.status_code == 400
            assert response.data == {"type": ['"invalid" is not a valid choice.']}
        
    def test_update_cast_member_fail_invalid_name(
            self,
            castMember_repo,
            cast_member_male,
            client
        ):
            castMember_repo.save(cast_member_male)
            url = f"/api/cast_members/{cast_member_male.id}/"
            
            response = client.put(url, data={"name": "", "type": "ACTOR"})
            
            assert response.status_code == 400
            assert response.data == {"name": ["This field may not be blank."]}
        
        
@pytest.mark.django_db
class TestDeleteCastMember:
    def test_delete_castMember(
        self,
        castMember_repo,
        cast_member_male,
        client
    ):
        castMember_repo.save(cast_member_male)
        url = f"/api/cast_members/{cast_member_male.id}/"
        
        response = client.delete(url)
        
        assert response.status_code == 204
        assert castMember_repo.get_by_id(cast_member_male.id) is None
        
    def test_fail_on_delete_castMember_invalid_uuid(
        self,
        client):
        url = "/api/cast_members/123/"
        
        response = client.delete(url)
        
        assert response.status_code == 400
        assert response.data == {"id": ["Must be a valid UUID."]}
        
    def test_fail_on_delete_castMember_not_found(
        self,
        client):
        id = uuid.uuid4()
        url = f"/api/cast_members/{id}/"
        
        response = client.delete(url)
        
        assert response.status_code == 400
        assert response.data == {"error": f"Cast member with id {str(id)} was not found!"}