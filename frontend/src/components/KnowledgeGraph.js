import React, { useRef, useEffect } from 'react';
import {init} from 'echarts';

function KnowledgeGraph({ paths }) {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    const chart = init(chartRef.current);

    const graph = {
      nodes: paths.nodes.map(node => ({ 
        ...node, 
        category: node.label 
      })),
      links: paths.links.map(link => ({ 
        ...link, 
        lineStyle: { 
          color: 'gray',
          type: 'dashed',
        } 
      })),
      categories: paths.nodes.map(node => ({ 
        name: node.label 
      }))
    };

    chart.setOption({
      series: [{
        type: 'graph',
        layout: 'force',
        roam: true,
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 6],
        label: {
          show: true,
          position: 'bottom',
          color: 'gray',
        },
        emphasis: {
          label: {
            show: true,
          }
        },
        force: {
          repulsion: 200,
          edgeLength: 120,
        },
        data: graph.nodes,
        links: graph.links,
        categories: graph.categories,
      }],
    });

    return () => chart.dispose();
  }, [paths]);

  return <div ref={chartRef} style={{ height: '600px' }}></div>;
}

export default KnowledgeGraph;
