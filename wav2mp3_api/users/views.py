from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import CreateUserSerializer
from users.models import User
import uuid


class CreateUserView(APIView):

    def post(self, request):
        post_user_serializer = CreateUserSerializer(data=request.data)

        if not post_user_serializer.is_valid():
            return Response(post_user_serializer.errors, status=400)

        if User.objects.filter(username=request.data.get('username')).exists():
            return Response({'error': 'Username already exists'}, status=400)

        username = request.data.get('username')

        user = {'username': username,
                'access_token': str(uuid.uuid4()),
                'user_uuid': str(uuid.uuid4())}

        user = User(**user)
        user.save()

        return Response({'access token': user.access_token, 'uuid': user.user_uuid}, status=201)
