import os

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from pydub import AudioSegment

from rest_framework.response import Response
from rest_framework.views import APIView

from loguru import logger
from records.models import Record
from records.serializers import UploadRecordSerializer
from users.models import User

from django.core.files.base import File, ContentFile
from io import BytesIO


class UploadRecordView(APIView):
    def post(self, request):
        if Record.objects.filter(user__user_uuid=request.data.get('user_uuid')).exists():
            Record.objects.filter(user__user_uuid=request.data.get('user_uuid')).delete()
            logger.info('Deleted all records for user %s', request.data.get('user_uuid'))

        file = request.FILES.get('file')
        suffix = f'_{request.data.get("user_uuid")[:4]}.mp3'
        filename_mp3 = file.name.replace(".wav", suffix)

        record_mp3 = BytesIO()
        record_wav = AudioSegment.from_wav(BytesIO(file.read()))
        record_wav.export(record_mp3, format='mp3')
        record_mp3.seek(0)

        record_to_save = ContentFile(record_mp3.read(), name=filename_mp3)
        user = User.objects.get(user_uuid=request.data.get('user_uuid'))
        record = Record.objects.create(record=record_to_save, user=user)
        download_url = request.build_absolute_uri(
           reverse('download_record') + f'?id={record.record_uuid}&user={user.user_uuid}')

        response = Response({'download_record': {'download_url': download_url,
                                                 'id': record.record_uuid,
                                                 'user': user.user_uuid}})

        return response


class DownloadRecordView(APIView):
    def get(self, request):
        record_uuid = request.GET.get('id')
        user_uuid = request.GET.get('user')

        record = get_object_or_404(Record, record_uuid=record_uuid, user__user_uuid=user_uuid)

        response = HttpResponse(record.record, content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename={record.record.name}'

        return response
