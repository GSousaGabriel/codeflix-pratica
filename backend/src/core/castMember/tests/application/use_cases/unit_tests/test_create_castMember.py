from unittest.mock import MagicMock
from uuid import UUID

import pytest
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.create_castMember import CreateCastMember
from src.core.castMember.application.use_cases.exceptions import InvalidCastMember
from src.core.castMember.domain.castMember import CastMember

class TestCreateCastMember:
    def test_create_castMember_valid_params(self):
        mocked_repo = MagicMock(CastMemberRepository)
        
        input = CreateCastMember.Input(
            name="John Doe",
            type="ACTOR"
        )
        use_case = CreateCastMember(mocked_repo)
        output = use_case.execute(input)
        
        assert isinstance(output.id, UUID)
        mocked_repo.save.assert_called_once_with(CastMember(
            id=output.id,
            name="John Doe",
            type="ACTOR"
        ))
        
    def test_create_castMember_invalid_name(self):
        mocked_repo = MagicMock(CastMemberRepository)
        
        input = CreateCastMember.Input(
            name="",
            type="ACTOR"
        )
        
        with pytest.raises(InvalidCastMember, match="Name should not be empty"):
            use_case = CreateCastMember(mocked_repo)
            use_case.execute(input)
        
    def test_create_castMember_invalid_type(self):
        mocked_repo = MagicMock(CastMemberRepository)
        
        input = CreateCastMember.Input(
            name="John Doe",
            type=""
        )
        
        with pytest.raises(InvalidCastMember, match="Type should be either ACTOR or DIRECTOR"):
            use_case = CreateCastMember(mocked_repo)
            use_case.execute(input)
        