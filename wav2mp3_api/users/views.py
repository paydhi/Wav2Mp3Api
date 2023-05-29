from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import CreateUserSerializer, ResponseUserSerializer


class CreateUserView(APIView):

    def post(self, request):
        post_user_serializer = CreateUserSerializer(data=request.data)
        post_user_serializer.is_valid(raise_exception=True)
        user = post_user_serializer.save()
        response_serializer = ResponseUserSerializer(instance=user)
        return Response(response_serializer.data, status=201)
