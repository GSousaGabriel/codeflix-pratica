from django.contrib import admin
from django_project.video_app.models import Video, AudioVideoMedia

class VideoAdmin(admin.ModelAdmin):
    pass

class AudioVideoMediaAdmin(admin.ModelAdmin):
    pass

admin.site.register(AudioVideoMedia, AudioVideoMediaAdmin)
admin.site.register(Video, VideoAdmin)