import uuid
from django.db import transaction
from src.core.video.application.use_cases.video_repository import VideoRepository
from src.core.video.domain.video import Video
from django_project.video_app.models import Video as VideoModel


class DjangoORMVideoRepository(VideoRepository):
    def __init__(self, video_model: VideoModel = VideoModel):
        self.video_model = video_model
    
    def save(self, video: Video):
        with transaction.atomic():
            new_video = self.video_model.objects.create(
                id = video.id,
                title = video.title,
                description = video.description,
                launch_year = video.launch_year,
                duration = video.duration,
                published = video.published,
                rating = video.rating,
                banner = video.banner,
                thumbnail = video.thumbnail,
                thumbnail_half = video.thumbnail_half,
                thumbnail_trailer = video.thumbnail_trailer,
                video = video.video
            )
            new_video.categories_ids.set(video.categories_ids)
            new_video.genres_ids.set(video.genres_ids)
            new_video.cast_members_ids.set(video.cast_members_ids)
            
    def get_by_id(self, id: uuid.UUID) -> Video | None:
        try:
            video_instance = self.video_model.objects.get(pk=id)
            return Video(
                video_instance.title,
                video_instance.description,
                video_instance.launch_year,
                video_instance.duration,
                video_instance.published,
                video_instance.rating,
                video_instance.categories_ids,
                video_instance.genres_ids,
                video_instance.cast_members_ids,
                video_instance.banner,
                video_instance.thumbnail,
                video_instance.thumbnail_half,
                video_instance.thumbnail_trailer,
                video_instance.video,
                id=video_instance.id)
        except self.video_model.DoesNotExist:
            return None
    
    def delete(self, id: uuid.UUID) -> None:
        self.video_model.objects.get(pk=id).delete()
    
    def update(self, video: Video) -> None:
        try:
            video_instance = self.video_model.objects.get(pk=video.id)
        except self.video_model.DoesNotExist:
            return None
        
        with transaction.atomic():
            self.video_model.objects.update(
                title = video.title,
                description = video.description,
                launch_year = video.launch_year,
                duration = video.duration,
                published = video.published,
                rating = video.rating,
                banner = video.banner,
                thumbnail = video.thumbnail,
                thumbnail_half = video.thumbnail_half,
                thumbnail_trailer = video.thumbnail_trailer,
                video = video.video
            )
            
            video_instance.categories_ids.set(video.categories_ids)
            video_instance.genres_ids.set(video.genres_ids)
            video_instance.cast_members_ids.set(video.cast_members_ids)
    
    def list(self) -> list[Video]:
        return [
            Video(
                video.title,
                video.description,
                video.launch_year,
                video.duration,
                video.published,
                video.rating,
                video.categories_ids,
                video.genres_ids,
                video.cast_members_ids,
                video.banner,
                video.thumbnail,
                video.thumbnail_half,
                video.thumbnail_trailer,
                video.video,
                id=video.id)
            for video in self.video_model.objects.all()
        ]