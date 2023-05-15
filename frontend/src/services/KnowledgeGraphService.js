import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:8000/search/';
const NODE_TYPES_URL = 'get_node_types/';
const RELATION_TYPES_URL = 'get_relationship_types/';
const PATHS_URL = 'get_all_paths/'

const fetchData = async () => {
  try {
    const nodeTypesResponse = await axios.get(API_BASE_URL + NODE_TYPES_URL);
    const relationTypesResponse = await axios.get(API_BASE_URL + RELATION_TYPES_URL);

    // console.log('nodeTypesResponse',nodeTypesResponse)

    if (!nodeTypesResponse.data || !relationTypesResponse.data) {
      throw new Error('Failed to fetch data');
    }

    return {
      startNodeTypes: nodeTypesResponse.data.node_types,
      relationTypes: relationTypesResponse.data.types,
      endNodeTypes: nodeTypesResponse.data.node_types
    };
  } catch (error) {
    console.error(error);
    throw new Error('Failed to fetch data');
  }
};



const fetchKnowledgeGraphData = async (params) => {
  try {
    const response = await axios.post(`${API_BASE_URL + PATHS_URL}`, {
      start_node_name: params.start_node_name,
      start_node_type: params.start_node_type,
      relation_type: params.relation_type,
      end_node_name: params.end_node_name,
      end_node_type: params.end_node_type,
      depth: params.depth,
      shortest: params.shortest,
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 50000 // 设置请求超时时间为5秒钟
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error('Failed to fetch knowledge graph data');
  }
};


export { fetchData, fetchKnowledgeGraphData };
