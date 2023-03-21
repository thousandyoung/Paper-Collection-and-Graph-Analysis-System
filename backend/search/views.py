from neomodel import Q, db

from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import *
from .utils import *
PAPERS_NUMBER_PER_PAGE = 10


@api_view(['GET'])
def paper_list(request):
    keyword = request.GET.get('keyword')
    page_number = request.GET.get('page')
    if not keyword:
        papers = Paper.nodes.order_by('-crawl_time')
    else:
        papers = Paper.nodes.filter(Q(title__icontains=keyword) | Q(abstract__icontains=keyword)).order_by('-crawl_time')
    paginator = Paginator(papers, PAPERS_NUMBER_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    papers_on_page = page_obj.object_list

    formatted_papers = []
    for paper in papers_on_page:
        formatted_paper = {
            'uid': paper.uid,
            'title': paper.title,
            'authors': [author.name for author in paper.authors.all()],
            'published_date': paper.published_date.isoformat(),
        }
        formatted_papers.append(formatted_paper)

    data = {
        'total_count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'papers': formatted_papers,
    }
    return JsonResponse(data)

@api_view(['GET'])
def paper_detail(request):
    # 获取论文id
    uid = request.GET.get('uid')
    # 查询neo4j数据库中的论文详细信息
    paper = Paper.nodes.get(uid=uid)

    if paper is None:
        return JsonResponse({'error': 'Paper not found'}, status=404)

    # 格式化论文详细信息
    formatted_paper = {
        'uid': paper.uid, 
        'title': paper.title,
        'abstract': paper.abstract,
        'link': paper.link,
        'published_date': paper.published_date.isoformat(),
        'authors': [{'name': author.name, 'department': author.department_name} for author in paper.authors.all()],
        'keywords': [keyword.name for keyword in paper.keywords.all()],
    }

    # 返回论文详细信息
    return JsonResponse(formatted_paper)


@api_view(['GET'])
def get_all_paths(request):
    start_node_name = request.GET.get('start_node_name')
    start_node_type = request.GET.get('start_node_type')
    
    end_node_name = request.GET.get('end_node_name')
    end_node_type = request.GET.get('end_node_type')


    relationship = request.GET.get('relationship')
    depth = request.GET.get('depth')
    shortest  = request.GET.get('shortest')
    path_finder = PathFinder()
    paths = path_finder.get_paths(
        start_node_name=start_node_name, 
        start_node_type=start_node_type, 
        end_node_name=end_node_name, 
        end_node_type=end_node_type, 
        relationship=relationship, 
        depth=depth,
        shortest=shortest
    )
    return JsonResponse({'paths': paths})


@api_view(['GET'])
def get_node_types(request):
    # 查询Neo4j中已有的节点类型
    query = "CALL db.labels()"
    results, _ = db.cypher_query(query)
    node_types = [label[0] for label in results]

    return JsonResponse({'node_types': node_types})

@api_view(['GET'])
def get_relationship_types(request):
    query = "CALL db.relationshipTypes()"
    results, _ = db.cypher_query(query)
    types = [result[0] for result in results]

    return JsonResponse({'types': types})