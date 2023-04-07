from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from expensecore.models import Tag
from expensecore.serializers.transaction_serializer import TagSerializer


class TagList(APIView):
    """
    List all tags, or create a new tag.
    """
    def get(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

