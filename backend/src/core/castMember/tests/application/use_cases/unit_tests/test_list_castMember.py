from unittest.mock import MagicMock

import pytest
from src.core._shared.listEntity import ListEntityResponse, ListPaginationInput, MetaPaginationOutput
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.list_castMember import ListCastMember
from src.core.castMember.domain.castMember import CastMember

@pytest.fixture
def castMember_both() -> CastMember:
    return CastMember(
            name="Joane John",
            type="DIRECTOR",
        )

@pytest.fixture
def castMember_female() -> CastMember:
    return CastMember(
            name="Joane Doe",
            type="DIRECTOR",
        )

@pytest.fixture
def castMember_male() -> CastMember:
    return CastMember(
            name="John Doe",
            type="ACTOR",
        )

@pytest.fixture
def castMember_repo() -> CastMemberRepository:
    return MagicMock(CastMemberRepository)

class TestListCastMember:
    def test_list_cast_member_with_values(
            self,
            castMember_repo,
            castMember_male,
            castMember_female
        ):
        
        castMember_repo.list.return_value = [castMember_male, castMember_female]
        input = ListPaginationInput(order_by="name")
        use_case = ListCastMember(castMember_repo)
        output = use_case.execute(input)
        
        assert len(output.data) == 2
        assert isinstance(output, ListEntityResponse)
        assert output.data[0].id == castMember_female.id
        assert output.data[1].id == castMember_male.id
        assert output.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=2
        )
        
    def test_list_cast_member_with_empty_list(
            self,
            castMember_repo
        ):
        castMember_repo.list.return_value = []
        
        use_case = ListCastMember(castMember_repo)
        output = use_case.execute(ListPaginationInput())
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 0
        assert output.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=0
        )
        
    def test_list_cast_member_with_2_pages(
            self,
            castMember_repo,
            castMember_male,
            castMember_female,
            castMember_both,
    ):
        castMember_repo.list.return_value = [castMember_male, castMember_both, castMember_female]
        
        input = ListPaginationInput(order_by="name", current_page=2)
        use_case = ListCastMember(castMember_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 1
        assert output.data[0].name == castMember_male.name
        assert output.meta == MetaPaginationOutput(
            current_page=2,
            per_page=2,
            total=3
        )