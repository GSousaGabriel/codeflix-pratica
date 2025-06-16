import uuid
from django.db import transaction
from src.core.video.application.use_cases.video_repository import VideoRepository
from src.core.video.domain.value_objects import AudioVideoMedia, MediaType
from src.core.video.domain.video import Video
from django_project.video_app.models import AudioVideoMedia as AudioVideoMediaORM, Video as VideoModel


class DjangoORMVideoRepository(VideoRepository):
    def __init__(self, video_model: VideoModel = VideoModel):
        self.video_model = video_model
    
    def save(self, video: Video):
        with transaction.atomic():
            video_mapped = VideoModeMapper.to_model(video)
            video_mapped.categories.set(video.categories)
            video_mapped.genres.set(video.genres)
            video_mapped.cast_members.set(video.cast_members)
            video_mapped.save()
            
    def get_by_id(self, id: uuid.UUID) -> Video | None:
        try:
            video_instance = self.video_model.objects.get(id=id)
            return VideoModeMapper.to_entity(video_instance)
        except self.video_model.DoesNotExist:
            return None
    
    def delete(self, id: uuid.UUID) -> None:
        self.video_model.objects.get(pk=id).delete()
    
    def update(self, video: Video) -> None:
        try:
            video_instance = self.video_model.objects.get(pk=video.id)
        except self.video_model.DoesNotExist:
            return None
        
        AudioVideoMediaORM.objects.filter(pk=video.id).delete()
        with transaction.atomic():
            video_instance.title = video.title
            video_instance.description = video.description
            video_instance.launch_year = video.launch_year
            video_instance.duration = video.duration
            video_instance.published = video.published
            video_instance.opened = video.opened
            video_instance.rating = video.rating
            video_instance.video = AudioVideoMediaORM.objects.create(
                name=video.video.name,
                raw_location=video.video.raw_location,
                encoded_location=video.video.encoded_location,
                status=video.video.status.value,
            ) if video.video else None
            
            video_instance.categories.set(video.categories)
            video_instance.genres.set(video.genres)
            video_instance.cast_members.set(video.cast_members)
            
            video_instance.save()
    
    def list(self) -> list[Video]:
        return [
            VideoModeMapper.to_entity(video)
            for video in self.video_model.objects.all()
        ]
        
class VideoModeMapper:
    @staticmethod
    def to_model(video: Video)-> VideoModel:
        return VideoModel(
            id = video.id,
            title = video.title,
            description = video.description,
            launch_year = video.launch_year,
            opened = video.opened,
            duration = video.duration,
            published = video.published,
            rating = video.rating,
        )
        
    @staticmethod
    def to_entity(video_model: VideoModel) -> Video:
        video = Video(
                title = video_model.title,
                description = video_model.description,
                launch_year = video_model.launch_year,
                duration = video_model.duration,
                published = video_model.published,
                opened = video_model.opened,
                rating = video_model.rating,
                categories = set(video_model.categories.values_list("id", flat=True)),
                genres = set(video_model.genres.values_list("id", flat=True)),
                cast_members = set(video_model.cast_members.values_list("id", flat=True)),
                id=video_model.id
            )
        
        if video_model.video:
            video.video = AudioVideoMedia(
                name=video_model.video.name,
                raw_location=video_model.video.raw_location,
                encoded_location=video_model.video.encoded_location,
                status=video_model.video.status,
                media_type=MediaType.VIDEO,
            )
            
        return video