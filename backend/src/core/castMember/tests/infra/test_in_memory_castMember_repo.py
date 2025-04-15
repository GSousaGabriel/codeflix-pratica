from src.core.castMember.domain.castMember import CastMember
from src.core.castMember.infra.in_memory_castMember_repo import InMemoryCastMemberRepo

class TestInMemoryCastMemberRepo:
    def test_save_in_repo(self):
        cast_member_repo = InMemoryCastMemberRepo()
        cast_member = CastMember(
            name="John Doe",
            type="ACTOR",
        )
        
        cast_member_repo.save(cast_member)
        
        assert cast_member.id is not None
        assert cast_member.name == "John Doe"
        assert cast_member.type == "ACTOR"

    def test_list_from_repo(self):
        cast_member = CastMember(
            name="Jane Doe",
            type="DIRECTOR",
        )
        cast_member_repo = InMemoryCastMemberRepo(cast_members=[cast_member])
        
        retrieved_cast_member = cast_member_repo.list()
        
        assert len(retrieved_cast_member) == 1
        assert retrieved_cast_member[0].id == cast_member.id
        assert retrieved_cast_member[0].name == "Jane Doe"
        assert retrieved_cast_member[0].type == "DIRECTOR"

    def test_update_on_repo(self):
        cast_member = CastMember(
            name="Jane Doe",
            type="DIRECTOR",
        )
        cast_member_repo = InMemoryCastMemberRepo(cast_members=[cast_member])
        cast_member.name = "John Doe"
        cast_member.type = "ACTOR"
        
        cast_member_repo.update(cast_member)
        updated_cast_member = cast_member_repo.get_by_id(cast_member.id)
        
        assert updated_cast_member.id == cast_member.id
        assert updated_cast_member.name == "John Doe"
        assert updated_cast_member.type == "ACTOR"
        
    def test_delete_from_repo(self):
        cast_member = CastMember(
            name="Jane Doe",
            type="DIRECTOR",
        )
        cast_member_repo = InMemoryCastMemberRepo(cast_members=[cast_member])
        
        cast_member_repo.delete(cast_member.id)
        
        retrieved_cast_member = cast_member_repo.get_by_id(cast_member.id)
        assert retrieved_cast_member is None
        assert len(cast_member_repo.list()) == 0