
import pytest

from src.core.castMember.application.use_cases.delete_castMember import DeleteCastMember
from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound
from src.core.castMember.domain.castMember import CastMember
from src.core.castMember.infra.in_memory_castMember_repo import InMemoryCastMemberRepo

@pytest.fixture
def cast_member() -> CastMember:
    return CastMember(name="John Doe", type="ACTOR")

@pytest.fixture
def castMember_repo(cast_member) -> InMemoryCastMemberRepo:
    return InMemoryCastMemberRepo([cast_member])

class TestDeleteCastMember:
    def test_delete_cast_member(
        self,
        cast_member,
        castMember_repo
    ):
        input = DeleteCastMember.Input(id=cast_member.id)
        use_case = DeleteCastMember(castMember_repo)
        use_case.execute(input)
        cast_member_deleted = castMember_repo.get_by_id(cast_member.id)
        
        assert cast_member_deleted is None
        
    def test_delete_castMember_with_invalid_id(
        self,
        castMember_repo
    ):
        input = DeleteCastMember.Input(id="")
        use_case = DeleteCastMember(castMember_repo)
        
        with pytest.raises(CastMemberNotFound, match="Cast member with id .* was not found!"):
            use_case.execute(input)
        