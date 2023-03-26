import csv
import sys
sys.path.append('..')
from search.models import Paper, Author, Department, Keyword
from datetime import datetime
from itertools import combinations

#将csv数据导入数据库
def import_data_from(csv_path):
    # 打开 CSV 文件并读取其中的数据
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 查询或创建文章节点
            try:
                # 尝试解析带有完整时间的日期字符串
                published_date = datetime.strptime(row['published_date'].strip(), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # 解析不了带有完整时间的日期字符串，则尝试只解析日期部分
                published_date = datetime.strptime(row['published_date'].strip().split()[0], '%Y-%m-%d')
                # 将时间部分用默认值填充
                published_date = published_date.replace(hour=0, minute=0, second=0)

            try:
                # 尝试解析带有完整时间的日期字符串
                crawl_time = datetime.strptime(row['retrieve_date'].strip(), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # 解析不了带有完整时间的日期字符串，则尝试只解析日期部分
                crawl_time = datetime.strptime(row['retrieve_date'].strip().split()[0], '%Y-%m-%d')
                # 将时间部分用默认值填充
                crawl_time = crawl_time.replace(hour=0, minute=0, second=0)
            
            try:
                # print('row title', row['title'])
                paper = Paper.nodes.filter(title=row['title']).first()
                # print('has paper ', paper.title)
            except:
                paper = Paper(
                    title= row['title'],
                    abstract= row['abstract'],
                    link= row['url'],
                    published_date= published_date,
                    crawl_time = crawl_time
                ).save()
           
            
            # 查询或创建作者节点
            author_name = row['author']
            department_name = row['department']
            try:
                author = Author.nodes.filter(name=author_name, department_name=department_name).first()
            except:
                author = Author(name=author_name, department_name=department_name).save()
        
            
            # 创建 Department 节点
            department_name = row['department']
            try:
                department = Department.nodes.filter(name= department_name).first()
            except:
                department = Department(name= department_name).save()
            
            # 创建或获取 Keyword 节点
            keyword_names = row['keywords'].split('|')
            for keyword_name in keyword_names:
                try: 
                    keyword = Keyword.nodes.filter(name= keyword_name).first()
                except:
                    keyword = Keyword(name= keyword_name.strip()).save()
                
                # 如果文章和关键词没有关系，则创建 HAS_KEYWORD 关系
                if not paper.keywords.is_connected(keyword):
                    paper.keywords.connect(keyword)

            # 获取该论文下所有关键字
            keywords = paper.keywords
            # 遍历关键字，两两添加共现关系
            for i in range(len(keywords)):
                for j in range(i+1, len(keywords)):
                    k1, k2 = keywords[i], keywords[j]
                    rel = k1.co_occurrence.relationship(k2)
                    # 如果关键字之间没有共现关系，则创建一个
                    if not rel:
                        rel = k1.co_occurrence.connect(k2)
                        # 设置反向关系以确保生成无向边
                        k2.co_occurrence.connect(k1, {'CO_OCCURRENCE': rel})
                    # 将共现关系权重加 1
                    rel.weight = (rel.weight or 0) + 1
                    rel.save()

            # 如果文章和作者没有关系，则创建 WROTE 关系
            if not paper.authors.is_connected(author):
                paper.authors.connect(author)
            
            # 建立 Author 和 Department 之间的关系
            if not author.department.is_connected(department):
                author.department.connect(department)
