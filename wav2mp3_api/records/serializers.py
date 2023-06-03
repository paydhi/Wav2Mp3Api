from rest_framework import serializers

from users.models import User


class InvalidUUIDException(serializers.ValidationError):
    status_code = 401
    default_detail = 'Invalid UUID.'
    default_code = 'invalid_uuid'


class UploadRecordSerializer(serializers.Serializer):
    file = serializers.FileField()
    user_uuid = serializers.UUIDField()
    access_token = serializers.UUIDField()

    class Meta:
        fields = ['file', 'user_uuid', 'access_token']

    def validate_file(self, value):
        if not value.name.endswith('.wav'):
            raise serializers.ValidationError('Invalid file extension, must be .wav', code=400)
        return value


class DownloadRecordSerializer(serializers.Serializer):
    record_uuid = serializers.UUIDField()
    user_uuid = serializers.UUIDField()

    class Meta:
        fields = ['record_uuid', 'user_uuid']
