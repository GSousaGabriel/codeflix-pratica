from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.storage.local_storage import LocalStorage
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.use_cases.upload_video import UploadVideo
from django_project.castMember_app.repository import DjangoORMCastMemberRepository
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.video_app.repository import DjangoORMVideoRepository
from django_project.video_app.serializers import CreateVideoInputSerializer, CreateVideoOutputSerializer
from src.django_project.permissions import IsAuthenticated

class VideoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]     
    def create(self, request: Request)->Response:
        serializer = CreateVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateVideoWithoutMedia.Input(**serializer.validated_data)
        use_case = CreateVideoWithoutMedia(
            DjangoORMVideoRepository(),
            DjangoORMCategoryRepository(),
            DjangoORMGenreRepository(),
            DjangoORMCastMemberRepository()
            )
       
        try:
            output = use_case.execute(input)
            final_output = CreateVideoOutputSerializer(output)
        except(InvalidVideo, RelatedEntitiesNotFound) as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(err)})
        
        return Response(status=status.HTTP_201_CREATED, data=final_output.data)
    
    def partial_update(self, request: Request, pk: UUID = None) -> Response:
        file = request.FILES["video_file"]
        content = file.read()
        content_type = file.content_type
        
        uploadVideo = UploadVideo(
            video_repo= DjangoORMVideoRepository(),
            storage_service=LocalStorage(),
            message_bus=MessageBus()
        )
        
        input = uploadVideo.Input(video_id=pk, file_name=file.name, content=content, content_type=content_type)
       
        try:
            uploadVideo.execute(input)
        except InvalidVideo:
            return Response(status=404)
       
        return Response(status=200)
            