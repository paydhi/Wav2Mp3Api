from io import BytesIO

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.urls import reverse
from loguru import logger
from pydub import AudioSegment
from pydub.exceptions import PydubException
from rest_framework.exceptions import APIException

from records.models import Record
from users.models import User


def convert_wav_to_mp3(file, *args, **kwargs):
    try:
        filename_mp3 = file.name.replace('.wav', '.mp3')
        record_mp3 = BytesIO()
        record_wav = AudioSegment.from_wav(BytesIO(file.read()))
        record_wav.export(record_mp3, format='mp3')
        record_mp3.seek(0)
        record_to_save = ContentFile(record_mp3.read(), name=filename_mp3)
    except PydubException:
        logger.error('Failed to convert audio, not valid wav file or corrupted file')
        raise APIException('Invalid file')
    return record_to_save


def get_download_url(request, record, user, *args, **kwargs):
    download_url = request.build_absolute_uri(
        reverse('download_record') + f'?id={record.record_uuid}&user={user.user_uuid}')
    return download_url


def get_user(user_uuid, *args, **kwargs):
    user = User.objects.filter(user_uuid=user_uuid).first()
    return user


def validate_user(user, *args, **kwargs):
    if not user:
        logger.error(f'User not found')
        raise APIException('User not found')


def validate_access_token(validated_serializer, user, *args, **kwargs):
    access_token = validated_serializer.validated_data.get('access_token')
    if not user.access_token == access_token:
        logger.error(f'Access token for user with uuid {user.user_uuid} does not match')
        raise APIException('Access token does not match')
    pass


def get_record(record_uuid, *args, **kwargs):
    record = Record.objects.filter(record_uuid=record_uuid).first()
    if not record:
        logger.error(f'Record with uuid {record_uuid} not found')
        raise APIException('Record not found')
    return record


def generate_download_response(record, *args, **kwargs):
    filename = record.record.name.removeprefix('uploads/')
    response = HttpResponse(record.record, content_type='audio/mpeg')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
