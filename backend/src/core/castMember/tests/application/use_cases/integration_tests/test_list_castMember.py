import pytest
from src.core._shared.listEntity import ListEntityResponse, ListPaginationInput, MetaPaginationOutput
from src.core.castMember.application.use_cases.list_castMember import ListCastMember
from src.core.castMember.domain.castMember import CastMember
from src.core.castMember.infra.in_memory_castMember_repo import InMemoryCastMemberRepo

@pytest.fixture
def cast_member_both() -> CastMember:
    return CastMember(
            name="John Joane",
            type="ACTOR",
        )
    
@pytest.fixture
def cast_member_male() -> CastMember:
    return CastMember(
            name="John Doe",
            type="ACTOR",
        )

@pytest.fixture
def cast_member_female() -> CastMember:
    return CastMember(
            name="Joane Doe",
            type="DIRECTOR",
        )

@pytest.fixture
def in_memory_repo() -> InMemoryCastMemberRepo:
    return InMemoryCastMemberRepo()

class TestListCastMember:
    def test_list_cast_member_with_values(
        self,
        in_memory_repo,
        cast_member_male,
        cast_member_female
    ):
        in_memory_repo.save(cast_member_male)
        in_memory_repo.save(cast_member_female)
        
        input = ListPaginationInput(order_by="name")
        use_case = ListCastMember(in_memory_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 2
        assert output.data[0].id == cast_member_female.id
        assert output.data[1].id == cast_member_male.id
        assert output.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=2
        )
        
    def test_list_cast_member_with_empty_list(
        self,
        in_memory_repo,
    ):
        input = ListPaginationInput()
        use_case = ListCastMember(in_memory_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 0
        assert output.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=0
        )
        
    def test_list_cast_member_with_2_pages(
            self,
            in_memory_repo,
        cast_member_male,
        cast_member_female,
        cast_member_both
    ):
        in_memory_repo.save(cast_member_male)
        in_memory_repo.save(cast_member_female)
        in_memory_repo.save(cast_member_both)
        
        input = ListPaginationInput(order_by="name", current_page=2)
        use_case = ListCastMember(in_memory_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 1
        assert output.data[0].name == cast_member_both.name
        assert output.meta == MetaPaginationOutput(
            current_page=2,
            per_page=2,
            total=3
        )