import { Card, Typography } from 'antd';
import { useLocation } from 'react-router-dom';
const { Title, Paragraph } = Typography;

function PaperDetailPage() {
  const location = useLocation();
  const paper = location.state;

  return (
    <Card title={paper.title}>
      <Title level={5}>作者：</Title>
      {paper.authors.map((author) => (
        <Paragraph key={author.name}>{author.name} ({author.department})</Paragraph>
      ))}
      <Title level={5}>发表日期：</Title>
      <Paragraph>{paper.published_date}</Paragraph>
      <Title level={5}>关键词：</Title>
      <Paragraph>{paper.keywords.join(', ')}</Paragraph>
      <Title level={5}>摘要：</Title>
      <Paragraph>{paper.abstract}</Paragraph>
    </Card>
  );
}

export default PaperDetailPage;
