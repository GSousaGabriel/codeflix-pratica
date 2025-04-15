

import pytest

from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.castMember.application.use_cases.update_castMember import UpdateCastMember
from src.core.castMember.domain.castMember import CastMember
from src.core.castMember.infra.in_memory_castMember_repo import InMemoryCastMemberRepo

@pytest.fixture
def cast_member() -> CastMember:
    return CastMember(name="John Doe", type="ACTOR")

@pytest.fixture
def castMember_repo(cast_member) -> InMemoryCastMemberRepo:
    return InMemoryCastMemberRepo([cast_member])

class TestUpdateCastMember:
    def test_update_castMember_successfully(
        self,
        cast_member,
        castMember_repo
    ):
        input = UpdateCastMember.Input(cast_member.id, name="Jane Doe", type="DIRECTOR")
        use_case = UpdateCastMember(castMember_repo)
        use_case.execute(input)
        updated_cast_member = castMember_repo.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Jane Doe"
        assert updated_cast_member.type == "DIRECTOR"
        
    def test_update_with_invalid_type(
        self,
        cast_member,
        castMember_repo
    ):
        input = UpdateCastMember.Input(id= cast_member.id, name="Jhon Doe", type="actor")
        use_case = UpdateCastMember(castMember_repo)
        
        with pytest.raises(InvalidCastMember, match="Type should be either ACTOR or DIRECTOR"):
            use_case.execute(input)
        
    def test_update_with_invalid_name(
        self,
        cast_member,
        castMember_repo
    ):
        input = UpdateCastMember.Input(id= cast_member.id, name="a"*256, type="ACTOR")
        use_case = UpdateCastMember(castMember_repo)
        
        with pytest.raises(InvalidCastMember, match="Name should not be longer than 255 characters"):
            use_case.execute(input)
        
    def test_update_castMember_not_found(
        self,
        castMember_repo
    ):
        input = UpdateCastMember.Input(id="non-existent-id", name="Jane Doe", type="DIRECTOR")
        use_case = UpdateCastMember(castMember_repo)
        
        with pytest.raises(CastMemberNotFound, match="Cast member with id .* was not found!"):
            use_case.execute(input)