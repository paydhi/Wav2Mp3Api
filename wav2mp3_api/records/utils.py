from io import BytesIO
from uuid import UUID

from django.core.files.base import ContentFile
from django.urls import reverse
from pydub import AudioSegment


def convert_wav_to_mp3(file, *args, **kwargs):
    filename_mp3 = file.name.replace('.wav', '.mp3')

    record_mp3 = BytesIO()
    record_wav = AudioSegment.from_wav(BytesIO(file.read()))
    record_wav.export(record_mp3, format='mp3')
    record_mp3.seek(0)

    record_to_save = ContentFile(record_mp3.read(), name=filename_mp3)
    return record_to_save


def get_download_url(request, record, user, *args, **kwargs):
    download_url = request.build_absolute_uri(
        reverse('download_record') + f'?id={record.record_uuid}&user={user.user_uuid}')
    return download_url


def is_valid_uuid(uuid_string):
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False
