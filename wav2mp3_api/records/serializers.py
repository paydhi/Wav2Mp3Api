from rest_framework import serializers


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
