from neomodel import db

class Neo4jToJson:
    def path_to_json(self, paths):
        json_paths = []
        for path_list in paths:
            path = path_list[0]
            nodes = []
            edges = []
            for i, node in enumerate(path.nodes):
                # 构建节点数据
                node_data = {"id": str(node.id), "label": list(node.labels)[0]}
                node_data.update(node._properties)
                nodes.append(node_data)
                
                # 构建关系数据
                if i > 0:
                    edge_data = {
                        "id": str(path.relationships[i-1].id),
                        "type": path.relationships[i-1].type,
                        "source": str(path.nodes[i-1].id),
                        "target": str(path.nodes[i].id),
                    }
                    edge_data.update(path.relationships[i-1]._properties)
                    edges.append(edge_data)
            
            # 构建 JSON 格式响应
            json_path = {
                "start_node": str(path.start_node.id),
                "end_node": str(path.end_node.id),
                "nodes": nodes,
                "edges": edges,
            }
            json_paths.append(json_path)
        return json_paths


class PathFinder:

    def get_paths(self, start_node_name, start_node_type, end_node_name, end_node_type, relationship, depth, shortest):
        
        if shortest is not None:
            shortest_query = 'allshortestpaths'
        else:
            shortest_query = ""

        if depth is not None:
            depth_query = f"..{depth}"
        else:
            depth_query = ""

        if relationship is not None:
            relationship_query = f":{relationship}"
        else:
            relationship_query = "*"

        if start_node_name is not None:
            if start_node_type != 'Paper':
                start_node_query = f":{start_node_type} {{name: '{start_node_name}'}}"
            else:
                start_node_query = f":{start_node_type} {{title: '{start_node_name}'}}"
        else:
            start_node_query = None

        if end_node_name is not None:
            if end_node_type != 'Paper':
                end_node_query = f":{end_node_type} {{name: '{end_node_name}'}}"
            else:
                end_node_query = f":{end_node_type} {{title: '{end_node_name}'}}"
        else:
            end_node_query = None

        query = self.construct_find_path_query(start_node_query, end_node_query, relationship_query, depth_query, shortest_query)

        results, _ = db.cypher_query(query)
        json_converter = Neo4jToJson()
        return json_converter.path_to_json(paths=results)

    def construct_find_path_query(self, start_node, end_node, relationship, depth_query, shortest):
        if start_node is not None and end_node is not None:
            query = f"MATCH p={shortest}(({start_node})-[{relationship}{depth_query}]-({end_node})) RETURN p"
        elif start_node is not None:
            query = f"MATCH p={shortest}(({start_node})-[{relationship}{depth_query}]-(n)) RETURN p"
        else:
            query = f"MATCH p={shortest}((n)-[{relationship}{depth_query}]-({end_node})) RETURN p"
        return query