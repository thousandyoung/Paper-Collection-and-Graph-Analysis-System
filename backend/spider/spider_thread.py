import threading 
import csv
import time
import os
import re
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tqdm import tqdm
from datetime import datetime
from django.db import transaction

from .models import Spider
from .data_importer import import_data_from

class SpiderThread(threading.Thread):
    def __init__(self, spider:Spider):
        super().__init__()
        self.spider = spider
        opt = Options()
        opt.add_experimental_option('excludeSwitches',['enable-automation'])
        opt.add_argument('--headless')
        opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
        url = 'https://www.cnki.net/'
        self.driver = Chrome(options=opt)
        self.driver.get(url=url)
        self._stop_event = threading.Event()
    
    def run(self):
        try:
            if not os.path.exists('./Data'):
                os.mkdir('./Data')

            #等待url加载
            WaitForFive()

            KEYWORD = self.spider.keyword
            TOTAL_PAGES = self.spider.total_pages

            try:
                #主页搜索
                self.driver.find_element(By.ID,"txt_SearchText").send_keys(KEYWORD,Keys.ENTER)
                
            except:
                #非主页搜索
                self.driver.find_element(By.ID,'txt_search').clear()
                self.driver.find_element(By.ID,'txt_search').send_keys(KEYWORD,Keys.ENTER)

            for current_page in range (1, TOTAL_PAGES+1):
                try:
                    print(f'{self.spider.name}{KEYWORD} : 正在读取第{current_page}页!')

                    WaitForFive()
                    search_results_window_handle = self.driver.current_window_handle

                    # 获取论文列表
                    tr_list = self.driver.find_elements(By.CLASS_NAME,'odd')
                    print('trlen:', len(tr_list))

                    for tr in tqdm(tr_list):
                        item = {}
                        # 抓取标题
                        try:
                            title = tr.find_element(By.CLASS_NAME,'name').text
                        except:
                            title = "无标题"        
                        item['title'] = title
                        
                        #抓取论文链接
                        try:
                            link = tr.find_element(By.XPATH, "./td[@class='name']/a").get_attribute('href')
                        except:
                            link = ''
                        item['link'] = link

                        #抓取发表时间
                        try:
                            date = tr.find_element(By.XPATH, "./td[@class='date']").text
                        except:
                            date = ''
                        item['date'] = date

                        #记录爬取时间
                        now = datetime.now() # 获取当前时间
                        retrieve_time = now.strftime("%Y-%m-%d %H:%M:%S") # 将时间格式化为字符串
                        item['retrieve_time'] = retrieve_time

                        # 进入详情
                        SwitchToDetailWindow(self.driver, link)

                        # 抓取摘要
                        try:
                            abstract = self.driver.find_element(By.CLASS_NAME, 'abstract-text').text
                        except:
                            abstract = "无摘要"
                        item['abstract'] = abstract

                        #抓取关键字
                        try:
                            keywords = self.driver.find_elements(By.NAME, 'keyword')
                            keywords_list = []
                            for keyword in keywords:
                                remove_items = r"[.!+-=——,$%^，,。;？?、~@#￥%……&*《》<>「」{}【】()/\\\[\]'\"]"
                                keyword_text = re.sub(remove_items, '', keyword.text)
                                keywords_list.append(keyword_text)
                        except:
                            keywords_list = ["无关键词"]
                        item['keywords_list'] = keywords_list

                        

                        
                        wx_tit_element = self.driver.find_element(By.CLASS_NAME, 'wx-tit')
                        #抓取作者
                        try:
                            author_element = wx_tit_element.find_element(By.XPATH, './h3[1]')
                            author_elements_list = author_element.find_elements(By.TAG_NAME,'a')
                            author_names_list = []
                            for element in author_elements_list:
                                author_names_list.append(element.text)
                        except:
                            print("grab author failed")

                        #抓取作者从属机构
                        try:
                            department_element = wx_tit_element.find_element(By.XPATH, './h3[2]')
                            department_elements_list = department_element.find_elements(By.TAG_NAME, 'a')
                        except:
                            print("grap department failed")
                        department_names_list = []
                        for element in department_elements_list:
                            department_names_list.append(element.text)

                        #生成author-department的dict
                        author_department_dict = {}
                        # 去除非法字符
                        r = r"[1234567890 .!+-=——,$%^，,。？?、~@#￥%……&*《》<>「」{}【】()/\\\[\]'\"]"
                        for author in author_names_list:
                            for department in department_names_list:
                                # 1:小明1,华南理工大学1 2:小明 华南理工大学
                                if author[-1] == department[0] or author[-1] not in ['0','1','2','3','4','5','6','7','8','9']:
                                    author_name = re.sub(r, '', author)
                                    department_name = re.sub(r, '', department)
                                    author_department_dict[author_name] = department_name
                                    break
                        item['author_department_dict'] = author_department_dict
                        # print(item)

                        # 打开 CSV 文件，使用 utf-8-sig 编码以支持中文
                        csv_filename = './Data/{keyword}.csv'.format(keyword = KEYWORD)
                        # check if the CSV file exists
                        if not os.path.isfile(csv_filename):
                            with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
                                writer = csv.writer(f)
                                # 写入标题行
                                writer.writerow(['title', 'author', 'department', 'keywords', 'retrieve_date', 'abstract', 'published_date', 'url'])
                        # append data to the CSV file 
                        with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as f:
                            writer = csv.writer(f)
                            # 写入数据行
                            # 遍历作者字典，获取每个作者的名称和单位
                            for author, department in author_department_dict.items():
                                keywords_str = "|".join(keywords_list)
                                writer.writerow([title, author, department, keywords_str, retrieve_time, abstract, date, link])

                        SwitchToSearchResultWindow(self.driver,search_results_window_handle)
                        print('back',len(self.driver.window_handles))

                    # check if the spider is stopped
                    if self.stopped():
                        raise Exception("thread stopped")
                    #本页抓取完毕，点击下一页
                    with transaction.atomic():
                        self.spider.current_page = current_page
                        self.spider.progress = int(current_page / TOTAL_PAGES * 100)
                        print(f'{self.spider.name} progress : {self.spider.progress}')
                        self.spider.save()
                    if HasNextPage(self.driver) == True:
                        self.driver.find_element(By.ID, 'PageNext').click()
                        WaitForFive()
                        search_results_window_handle = self.driver.current_window_handle

                    else:
                        print("have no next page")
                        break

                except:
                    raise Exception('定位失败')

        except Exception as e:
            with transaction.atomic():
                print(e)
                self.spider.status = "FAILED"
                self.spider.save()
        else:
            with transaction.atomic():
                self.spider.status = "COMPLETED"
                self.spider.save()
            #存入数据库
            csv_filename = './Data/{keyword}.csv'.format(keyword = self.spider.keyword)
            import_data_from(csv_path=csv_filename)
        finally:
            self.driver.quit()
            f.close()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def WaitForFive():
    time.sleep(5)

# 判断是否存在下一页
def HasNextPage(web):
    try:
        web.find_element(By.ID,"PageNext")
        return True
    except:
        print("have no next page")
        return False


def SwitchToDetailWindow(web, url):
    try:
        # web.get(url)
        web.execute_script("window.open('');")
        print("open blank window")
        web.switch_to.window(web.window_handles[-1])
        web.get(url)
        print('switch to new window')
        WaitForFive()
    except:
        print("switch to detail window failed")

def SwitchToSearchResultWindow(web, window_handle):
    try:
        web.close()
        WaitForFive()
        web.switch_to.window(window_handle)
        WaitForFive()
    except:
        print("switch to search result window failed")
   