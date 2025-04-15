

from unittest.mock import create_autospec
import pytest

from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.delete_castMember import DeleteCastMember
from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound
from src.core.castMember.domain.castMember import CastMember

@pytest.fixture
def cast_member():
    return CastMember(
        name="John Doe",
        type="ACTOR",
    )

@pytest.fixture
def mock_repo_castMember():
    return create_autospec(CastMemberRepository)

class TestDeleteCastMember:
    def test_delete_castMember_with_invalid_id(
        self,
        mock_repo_castMember
    ):
        input = DeleteCastMember.Input(id="")
        use_case = DeleteCastMember(mock_repo_castMember)
        mock_repo_castMember.get_by_id.return_value = None
        
        with pytest.raises(CastMemberNotFound, match="Cast member with id .* was not found!"):
            use_case.execute(input)
            
    def test_delete_castMember_successfully(
        self,
        cast_member,
        mock_repo_castMember
    ):
        input = DeleteCastMember.Input(id=cast_member.id)
        mock_repo_castMember.get_by_id.return_value = cast_member
        use_case = DeleteCastMember(mock_repo_castMember)
        use_case.execute(input)
        
        mock_repo_castMember.delete.assert_called_once_with(cast_member.id)
        