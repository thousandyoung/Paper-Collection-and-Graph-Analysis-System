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


# import threading
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
# from .models import Spider

# #所有爬虫的列表
# def index(request):
#     spiders = Spider.objects.all()
#     context = {"spiders": spiders}
#     return render(request, "index.html", context)


# #处理新增爬虫的请求，并在新开线程执行爬虫功能
# @csrf_exempt
# def add_spider(request):
#     if request.method == "POST":
#         keyword = request.POST.get("keyword")
#         name = request.POST.get("name")
#         total_pages = request.POST.get("total_pages")
#         spider = Spider(keyword=keyword, name=name, total_pages=total_pages)
#         spider.save()
#         spider.start()
#         return redirect("index")
#     else:
#         return render(request, "add_spider.html")


# #根据爬虫ID查询对应的爬虫并渲染其状态和进度；
# def monitor(request, spider_id):
#     spider = Spider.objects.get(id=spider_id)
#     progress = spider.progress
#     status = spider.status
#     context = {"spider": spider, "progress": progress, "status": status}
#     return render(request, "monitor.html", context)


# #根据爬虫ID删除对应的爬虫，如果爬虫正在运行，则先停止对应的线程。
# def delete_spider(request, spider_id):
#     spider = Spider.objects.get(id=spider_id)
#     if spider.status == "RUNNING":
#         spider.stop()
#     spider.delete()
#     return redirect("index")