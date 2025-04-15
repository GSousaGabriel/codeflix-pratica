from unittest.mock import MagicMock
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.list_castMember import ListCastMember
from src.core.castMember.domain.castMember import CastMember

class TestListCastMember:
    def test_list_cast_member_with_values(self):
        mock_repo = MagicMock(CastMemberRepository)
        cast_member = CastMember(
            name="John Doe",
            type="ACTOR",
        )
        
        mock_repo.list.return_value = [cast_member]
        
        use_case = ListCastMember(mock_repo)
        output = use_case.execute()
        
        assert len(output.data) == 1
        assert output.data[0].id == cast_member.id
        
    def test_list_cast_member_with_empty_list(self):
        mock_repo = MagicMock(CastMemberRepository)
        mock_repo.list.return_value = []
        
        use_case = ListCastMember(mock_repo)
        output = use_case.execute()
        
        assert len(output.data) == 0