import pytest
from uuid import UUID
import uuid
from src.core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()
            
    def test_name_should_have_less_255_characteres(self):
        with pytest.raises(ValueError, match="Name should not be longer than 255 characters"):
            Category("a"*256)
            
    def test_name_should_be_truthy(self):
        with pytest.raises(ValueError, match="Name should not be empty"):
            Category("")
            
    def test_id_must_be_generated_if_not_provided(self):
        category = Category("Movies")
        assert isinstance(category.id, UUID)
            
    def test_created_category_default_values(self):
        category = Category("Movies")
        assert category.name == "Movies"
        assert category.description == ""
            
    def test_created_category_provided_values(self):
        category = Category("Movies", id=uuid.uuid4(), description="Movies in general", is_active=False)
        assert category.name == "Movies"
        assert category.description == "Movies in general"
        assert isinstance(category.id, UUID)
        assert category.is_active is False
            
    def test_show_info_when_object_called_as_string(self):
        category = Category("Movies", id=uuid.uuid4(), description="Movies in general", is_active=False)
        assert str(category) == "Movies - Movies in general (False)"
        
class TestUpdateCategory:
    def test_update_category_with_name_description(self):
        category = Category("Movies", description="Movies in general")
        
        category.update_category(name="Serie", description="Series in general")
        
        assert category.name == "Serie"
        assert category.description == "Series in general"
            
    def test_name_should_not_update_with_more_255_characteres(self):
        with pytest.raises(ValueError, match="Name should not be longer than 255 characters"):
            category = Category("Movies", description="Movies in general")
            
            category.update_category(name="a"*256, description="Series in general")
            
    def test_name_should_not_update_when_falsy(self):
        with pytest.raises(ValueError, match="Name should not be empty"):
            category = Category("Movies", description="Movies in general")
            
            category.update_category(name="", description="Series in general")
        
class TestActivateCategory:
    def test_activate_category(self):
        category = Category("Movies", description="Movies in general")
        
        category.activate()
        assert category.is_active is True
        
    def test_activate_category_already_active(self):
        category = Category("Movies", description="Movies in general", is_active=True)
        
        category.activate()
        assert category.is_active is True
        
class TestDeactivateCategory:
    def test_deactivate_category(self):
        category = Category("Movies", description="Movies in general")
        
        category.deactivate()
        assert category.is_active is False
        
    def test_deactivate_category_already_inative(self):
        category = Category("Movies", description="Movies in general", is_active=False)
        
        category.deactivate()
        assert category.is_active is False

class TestCategoryEquality:
    def test_categories_have_same_id(self):
        common_id = uuid.uuid4()
        category_1 = Category("Movies", id=common_id)
        category_2 = Category("Movies", id=common_id)
        
        assert category_1 == category_2
        
    def test_equality_different_classes(self):
        class Dummy:
            pass
        
        common_id = uuid.uuid4()
        category_1 = Category("Movies", id=common_id)
        dummy = Dummy()
        dummy.id = common_id
        
        assert category_1 != dummy
       