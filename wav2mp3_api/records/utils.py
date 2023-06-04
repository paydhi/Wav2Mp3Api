from io import BytesIO

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.urls import reverse
from loguru import logger
from pydub import AudioSegment
from pydub.exceptions import PydubException
from rest_framework.exceptions import APIException
from rest_framework.request import Request

from records.models import Record
from records.serializers import UploadRecordSerializer
from users.models import User


def convert_wav_to_mp3(file: ContentFile, *args, **kwargs) -> ContentFile:
    """
    Convert wav file to mp3
    :param file: File from request
    :return: ContentFile instance of mp3 file
    :exception: PydubException if Pydub could not convert file to mp3
    """
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


def get_download_url(request: Request, record: Record, user: User, *args, **kwargs) -> str:
    """
    Get download url for record
    :param request: request to generate download url
    :param record: Record instance
    :param user: User instance
    :return: String of absolute url to download file
    """
    download_url = request.build_absolute_uri(
        reverse('download_record') + f'?id={record.record_uuid}&user={user.user_uuid}')
    return download_url


def get_user(user_uuid: str, *args, **kwargs) -> User:
    """
    Get user instance
    :param user_uuid: uuid of user
    :return: User instance
    """
    user = User.objects.filter(user_uuid=user_uuid).first()
    return user


def validate_user(user, *args, **kwargs):
    """
    Validate user
    :param user: User instance to validate
    :exception: APIException if user is Null
    """
    if not user:
        logger.error(f'User not found')
        raise APIException('User not found')


def validate_access_token(validated_serializer: UploadRecordSerializer, user: User, *args, **kwargs) -> None:
    """
    Validate access token of user
    :param validated_serializer: serializer.is_valid() instance
    :param user: User instance
    :exception: APIException if access token does not match
    """
    access_token = validated_serializer.validated_data.get('access_token')
    if not user.access_token == access_token:
        logger.error(f'Access token for user with uuid {user.user_uuid} does not match')
        raise APIException('Access token does not match')
    pass


def get_record(record_uuid: str, *args, **kwargs) -> Record:
    """
    Get record from database
    :param record_uuid: uuid of record
    :return: Record instance
    :exception: APIException if record not found
    """
    record = Record.objects.filter(record_uuid=record_uuid).first()
    if not record:
        logger.error(f'Record with uuid {record_uuid} not found')
        raise APIException('Record not found')
    return record


def generate_download_response(record: Record, *args, **kwargs) -> HttpResponse:
    """
    Generate response for download from browser
    :param record: Record instance
    :return: HttpResponse
    """
    filename = record.record.name.removeprefix('uploads/')
    response = HttpResponse(record.record, content_type='audio/mpeg')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
