from rest_framework import serializers
from records.models import Record


class UploadRecordSerializer(serializers.Serializer):
    file = serializers.FileField()
    user_uuid = serializers.UUIDField()
    access_token = serializers.UUIDField()

    class Meta:
        fields = ['file', 'user_uuid', 'access_token']


class RecordUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['record_uuid', 'record']
