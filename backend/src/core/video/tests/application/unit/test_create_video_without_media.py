from unittest.mock import create_autospec
from uuid import UUID
import pytest

from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.domain.castMember import CastMember
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.use_cases.video_repository import VideoRepository

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Action")

@pytest.fixture
def cast_member() -> CastMember:
    return CastMember(name="John Doe", type="ACTOR")

@pytest.fixture
def drama_genre() -> Genre:
    return Genre(name="Drama")

@pytest.fixture
def category_repo() -> CategoryRepository:
    return create_autospec(CategoryRepository)

@pytest.fixture
def genre_repo() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def cast_member_repo() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)

@pytest.fixture
def video_repo() -> VideoRepository:
    return create_autospec(VideoRepository)

class TestCreateVideoWithoutMedia:
    def test_create_video_successfully(
        self,
        movie_category,
        cast_member,
        drama_genre,
        genre_repo,
        cast_member_repo,
        category_repo,
        video_repo
    ):
        use_case = CreateVideoWithoutMedia(video_repo, category_repo, genre_repo, cast_member_repo)
        genre_repo.list.return_value = [drama_genre]
        cast_member_repo.list.return_value = [cast_member]
        category_repo.list.return_value = [movie_category]
        
        input = CreateVideoWithoutMedia.Input("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set([movie_category.id]), set([drama_genre.id]), set([cast_member.id]))
        output = use_case.execute(input)
        
        assert isinstance(output.id, UUID)
        
    def test_fail_to_create_video_with_empty_title(
        self,
        movie_category,
        cast_member,
        drama_genre,
        genre_repo,
        cast_member_repo,
        category_repo,
        video_repo
    ):
        use_case = CreateVideoWithoutMedia(video_repo, category_repo, genre_repo, cast_member_repo)
        genre_repo.list.return_value = [drama_genre]
        cast_member_repo.list.return_value = [cast_member]
        category_repo.list.return_value = [movie_category]
        
        input = CreateVideoWithoutMedia.Input("", "Tense movie descripion", 2000, 123.34, True, "ER", set([movie_category.id]), set([drama_genre.id]), set([cast_member.id]))
        
        with pytest.raises(InvalidVideo, match="Title cannot be empty."):
            use_case.execute(input)
        
    def test_fail_to_create_video_with_big_title(
        self,
        movie_category,
        cast_member,
        drama_genre,
        genre_repo,
        cast_member_repo,
        category_repo,
        video_repo
    ):
        use_case = CreateVideoWithoutMedia(video_repo, category_repo, genre_repo, cast_member_repo)
        genre_repo.list.return_value = [drama_genre]
        cast_member_repo.list.return_value = [cast_member]
        category_repo.list.return_value = [movie_category]
        
        input = CreateVideoWithoutMedia.Input("a"*255, "Tense movie descripion", 2000, 123.34, True, "ER", set([movie_category.id]), set([drama_genre.id]), set([cast_member.id]))
        
        with pytest.raises(InvalidVideo, match="Title cannot be longer than 255 characteres."):
            use_case.execute(input)
        
    def test_fail_to_create_video_with_no_duration(
        self,
        movie_category,
        cast_member,
        drama_genre,
        genre_repo,
        cast_member_repo,
        category_repo,
        video_repo
    ):
        use_case = CreateVideoWithoutMedia(video_repo, category_repo, genre_repo, cast_member_repo)
        genre_repo.list.return_value = [drama_genre]
        cast_member_repo.list.return_value = [cast_member]
        category_repo.list.return_value = [movie_category]
        
        input = CreateVideoWithoutMedia.Input("A title", "Tense movie descripion", 2000, 0, True, "ER", set([movie_category.id]), set([drama_genre.id]), set([cast_member.id]))
        
        with pytest.raises(InvalidVideo, match="Duration cannot be 0 or less."):
            use_case.execute(input)
        
    def test_can_not_create_video_with_invalid_related_entities(
        self,
        movie_category,
        cast_member,
        drama_genre,
        genre_repo,
        cast_member_repo,
        category_repo,
        video_repo
    ):
        use_case = CreateVideoWithoutMedia(video_repo, category_repo, genre_repo, cast_member_repo)
        genre_repo.list.return_value = []
        cast_member_repo.list.return_value = []
        category_repo.list.return_value = []
        
        input = CreateVideoWithoutMedia.Input("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set([movie_category.id]), set([drama_genre.id]), set([cast_member.id]))
        
        with pytest.raises(RelatedEntitiesNotFound, match="Categories with provided IDs not found.\nGenres with provided IDs not found.\nCast members with provided IDs not found."):
            use_case.execute(input)
        
    def test_can_not_create_video_with_some_invalid_related_entities(
        self,
        movie_category,
        cast_member,
        drama_genre,
        genre_repo,
        cast_member_repo,
        category_repo,
        video_repo
    ):
        use_case = CreateVideoWithoutMedia(video_repo, category_repo, genre_repo, cast_member_repo)
        genre_repo.list.return_value = []
        cast_member_repo.list.return_value = []
        category_repo.list.return_value = [movie_category]
        
        input = CreateVideoWithoutMedia.Input("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set([movie_category.id]), set([drama_genre.id]), set([cast_member.id]))
        
        with pytest.raises(RelatedEntitiesNotFound, match="Genres with provided IDs not found.\nCast members with provided IDs not found."):
            use_case.execute(input)