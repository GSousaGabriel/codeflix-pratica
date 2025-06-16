from uuid import uuid4
from django.db import models

from src.core.video.domain.value_objects import MediaStatus, Rating


class Video(models.Model):
    RATING_CHOICES = [(rating.name, rating.value) for rating in Rating]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_year = models.IntegerField()
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    opened = models.BooleanField()
    published = models.BooleanField()
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    categories = models.ManyToManyField("category_app.Category", related_name="videos")
    genres = models.ManyToManyField("genre_app.Genre", related_name="videos")
    cast_members = models.ManyToManyField("castMember_app.CastMember", related_name="videos")
    banner = models.OneToOneField("ImageMedia", null=True, blank=True, on_delete=models.SET_NULL, related_name="video_banner")
    thumbnail = models.OneToOneField("ImageMedia", null=True, blank=True, on_delete=models.SET_NULL, related_name="video_thumbnail")
    thumbnail_half = models.OneToOneField("ImageMedia", null=True, blank=True, on_delete=models.SET_NULL, related_name="video_thumbnail_half")
    thumbnail_trailer = models.OneToOneField("ImageMedia", null=True, blank=True, on_delete=models.SET_NULL, related_name="video_thumbnail_trailer")
    video = models.OneToOneField("AudioVideoMedia", null=True, blank=True, on_delete=models.SET_NULL, related_name="video_media")
    
    class Meta:
        db_table = "videos"
    
    def __str__(self):
        return self.title
    
class ImageMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    checksum = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)

class AudioVideoMedia(models.Model):
    STATUS_CHOICES = [(status.name, status.value) for status in MediaStatus]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)
    encoded_location = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=MediaStatus.PENDING.value)