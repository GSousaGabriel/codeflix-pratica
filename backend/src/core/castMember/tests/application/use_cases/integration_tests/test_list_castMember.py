from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.list_castMember import ListCastMember
from src.core.castMember.domain.castMember import CastMember
from src.core.castMember.infra.in_memory_castMember_repo import InMemoryCastMemberRepo

class TestListCastMember:
    def test_list_cast_member_with_values(self):
        cast_member = CastMember(
            name="John Doe",
            type="ACTOR",
        )
        castMember_repo = InMemoryCastMemberRepo([cast_member])
        
        use_case = ListCastMember(castMember_repo)
        output = use_case.execute()
        
        assert len(output.data) == 1
        assert output.data[0].id == cast_member.id
        
    def test_list_cast_member_with_empty_list(self):
        castMember_repo = InMemoryCastMemberRepo()
        
        use_case = ListCastMember(castMember_repo)
        output = use_case.execute()
        
        assert len(output.data) == 0