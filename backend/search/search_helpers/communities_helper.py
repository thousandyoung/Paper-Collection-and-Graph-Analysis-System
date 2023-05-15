import networkx as nx
from community import best_partition

from neomodel import db

from ..models import Keyword, Author

def find_communities():
    # 查询关键字节点
    query = 'MATCH (k:Keyword) RETURN k'
    result, _ = db.cypher_query(query)
    keywords = [Keyword.inflate(row[0]) for row in result]

    # 记录keyword id-name
    keyword_id_name_map = {}
    for keyword in keywords:
        keyword_id_name_map[keyword.id] = keyword.name
            
    # 创建一个无向图
    graph = nx.Graph()
    for keyword in keywords:
        graph.add_node(keyword.id)
    for keyword1 in keywords:
        query = f'MATCH (k1:Keyword)-[r:CO_OCCURRENCE]->(k2:Keyword) WHERE ID(k1)={keyword1.id} RETURN k2, r.weight'
        result, _ = db.cypher_query(query)
        for row in result:
            keyword2_id = row[0].id
            weight = row[1]
            if weight > 0:
                graph.add_edge(keyword1.id, keyword2_id, weight=weight)

    # 使用louvain算法查找社区
    partition = best_partition(graph)

    # 将节点和社区映射到字典
    keyword_communities = {}
    for keyword_id, community_id in partition.items():
        if community_id not in keyword_communities:
            keyword_communities[community_id] = []
        keyword_communities[community_id].append(keyword_id)

    # 将关键字社区映射到作者社区
    # 记录author id-name
    author_id_name_map = {}
    author_communities = {}
    for community_id, keyword_ids in keyword_communities.items():
        query = f'MATCH (a:Author)-[:WROTE]->(p:Paper)-[:HAS_KEYWORD]->(k:Keyword) WHERE ID(k) IN {keyword_ids} RETURN DISTINCT a'
        result, _ = db.cypher_query(query)
        authors = [Author.inflate(row[0]) for row in result]
        author_ids = set([author.id for author in authors])
        author_communities[community_id] = author_ids
        for author in authors:
            author_id_name_map[author.id] = author.name

    mapped_author_communities = {}
    for community_id, author_ids in author_communities.items():
        mapped_author_names = [author_id_name_map.get(author_id, author_id) for author_id in author_ids]
        mapped_author_communities[community_id] = mapped_author_names
    
    mapped_keyword_communities = {}
    for community_id, keyword_ids in keyword_communities.items():
        mapped_keyword_names = [keyword_id_name_map.get(keyword_id, keyword_id) for keyword_id in keyword_ids]
        mapped_keyword_communities[community_id] = mapped_keyword_names

    results = {'keyword_communities':mapped_keyword_communities, 'author_communities': mapped_author_communities}

    return results
