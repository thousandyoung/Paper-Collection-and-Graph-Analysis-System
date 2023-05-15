import React, { useState, useEffect } from 'react';
import { Form, Input, Select, Button, Checkbox, Alert, InputNumber } from 'antd';
import { fetchData, fetchKnowledgeGraphData } from '../services/KnowledgeGraphService.js';

import KnowledgeGraph from '../components/KnowledgeGraph.js';

const { Option } = Select;

function KnowledgeGraphPage() {
  const [startNodeTypes, setStartNodeTypes] = useState([]);
  const [relationTypes, setRelationTypes] = useState([]);
  const [endNodeTypes, setEndNodeTypes] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [shortest, setShortest] = useState(false);
  const [depth, setDepth] = useState(1);
  const [graphData, setGraphData] = useState(null);

  // Fetch the node types, relation types and end node types from the API on component mount
  useEffect(() => {
    fetchData()
      .then(data => {
        // console.log('data:', data);
        setStartNodeTypes(data.startNodeTypes);
        setRelationTypes(data.relationTypes);
        setEndNodeTypes(data.endNodeTypes);
      })
      .catch(error => {
        setError(error.message);
      });
  }, []);


  // Handle form submit
  async function handleSubmit(values) {
    setIsLoading(true);
    console.log(values);
    try {
      const response = await fetchKnowledgeGraphData(values);
      console.log('paths', response);

      // Process the response data and display it on the page
      const processedData = processResponseData(response);
      setGraphData(processedData);

      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setError('Failed to fetch knowledge graph data');
      setIsLoading(false);
    }
  }

  // Convert response data to graph data format 立即触发渲染
  function processResponseData(response) {
    const graphData = {
      nodes: [],
      links: [],
    };


    response.paths.forEach(path => {
      path.nodes.forEach(node => {
        if (!graphData.nodes.some(n => n.id === node.id)) {
          graphData.nodes.push({
            id: node.id,
            label: node.label,
            ...node,
          });
        }
      });

      path.edges.forEach(edge => {
        if (!graphData.links.some(link => link.id === edge.id)) {
          graphData.links.push({
            id: edge.id,
            source: edge.source,
            target: edge.target,
            label: edge.type,
            ...edge,
          });
        }
      });
    });

    return graphData;
  }

  return (
    <div>
      <h1>Knowledge Graph</h1>
      <Form onFinish={(values) => {
        values.shortest = shortest;
        handleSubmit(values)
      }}>
        <Form.Item label="Start Node Name" name="start_node_name">
          <Input />
        </Form.Item>
        <Form.Item label="Start Node Type" name="start_node_type">
          <Select>
            <Option value="">--Select a type--</Option>
            {startNodeTypes && startNodeTypes.map((nodeType) => (
              <Option key={nodeType.id} value={nodeType.name}>
                {nodeType.name}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item label="Relation Type" name="relation_type">
          <Select>
            <Option value="">--Select a type--</Option>
            {relationTypes && relationTypes.map((relationType) => (
              <Option key={relationType.id} value={relationType.name}>
                {relationType.name}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item label="End Node Name" name="end_node_name">
          <Input />
        </Form.Item>
        <Form.Item label="End Node Type" name="end_node_type">
          <Select>
            <Option value="">--Select a type--</Option>
            {endNodeTypes && endNodeTypes.map((nodeType) => (
              <Option key={nodeType.id} value={nodeType.name}>
                {nodeType.name}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item label="Depth" name="depth">
          <InputNumber min={1} onChange={(value) => setDepth(value)} />
        </Form.Item>
        <Form.Item label="Shortest" name="shortest">
          <Checkbox checked={shortest} onChange={(e) => setShortest(e.target.checked)}>Shortest</Checkbox>
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={isLoading}>
            {isLoading ? 'Loading...' : 'Submit'}
          </Button>
        </Form.Item>
      </Form>
      {error && <Alert message={error} type="error" />}
      {graphData && Object.keys(graphData).length > 0 && <KnowledgeGraph paths={graphData} />}
    </div>
  );
}

export default KnowledgeGraphPage;
