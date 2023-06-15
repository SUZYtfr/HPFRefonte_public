from rest_framework.views import APIView
from rest_framework.response import Response

class ContactView(APIView):
    def post(self, request, *args, **kwargs):
        return Response()
