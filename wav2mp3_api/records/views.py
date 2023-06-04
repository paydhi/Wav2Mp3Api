from rest_framework.response import Response
from rest_framework.views import APIView

from records.models import Record
from records.serializers import UploadRecordSerializer, DownloadRecordSerializer
from records.utils import convert_wav_to_mp3, get_download_url, validate_access_token, get_record, validate_user, \
    get_user, generate_download_response


class UploadRecordView(APIView):
    serializer_class = UploadRecordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_uuid = serializer.validated_data.get('user_uuid')
        user = validate_user(get_user(user_uuid))
        validate_access_token(serializer, user)

        file = convert_wav_to_mp3(serializer.validated_data.get('file'))
        record = Record.objects.create(record=file, user=user)

        download_url = get_download_url(request, record, user)
        response = Response({'download_url': download_url}, status=201)
        return response


class DownloadRecordView(APIView):
    serializer_class = DownloadRecordSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        validate_user(get_user(serializer.validated_data.get('user')))

        record_uuid = serializer.validated_data.get('id')
        record = get_record(record_uuid)
        response = generate_download_response(record)
        return response
