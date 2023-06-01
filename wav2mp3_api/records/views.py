import os

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
        user = User.objects.get(user_uuid=request.data.get('user_uuid'))

        file = request.FILES['file']
        suffix = f'_{request.data.get("user_uuid")[:4]}.mp3'
        filename_mp3 = file.name.replace(".wav", suffix)

        record_mp3 = BytesIO()
        record = AudioSegment.from_wav(BytesIO(file.read()))
        record.export(record_mp3, format='mp3')
        record_mp3.seek(0)
        record_to_save = ContentFile(record_mp3.read(), name=filename_mp3)

        Record.objects.create(record=record_to_save, user=user)

        return Response({'status': 'success'})
