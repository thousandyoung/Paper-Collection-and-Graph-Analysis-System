import React, { useState } from 'react';
import { Button, Table } from 'antd';
import { getCommunityData } from '../services/CommunityDectionService';

const columns = [
  {
    title: 'Community ID',
    dataIndex: 'community_id',
    key: 'community_id',
  },
  {
    title: 'Keyword Community',
    dataIndex: 'keyword_community',
    key: 'keyword_community',
  },
  {
    title: 'Author Community',
    dataIndex: 'author_community',
    key: 'author_community',
  },
];

const CommunityDetectionPage = () => {
  const [data, setData] = useState([]);

  const handleGetCommunityData = async () => {
    const communityData = await getCommunityData();
    const tableData = [];

    for (const [community_id, keywords] of Object.entries(
      communityData.keyword_communities
    )) {
      const authors = communityData.author_communities[community_id] || [];
      tableData.push({
        key: community_id,
        community_id: community_id,
        keyword_community: keywords.join(', '),
        author_community: authors.join(', '),
      });
    }

    setData(tableData);
  };

  return (
    <>
      <Button onClick={handleGetCommunityData}>Get Community Data</Button>
      <Table columns={columns} dataSource={data} />
    </>
  );
};

export default CommunityDetectionPage;
