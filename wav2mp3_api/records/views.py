from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser

from loguru import logger


class UploadRecordView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser)

    def post(self, request):
        # TODO: fix file upload
        file = request.FILES.get('file')
        logger.info(f'file: {file}')
        data = {'user_uuid': request.data.get('user_uuid'),
                'access_token': request.data.get('access_token')}
        logger.info(f'data: {data}')

        return Response({'status': 'success'})
