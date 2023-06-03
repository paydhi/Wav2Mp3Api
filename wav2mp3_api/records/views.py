from django.http import HttpResponse
from pydub.exceptions import PydubException

from rest_framework.response import Response
from rest_framework.views import APIView

from loguru import logger
from records.models import Record
from records.serializers import UploadRecordSerializer, DownloadRecordSerializer
from users.models import User

from records.utils import convert_wav_to_mp3, get_download_url


class UploadRecordView(APIView):
    serializer_class = UploadRecordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_uuid = serializer.validated_data.get('user_uuid')
        access_token = serializer.validated_data.get('access_token')
        user_query = User.objects.filter(user_uuid=user_uuid)

        if not user_query.exists():
            logger.error(f'User with uuid {user_uuid} not found')
            return Response(data={'user_uuid': 'User not found'}, status=401)
        elif not user_query.first().access_token == access_token:
            logger.error(f'Access token for user with uuid {user_uuid} does not match')
            return Response(data={'access_token': 'Access token does not match'}, status=401)

        file = request.FILES.get('file')
        try:
            file = convert_wav_to_mp3(file)
        except PydubException:
            logger.error('Failed to convert audio, not valid wav file or corrupted file')
            return Response({'error': 'Invalid file'}, status=400)

        user = user_query.first()
        record = Record.objects.create(record=file, user=user)

        download_url = get_download_url(request, record, user)

        response = Response({'download_record': {'download_url': download_url,
                                                 'id': record.record_uuid,
                                                 'user': user.user_uuid}}, status=201)

        return response


class DownloadRecordView(APIView):
    serializer_class = DownloadRecordSerializer

    def get(self, request):
        serializer = self.serializer_class(data={'record_uuid': request.GET.get('id'),
                                                 'user_uuid': request.GET.get('user')})
        serializer.is_valid(raise_exception=True)
        record_uuid = serializer.validated_data.get('record_uuid')
        user_uuid = serializer.validated_data.get('user_uuid')

        record_query = Record.objects.filter(record_uuid=record_uuid)
        user_query = User.objects.filter(user_uuid=user_uuid)

        if not user_query.exists():
            logger.error(f'User with uuid {user_uuid} not found')
            return Response(data={'user_uuid': 'User not found'}, status=401)

        if not record_query.exists():
            logger.error(f'Record with uuid {record_uuid} not found')
            return Response(data={'record_uuid': 'Record not found'}, status=400)

        record = record_query.first()
        filename = record.record.name.removeprefix('uploads/')

        response = HttpResponse(record.record, content_type='audio/mpeg')
        logger.info(record.record.name)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
