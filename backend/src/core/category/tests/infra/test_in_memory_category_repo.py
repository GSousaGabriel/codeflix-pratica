from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repo import InMemoryCategoryRepo


class TestInMemoryCategoryRepo:
    def test_can_save_category(self):
        repo = InMemoryCategoryRepo()
        category = Category(name="Movie", description="Movie category")
        
        repo.save(category)
        
        assert len(repo.categories) == 1
        assert repo.categories[0] == category
        
    def test_can_get_category(self):
        category = Category(name="Movie", description="Movie category")
        repo = InMemoryCategoryRepo([category])
        
        response = repo.get_by_id(category.id)
        
        assert len(repo.categories) == 1
        assert response == category
        
    def test_can_delete_category(self):
        category = Category(name="Movie", description="Movie category")
        repo = InMemoryCategoryRepo([category])
        
        response = repo.delete(category.id)
        
        assert response is None
        assert len(repo.categories) == 0