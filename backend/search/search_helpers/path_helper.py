from neomodel import db
import time, string, ast

class Neo4jToJson:    
    def content_to_json(self, content):
        # print(content)
        open_content = content[0]
        if open_content is None or len(open_content) == 0 or open_content[0] is None or len(open_content[0]) == 0:
            return  {
            "nodes": "",
            "edges": "",
        }
        if type(open_content[0]) == list:
            return self.nodes_and_rels_to_json(content=open_content)
        else:
            return self.path_to_json(paths=content)
        
    def nodes_and_rels_to_json(self, content):
        json_paths = []
       
        nodes = []
        edges = []
        # print(content)
        path_nodes = content[0]
        path_relationships = content[1]
        # print(path_relationships)
        for i, node in enumerate(path_nodes):
            # 构建节点数据  
            node_data = {"id": str(node.id), "label": list(node.labels)[0]}
            node_data.update(node._properties)
            nodes.append(node_data)
            
        # 构建关系数据
        for relationship in path_relationships:
            edge_data = {
                "id": str(relationship.id),
                "type": str(relationship.type),
                "source": str(relationship.nodes[0].id),
                "target":str(relationship.nodes[1].id),
            }
            edge_data.update(relationship._properties)
            edges.append(edge_data)
        
        # 构建 JSON 格式响应
        json_path = {
            "nodes": nodes,
            "edges": edges,
        }
        json_paths.append(json_path)
        return json_paths
    
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
                "nodes": nodes,
                "edges": edges,
            }
            json_paths.append(json_path)
        return json_paths

# 路径发现的所有情况
# 1、与起始节点相连的所有路径
# 2、与起始节点通过某关系相连的所有路径
# 3、起始节点通过某关系与终止节点相连的路径
# 4、与终止节点相连的所有路径
# 5、与终止节点通过某关系相连的所有路径
# 6、起始节点与终止节点之间的所有路径
# 7、通过某关系相连的所有路径
# 8、所有路径

class PathFinder:

    def get_paths(self, start_node_name=None, start_node_type=None, end_node_name=None, end_node_type=None, relationship=None, depth=None, shortest=None):
    
        if (not start_node_name and start_node_type) or (start_node_name and not start_node_type):
            raise ValueError("start_node_type and start_node_name must occur together")

        if (not end_node_name and end_node_type) or (end_node_name and not end_node_type):
            raise ValueError("end_node_type and end_node_name must occur together")

        if shortest == True:
            shortest_query = 'allshortestpaths'
        else:
            shortest_query = ""

        if relationship is not None:
            relationship_query = f":{relationship}*"
        else:
            relationship_query = "*"

        if start_node_name is not None:
            if start_node_type != 'Paper':
                start_node_query = f":{start_node_type} {{name: '{start_node_name}'}}"
            else:
                start_node_query = f":{start_node_type} {{title: '{start_node_name}'}}"
        else:
            start_node_query = ""

        if end_node_name is not None:
            if end_node_type != 'Paper':
                end_node_query = f":{end_node_type} {{name: '{end_node_name}'}}"
            else:
                end_node_query = f":{end_node_type} {{title: '{end_node_name}'}}"
        else:
            end_node_query = ""
        
        if depth is not None:
            depth_query = f"..{depth}"
        else:
            # 针对情况8，展示所有路径的情况进行优化
            if start_node_query == "" and end_node_query == "":
                depth_query = "..1"
            else:
                depth_query = ""

        query = self.construct_find_path_query(start_node_query, end_node_query, relationship_query, depth_query, shortest_query)
        print(query)

        start_time = time.time()
        results, _ = db.cypher_query(query)
        end_time = time.time()
        execution_time = end_time - start_time  
        print("执行时间：", execution_time, "秒")
        print(results)
        
        json_converter = Neo4jToJson()
        return json_converter.path_to_json(paths=results)

    def construct_find_path_query(self, start_node="", end_node="", relationship="", depth_query="", shortest=""):
        if shortest == True and depth_query != "":
            raise ValueError("allshortestpaths can't be used with depth arguments")

        if start_node is not None and start_node != "" and end_node is not None and end_node != "":
            #情况3，6
            query = f"MATCH p={shortest}(({start_node})-[{relationship}{depth_query}]-({end_node})) RETURN DISTINCT p LIMIT 2000"
        else:
            #其他所有情况
            query = f"MATCH p=({start_node})-[{relationship}{depth_query}]-({end_node}) RETURN DISTINCT p LIMIT 2000"

        return query
    
class OptimizedPathFinder:

    def get_paths(self, start_node_name=None, start_node_type=None, end_node_name=None, end_node_type=None, relationship=None, depth=None, shortest=None):

        if (not start_node_name and start_node_type) or (start_node_name and not start_node_type):
            raise ValueError("start_node_type and start_node_name must occur together")

        if (not end_node_name and end_node_type) or (end_node_name and not end_node_type):
            raise ValueError("end_node_type and end_node_name must occur together")

        if shortest == True:
            shortest_query = 'use_shortest_option'
        else:
            shortest_query = ""

        if relationship is not None:
            relationship_query = f"{relationship}"
        else:
            relationship_query = ""

        if start_node_name is not None:
            if start_node_type != 'Paper':
                start_node_query = f":{start_node_type} {{name: '{start_node_name}'}}"
            else:
                start_node_query = f":{start_node_type} {{title: '{start_node_name}'}}"
        else:
            start_node_query = ""

        if end_node_name is not None:
            if end_node_type != 'Paper':
                end_node_query = f":{end_node_type} {{name: '{end_node_name}'}}"
            else:
                end_node_query = f":{end_node_type} {{title: '{end_node_name}'}}"
        else:
            end_node_query = ""
        
        if depth is not None:
            depth_query = f",maxLevel: {depth}"
            depth_number_query = f",{depth}"
        else:
            depth_query = ""
            depth_number_query = ""
        query = self.construct_find_path_query(start_node_query, end_node_query, relationship_query, depth_query, shortest_query, depth_number_query)
        
        start_time = time.time()
        results, _ = db.cypher_query(query)
        # print(results)
        print(query)
        end_time = time.time()
        execution_time = end_time - start_time  
        print("执行时间：", execution_time, "秒")
        
        json_converter = Neo4jToJson()
        return json_converter.content_to_json(content=results)
    
    def construct_find_path_query(self, start_node="", end_node="", relationship="", depth_query="", shortest="", depth_number_query=""):
        if shortest == True and depth_query != "":
            raise ValueError("allshortestpaths can't be used with depth arguments")
        if start_node != "" and end_node != "":
            if shortest == "":
                if relationship != "":
                    #情况3 spanningTree支持关系定制
                    query = f"""MATCH (start_node{start_node})
                                MATCH (end_node{end_node})
                                CALL apoc.path.spanningTree(start_node, {{
                                    relationshipFilter: "{relationship}"
                                    ,terminatorNodes: [end_node]
                                    ,limit: 1000
                                    {depth_query}
                                }})
                                YIELD path
                                RETURN path;
                            """
                else:
                    #情况6 allSimplePaths不关心关系，只关心节点
                    query = f"""MATCH (start_node{start_node})
                                MATCH (end_node{end_node})
                                CALL apoc.algo.allSimplePaths(start_node,
                                    end_node,
                                    '',
                                    500
                                )
                                YIELD path
                                RETURN path;
                            """
                    
            else:
                #最短路径只在有起始节点和终止节点的情况下有意义
                # query = f"""MATCH (start_node{start_node})
                #             MATCH (end_node{end_node})
                #             CALL apoc.algo.shortestPath(start_node,end_node,null)
                #             YIELD path
                #             RETURN path;
                #         """
                # print(query)
                query = f"MATCH p=allshortestpaths(({start_node})-[]-({end_node})) RETURN DISTINCT p LIMIT 2000"
        elif start_node != "":
            if relationship != "":
                #情况2
                relationship_query = f"relationshipFilter: \"{relationship}>\""
            else:
                #情况1
                relationship_query = f""
                
            query = f"""MATCH (start_node{start_node})
                        CALL apoc.path.subgraphAll(start_node, {{
                            {relationship_query}
                            ,limit: 2000
                            {depth_query}

                        }})
                        YIELD nodes, relationships
                        RETURN nodes, relationships;
                    """
         
        elif end_node != "":
            if relationship != "":
                #情况5
                relationship_query = f"relationshipFilter: \"{relationship}\""
            else:
                #情况4
                relationship_query = f""

            query = f"""MATCH (end_node{end_node})
                    CALL apoc.path.subgraphAll(end_node, {{
                        {relationship_query}
                        ,limit: 2000
                        {depth_query}
                    }})
                    YIELD nodes, relationships
                    RETURN nodes, relationships;
                """
        else:
            if relationship != "":
                #情况7
                query = f"MATCH p=()-[:{relationship}*..1]-() RETURN DISTINCT p LIMIT 2000"
            else:
                #情况8
                query = f"""MATCH p=()-[*..1]->()
                            RETURN distinct p limit 2000;
                        """
        return query