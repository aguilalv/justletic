from rest_framework.views import APIView
from rest_framework.response import Response

from keys.models import Key
from .serializers import KeySerializer

class KeyDetail(APIView):
    """Retrieve a Key instance"""

    def get(self,request):
        key = Key.objects.filter(user__pk=request.user.pk).first()
        serializer = KeySerializer(key)
        return Response(serializer.data)
