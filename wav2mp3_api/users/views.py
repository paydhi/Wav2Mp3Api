from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import CreateUserSerializer, ResponseUserSerializer


class CreateUserView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = ResponseUserSerializer(instance=user)
        return Response(response_serializer.data, status=201)
