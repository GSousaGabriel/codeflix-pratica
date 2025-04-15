import pytest
from src.core.castMember.domain.castMember import CastMember

class TestCreateCastMember:
    def test_create_cast_member(self):
        cast_member = CastMember(name="John Doe", type="ACTOR")
        
        assert cast_member.name == "John Doe"
        assert cast_member.type == "ACTOR"
        
    def test_cast_member_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            CastMember(type="ACTOR")
        
    def test_cast_member_type_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'type'"):
            CastMember(name="John Doe")
        
    def test_cast_member_invalid_name_length(self):
        with pytest.raises(ValueError, match="Name should not be longer than 255 characters"):
            CastMember(name="a"*256, type="ACTOR")

class TestUpdateCastMember:
    def test_change_cast_member_data(self):
        cast_member = CastMember(name="John Doe", type="ACTOR")
        cast_member.change_name("Jane Doe")
        cast_member.change_type("DIRECTOR")
        
        assert cast_member.name == "Jane Doe"
        assert cast_member.type == "DIRECTOR"
        
    def test_cast_member_can_not_update_invalid_value(self):
        with pytest.raises(ValueError, match="Name should not be empty"):
            cast_member = CastMember(name="John Doe", type="ACTOR")
            cast_member.change_name("")
        
    def test_cast_member_invalid_name_length(self):
        with pytest.raises(ValueError, match="Name should not be longer than 255 characters"):
            cast_member = CastMember(name="John Doe", type="ACTOR")
            cast_member.change_name("a"*256)
        
    def test_cast_member_can_not_change_type_when_invalid(self):
        with pytest.raises(ValueError, match="Type should be either ACTOR or DIRECTOR"):
            cast_member = CastMember(name="John Doe", type="ACTOR")
            cast_member.change_type("invalid")