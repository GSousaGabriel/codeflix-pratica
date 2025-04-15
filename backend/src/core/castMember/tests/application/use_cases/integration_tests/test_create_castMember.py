
from uuid import UUID
import pytest

from src.core.castMember.application.use_cases.create_castMember import CreateCastMember
from src.core.castMember.application.use_cases.exceptions import InvalidCastMember
from src.core.castMember.domain.castMember import CastMember
from src.core.castMember.infra.in_memory_castMember_repo import InMemoryCastMemberRepo


@pytest.fixture
def castMember_repo() -> InMemoryCastMemberRepo:
    return InMemoryCastMemberRepo()

class TestCreateCastMember:
    def test_create_cast_member(
        self,
        castMember_repo
    ):
        input = CreateCastMember.Input(name="John Doe", type="ACTOR")
        use_case = CreateCastMember(castMember_repo)
        output = use_case.execute(input)
        cast_member = castMember_repo.get_by_id(output.id)
        
        assert isinstance(output.id, UUID)
        assert cast_member is not None
        assert cast_member.name == input.name
        assert cast_member.type == input.type
        
    def test_create_castMember_invalid_name(
        self,
        castMember_repo    
    ):        
        input = CreateCastMember.Input(
            name="",
            type="ACTOR"
        )
        
        with pytest.raises(InvalidCastMember, match="Name should not be empty"):
            use_case = CreateCastMember(castMember_repo)
            use_case.execute(input)
        
    def test_create_castMember_invalid_type(
        self,
        castMember_repo
    ):        
        input = CreateCastMember.Input(
            name="John Doe",
            type=""
        )
        
        with pytest.raises(InvalidCastMember, match="Type should be either ACTOR or DIRECTOR"):
            use_case = CreateCastMember(castMember_repo)
            use_case.execute(input)