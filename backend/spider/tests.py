from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Spider
from .serializers import SpiderSerializer
import json

class SpidersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.spider_data_1 = {'name': 'Test Spider 1', 'keyword': 'test1', 'total_pages': 1}
        self.spider_data_2 = {'name': 'Test Spider 2', 'keyword': 'test2', 'total_pages': 1}
        self.response_1 = self.client.post('/spider/spiders/', self.spider_data_1, format='json')
        self.response_2 = self.client.post('/spider/spiders/', self.spider_data_2, format='json')
        # print('setup:')
        # print(self.response_1.status_code)
        # print(json.loads(self.response_1.content.decode('utf-8')))

    def test_create_spider(self):
        print('test_create_spider')
        self.assertEqual(self.response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response_2.status_code, status.HTTP_201_CREATED)
        

    def test_get_all_spiders(self):
        response = self.client.get('/spider/spiders/')
        spiders = Spider.objects.all()
        print('test_get_all_spiders', spiders)
        serializer = SpiderSerializer(spiders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_spider(self):
        spider = Spider.objects.first()
        response = self.client.get(f'/spider/spiders/{spider.id}/')
        serializer = SpiderSerializer(spider)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_spider(self):
    #     spider = Spider.objects.first()
    #     response = self.client.delete(f'/spider/spiders/{spider.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
