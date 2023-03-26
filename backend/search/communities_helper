import networkx as nx
from community import best_partition
import json

from community import best_partition

def detect_community(json_paths):
    # 创建边列表
    edges = []
    for path in json_paths:
        for edge in path['edges']:
            # 如果边没有权重，则默认权重为1
            weight = edge.get('weight', 1)
            edges.append((edge['source'], edge['target'], weight))
    
    # 使用Louvain算法检测社区
    graph = nx.Graph(edges)
    partition = best_partition(graph)
    
    # 构建节点-社区字典
    node_community = {}
    for node, community in partition.items():
        node_community[node] = community
    
    return node_community
