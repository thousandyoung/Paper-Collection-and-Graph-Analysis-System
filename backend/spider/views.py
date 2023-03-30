from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Spider
from .serializers import SpiderSerializer


@api_view(['GET', 'POST'])
def spiders(request):
    if request.method == 'GET':
        spiders = Spider.objects.all()
        serializer = SpiderSerializer(spiders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SpiderSerializer(data=request.data)
        if serializer.is_valid():
            spider = serializer.save()
            spider.start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'DELETE'])
def spider(request, spider_id):
    try:
        spider = Spider.objects.get(id=spider_id)
    except Spider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpiderSerializer(spider)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if spider.status == 'RUNNING':
            spider.stop()
        spider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
