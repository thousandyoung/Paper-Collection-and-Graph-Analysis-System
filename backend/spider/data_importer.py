import csv
import sys
sys.path.append('..')
from search.models import Paper, Author, Department, Keyword
from datetime import datetime

#将csv数据导入数据库
def import_data_from(csv_path):
    # 打开 CSV 文件并读取其中的数据
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 查询或创建文章节点
            published_date = datetime.strptime(row['published_date'], '%Y-%m-%d')
            crawl_time = datetime.strptime(row['retrieve_date'], '%Y-%m-%d %H:%M:%S')
            try:
                print('row title', row['title'])
                paper = Paper.nodes.filter(title=row['title']).first()
                print('has paper ', paper.title)
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
            
            # 如果文章和作者没有关系，则创建 WROTE 关系
            if not paper.authors.is_connected(author):
                paper.authors.connect(author)
            
            # 建立 Author 和 Department 之间的关系
            if not author.department.is_connected(department):
                author.department.connect(department)
