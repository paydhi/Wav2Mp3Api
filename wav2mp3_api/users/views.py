from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import CreateUserSerializer, ResponseUserSerializer
from loguru import logger
from users.models import User


class CreateUserView(APIView):

    def post(self, request):
        post_user_serializer = CreateUserSerializer(data=request.data)

        if not post_user_serializer.is_valid():
            return Response(post_user_serializer.errors, status=400)

        if User.objects.filter(username=request.data.get('username')).exists():
            return Response({'error': 'Username already exists'}, status=400)

        username = request.data.get('username')
        user = User(username=username)
        user.save()

        response_data = {'access_token': str(user.access_token), 'user_uuid': str(user.user_uuid)}
        logger.info(response_data)

        response_serializer = ResponseUserSerializer(data=response_data)

        if response_serializer.is_valid(raise_exception=True):
            logger.info(f'User {username} created successfully')
            logger.info(response_serializer.data)
            logger.info(response_serializer.errors)
            logger.info(response_serializer.validated_data)

            return Response(response_serializer.validated_data, status=201)
        else:
            return Response(response_serializer.errors, status=201)
