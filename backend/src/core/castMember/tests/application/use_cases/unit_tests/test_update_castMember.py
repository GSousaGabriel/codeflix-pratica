from unittest.mock import create_autospec
import pytest
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.castMember.application.use_cases.update_castMember import UpdateCastMember
from src.core.castMember.domain.castMember import CastMember

@pytest.fixture
def cast_member():
    return CastMember(name="John Doe", type="ACTOR")

@pytest.fixture
def mock_castMember_repo():
    return create_autospec(CastMemberRepository)

class TestUpdateCastMember:
    def test_update_castMember_valid_params(
        self,
        cast_member,
        mock_castMember_repo
    ):
        input = UpdateCastMember.Input(id= cast_member.id, name="Jane Doe", type="DIRECTOR")
        
        mock_castMember_repo.get_by_id.return_value = cast_member
        use_case = UpdateCastMember(mock_castMember_repo)
        use_case.execute(input)
        
        mock_castMember_repo.update.assert_called_once_with(
            CastMember(
                id= cast_member.id,
                name= "Jane Doe",
                type= "DIRECTOR",
            )
        )
        
    def test_update_with_invalid_type(
        self,
        cast_member,
        mock_castMember_repo
    ):
        input = UpdateCastMember.Input(id= cast_member.id, name="John Doe", type="actor")
        use_case = UpdateCastMember(mock_castMember_repo)
        mock_castMember_repo.get_by_id.return_value = cast_member
        
        with pytest.raises(InvalidCastMember, match="Type should be either ACTOR or DIRECTOR"):
            use_case.execute(input)
            
        mock_castMember_repo.update.assert_not_called()
        
    def test_update_with_invalid_name(
        self,
        cast_member,
        mock_castMember_repo
    ):
        input = UpdateCastMember.Input(id= cast_member.id, name="a"*256, type="ACTOR")
        use_case = UpdateCastMember(mock_castMember_repo)
        mock_castMember_repo.get_by_id.return_value = cast_member
        
        with pytest.raises(InvalidCastMember, match="Name should not be longer than 255 characters"):
            use_case.execute(input)
            
        mock_castMember_repo.update.assert_not_called()
        
    def test_update_castMember_not_found(
        self,
        mock_castMember_repo
    ):
        input = UpdateCastMember.Input(id="non-existent-id", name="Jane Doe", type="DIRECTOR")
        use_case = UpdateCastMember(mock_castMember_repo)
        
        mock_castMember_repo.get_by_id.return_value = None
        
        with pytest.raises(CastMemberNotFound, match="Cast member with id .* was not found!"):
            use_case.execute(input)
            
        mock_castMember_repo.update.assert_not_called()
        
