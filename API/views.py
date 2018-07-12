from rest_framework.views import APIView
from rest_framework.response import Response

class KeyDetail(APIView):
    """Retrieve a Key instance"""

    def get(self,request):
        print(f'---> {request.user}')
        return Response()
