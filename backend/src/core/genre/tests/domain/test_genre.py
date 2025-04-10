import pytest
from uuid import UUID
import uuid
from src.core.genre.domain.genre import Genre

class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()
            
    def test_name_should_have_less_255_characteres(self):
        with pytest.raises(ValueError, match="Name should not be longer than 255 characters"):
            Genre("a"*256)
            
    def test_name_should_be_truthy(self):
        with pytest.raises(ValueError, match="Name should not be empty"):
            Genre("")
            
    def test_create_genre_with_defautl_values(self):
        genre = Genre("Romance")
        
        assert genre.name == "Romance"
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories_ids == set()
            
    def test_created_genre_provided_values(self):
        categories = {uuid.uuid4(), uuid.uuid4()}
        genre = Genre("Romance", id=uuid.uuid4(), categories_ids=categories, is_active=False)
        assert genre.name == "Romance"
        assert genre.categories_ids == categories
        assert isinstance(genre.id, UUID)
        assert genre.is_active is False
            
    def test_show_info_when_object_called_as_string(self):
        genre = Genre("Romance", id=uuid.uuid4(), is_active=False)
        assert str(genre) == "Romance - (False)"
        
class TestUpdateGenre:
    def test_update_genre_name (self):
        genre = Genre("Romance")
        genre.change_name(name="Drama")
        
        assert genre.name == "Drama"
            
    def test_name_should_not_update_with_more_255_characteres(self):
        with pytest.raises(ValueError, match="Name should not be longer than 255 characters"):
            genre = Genre("Romance")
            
            genre.change_name(name="a"*256)
            
    def test_name_should_not_update_when_falsy(self):
        with pytest.raises(ValueError, match="Name should not be empty"):
            genre = Genre("Romance")
            
            genre.change_name(name="")
        
class TestActivateGenre:
    def test_activate_genre(self):
        genre = Genre("Romance")
        
        genre.activate()
        assert genre.is_active is True
        
    def test_activate_genre_already_active(self):
        genre = Genre("Romance", is_active=True)
        
        genre.activate()
        assert genre.is_active is True
        
class TestDeactivateGenre:
    def test_deactivate_genre(self):
        genre = Genre("Romance")
        
        genre.deactivate()
        assert genre.is_active is False
        
    def test_deactivate_genre_already_inative(self):
        genre = Genre("Romance", is_active=False)
        
        genre.deactivate()
        assert genre.is_active is False
        
class TestAddCategory:
    def test_add_category_to_genre(self):
        genre = Genre("Romance")
        id_category = uuid.uuid4()
        
        genre.add_category(id_category)
        
        assert len(genre.categories_ids) == 1
        assert genre.categories_ids == {id_category}
        
    def test_add_multiple_categories_to_genre(self):
        genre = Genre("Romance")
        id_category = uuid.uuid4()
        id_category2 = uuid.uuid4()
        
        genre.add_category(id_category)
        genre.add_category(id_category2)
        
        assert len(genre.categories_ids) == 2
        assert id_category in genre.categories_ids
        assert id_category2 in genre.categories_ids
        
    def test_remove_category_from_genre(self):
        id_category = uuid.uuid4()
        genre = Genre("Romance", categories_ids={id_category})
        
        genre.remove_category(id_category)
        
        assert len(genre.categories_ids) == 0
        
    def test_remove_all_category_from_genre(self):
        id_category = uuid.uuid4()
        id_category2 = uuid.uuid4()
        genre = Genre("Romance", categories_ids={id_category, id_category2})
        
        genre.clear_category()
        
        assert len(genre.categories_ids) == 0

class TestGenreEquality:
    def test_categories_have_same_id(self):
        common_id = uuid.uuid4()
        genre_1 = Genre("Romance", id=common_id)
        genre_2 = Genre("Romance", id=common_id)
        
        assert genre_1 == genre_2
        
    def test_equality_different_classes(self):
        class Dummy:
            pass
        
        common_id = uuid.uuid4()
        genre_1 = Genre("Romance", id=common_id)
        dummy = Dummy()
        dummy.id = common_id
        
        assert genre_1 != dummy
       