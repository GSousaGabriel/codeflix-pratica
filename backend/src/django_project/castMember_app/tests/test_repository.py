import uuid

import pytest
from core.castMember.application.use_cases.list_castMember import ListCastMember
from django_project.castMember_app.repository import DjangoORMCastMemberRepository
from src.core._shared.listEntity import ListPaginationInput, MetaPaginationOutput
from src.core.castMember.application.use_cases.create_castMember import CreateCastMember
from src.core.castMember.application.use_cases.delete_castMember import DeleteCastMember
from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.castMember.application.use_cases.update_castMember import UpdateCastMember

@pytest.fixture
def castMember_repo() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()

@pytest.mark.django_db
class Testlist:
    def test_list_castMember(
            self,
            castMember_repo
        ):
            castMember_repo.castMember_model.objects.create(
                id=uuid.uuid4(),
                name="Test CastMember",
                type="ACTOR",
            )
            
            input = ListPaginationInput()
            use_case = ListCastMember(castMember_repo)
            response = use_case.execute(input)
            
            assert len(response.data) == 1
            assert response.meta == MetaPaginationOutput(
                current_page = 1,
                per_page = 2,
                total = 1
            )
        
    def test_list_empty_castMember(
            self,
            castMember_repo
        ):
            input = ListPaginationInput()
            use_case = ListCastMember(castMember_repo)
            response = use_case.execute(input)
            
            assert len(response.data) == 0
            assert response.meta == MetaPaginationOutput(
                current_page = 1,
                per_page = 2,
                total = 0
            )

@pytest.mark.django_db
class TestCreate:
    def test_create_successfully_castMember(
            self,
            castMember_repo
        ):        
            input = CreateCastMember.Input(name="Test CastMember", type="ACTOR")
            use_case = CreateCastMember(castMember_repo)
            output = use_case.execute(input)
            
            assert isinstance(output.id, uuid.UUID)
        
    def test_create_castMember_with_invalid_type(
            self,
            castMember_repo
        ):
            input = CreateCastMember.Input(name="Test CastMember", type="INVALID_TYPE")
            use_case = CreateCastMember(castMember_repo)
            
            with pytest.raises(InvalidCastMember, match="Type should be either ACTOR or DIRECTOR"):
                use_case.execute(input)
        
    def test_create_castMember_with_invalid_name(
            self,
            castMember_repo
        ):
            input = CreateCastMember.Input(name="", type="DIRECTOR")
            use_case = CreateCastMember(castMember_repo)
            
            with pytest.raises(InvalidCastMember, match="Name should not be empty"):
                use_case.execute(input)
            
@pytest.mark.django_db
class TestUpdate:
    def test_update_castMember(
            self,
            castMember_repo
        ):
            id = uuid.uuid4()
            castMember_repo.castMember_model.objects.create(id= id, name="Test CastMember", type="ACTOR")
            
            input = UpdateCastMember.Input(id=id, name="Updated CastMember", type="DIRECTOR")
            use_case = UpdateCastMember(castMember_repo)
            use_case.execute(input)
            
            assert castMember_repo.castMember_model.objects.get(pk=id).name == "Updated CastMember"
            assert castMember_repo.castMember_model.objects.get(pk=id).type == "DIRECTOR"
            
    def test_fail_to_update_with_invalid_type(
        self,
        castMember_repo
    ):
        id = uuid.uuid4()
        castMember_repo.castMember_model.objects.create(id= id, name="Test CastMember", type="ACTOR")
        
        input = UpdateCastMember.Input(id=id, name="Updated CastMember", type="INVALID_TYPE")
        use_case = UpdateCastMember(castMember_repo)
        
        with pytest.raises(InvalidCastMember, match="Type should be either ACTOR or DIRECTOR"):
            use_case.execute(input)
            
    def test_fail_to_update_with_invalid_name(
        self,
        castMember_repo
    ):
        id = uuid.uuid4()
        castMember_repo.castMember_model.objects.create(id= id, name="Test CastMember", type="ACTOR")
        
        input = UpdateCastMember.Input(id=id, name="", type="DIRECTOR")
        use_case = UpdateCastMember(castMember_repo)
        
        with pytest.raises(InvalidCastMember, match="Name should not be empty"):
            use_case.execute(input)
            
    def test_fail_to_update_when_id_is_not_found(
        self,
        castMember_repo
    ):
        input = UpdateCastMember.Input(id=uuid.uuid4(), name="", type="DIRECTOR")
        use_case = UpdateCastMember(castMember_repo)
        
        with pytest.raises(CastMemberNotFound, match="Cast member with id .* was not found!"):
            use_case.execute(input)
            
@pytest.mark.django_db
class TestDelete:
    def test_delete_castMember_successfully(
            self,
            castMember_repo
        ):
            id = uuid.uuid4()
            castMember_repo.castMember_model.objects.create(id= id, name="Test CastMember", type="ACTOR")
            
            input = DeleteCastMember.Input(id=id)
            use_case = DeleteCastMember(castMember_repo)
            use_case.execute(input)
            
            assert castMember_repo.castMember_model.objects.filter(pk=id).exists() == False
    
    def test_do_not_delete_castMember_when_id_not_found(
            self,
            castMember_repo
        ):
            id = uuid.uuid4()
            
            input = DeleteCastMember.Input(id=id)
            use_case = DeleteCastMember(castMember_repo)
            
            with pytest.raises(CastMemberNotFound, match="Cast member with id .* was not found!"):
                use_case.execute(input)