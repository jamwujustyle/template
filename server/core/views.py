from rest_framework.views import APIView
from rest_framework import status, response
from rest_framework.permissions import AllowAny


class Mock(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data_to_return = {
            "name": "wind",
            "age": 23,
            "specialty": "developer",
        }

        return response.Response(data_to_return, status=status.HTTP_200_OK)
