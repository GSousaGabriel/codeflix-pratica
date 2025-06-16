from uuid import UUID
import uuid
import pytest

from core.genre.domain.genre import Genre
from core.video.domain.video import Video
from django_project.video_app.repository import DjangoORMVideoRepository

@pytest.fixture
def video_repo() -> DjangoORMVideoRepository:
    return DjangoORMVideoRepository()

@pytest.mark.django_db
class TestVideo:
    def test_save_video_successfully(
        self,
        video_repo
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video_repo.save(video)
        
        saved_video = video_repo.video_model.objects.first()
        
        assert isinstance(saved_video.id, UUID)
        assert saved_video.title == "A movie"
        assert video_repo.video_model.objects.count() == 1
        
    def test_video_get_by_id(
        self,
        video_repo
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video_repo.save(video)
        
        saved_video = video_repo.get_by_id(video.id)
        
        assert saved_video is not None
        assert saved_video.title == "A movie"
        
    def test_video_get_by_id_non_existent_id(
        self,
        video_repo
    ):
        saved_video = video_repo.get_by_id(uuid.uuid4())
        
        assert saved_video is None
        
    def test_delete_video_successfully(
        self,
        video_repo
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video_repo.save(video)
        video_repo.delete(video.id)
        
        assert video_repo.video_model.objects.count() == 0
        
    def test_update_video_successfully(
        self,
        video_repo
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video_repo.save(video)
        
        video.title = "A serie"
        video.description = "A serie description"
        
        video_repo.update(video)
        updated_video = video_repo.video_model.objects.first()
        
        assert updated_video.title == "A serie"
        assert updated_video.description == "A serie description"
        assert video_repo.video_model.objects.count() == 1
        
    def test_do_not_update_video_when_no_id_valid(
        self,
        video_repo
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video2 = Video(
            title = "A drama movie", 
            description="Drama movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video_repo.save(video)
        
        video2.title = "A romance video"
        video2.description = "A romance video description"
        
        updated_video = video_repo.update(video2)
        video_video = video_repo.video_model.objects.first()
        
        assert updated_video is None
        assert video_video.title == "A movie"
        assert video_video.description == "Tense movie descripion"
        
    def test_get_all_videos(
        self,
        video_repo
    ):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video2 = Video(
            title = "A drama movie", 
            description="Drama movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        video_repo.save(video)
        video_repo.save(video2)
        
        all_videos = video_repo.list()
        
        assert len(all_videos) == 2
        
    def test_get_all_videos_empty(
        self,
        video_repo
    ):
        all_videos = video_repo.list()
        
        assert len(all_videos) == 0
        