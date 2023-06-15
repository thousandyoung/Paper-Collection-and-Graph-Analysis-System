import threading
from datetime import datetime
from django.db import models


class Spider(models.Model):
    keyword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    total_pages = models.IntegerField()
    current_page = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=[("PENDING", "Pending"), ("RUNNING", "Running"), ("COMPLETED", "Completed"), ("FAILED", "Failed")], default="PENDING"
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def start(self):
        self.status = "RUNNING"
        self.start_time = datetime.now()  # 记录开始时间
        self.save()
        from .spider_thread import SpiderThread
        spider_thread = SpiderThread(spider=self)
        print("spiderthread's spider: ", spider_thread.spider)
        spider_thread.start()

    def stop(self):
        if self.status == "RUNNING":
            self.status = "FAILED"
            self.end_time = datetime.now()  # 记录结束时间
            self.save()
            from .spider_thread import SpiderThread
            # find the corresponding thread and stop it
            for thread in threading.enumerate():
                if isinstance(thread, SpiderThread) and thread.spider.id == self.id:
                    thread.stop()#重写的stop,用于设置thread event
                    thread.join()
    
    def calculate_execution_time(self):
        if self.start_time and self.end_time:
            execution_time = self.end_time - self.start_time
            print("Execution time:", execution_time)