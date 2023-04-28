from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ParaphraseSerializer

from utils import generator_noun_paraphrases


class ParaphraseAPIView(APIView):
    allowed_params = ['tree', 'limit']
    serializer_class = ParaphraseSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        tree = data.get('tree')
        limit = data.get('limit')

        paraphrases = generator_noun_paraphrases(tree, limit=limit)
        response_data = [{'tree': par} for par in paraphrases]

        return Response({'paraphrases': response_data})

