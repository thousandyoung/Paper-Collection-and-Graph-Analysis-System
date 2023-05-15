import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { searchPapers, getPaper} from '../services/PaperService';
import { Input, Button, Table, Pagination } from 'antd';
import { SearchContext } from '../App';

function PaperSearchPage() {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const { results, setResults, total, setTotal } = useContext(SearchContext);

  const handlePageChange = (page, pageSize) => {
    setCurrentPage(page);
    setPageSize(pageSize);
    searchPapers(query, page, pageSize).then((data) => {
      setResults(data.papers);
      setTotal(data.total_count);
    });
  };

  const handleSearch = async () => {
    const data = await searchPapers(query, currentPage, pageSize);
    setResults(data.papers);
    setTotal(data.total_count);
  };

  const handleTitleClick = async (record) => {
    const paper = await getPaper(record.uid); // 获取论文具体信息
    navigate(`/paper-detail/${record.uid}`, { state: paper }); // 导航到论文详情页面，并传递论文具体信息
  };
  
  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const columns = [
    {
      title: 'UID',
      dataIndex: 'uid',
      key: 'uid',
      render: () => null, // 隐藏列，返回空字符串
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      render: (text, record) =>  <Link onClick={() => handleTitleClick(record)}>{text}</Link> 
    },
    {
      title: 'Authors',
      dataIndex: 'authors',
      key: 'authors',
    },
    {
      title: 'Published Date',
      dataIndex: 'published_date',
      key: 'published_date',
    },
  ];
  // 渲染时忽略UID列
  const filteredColumns = columns.filter((column) => column.key !== 'uid');

  return (
    <div className="container">
      <h2>Paper Search</h2>

      <Input value={query} onChange={handleInputChange} placeholder="Enter paper title" />

      <Button type="primary" onClick={handleSearch}>Search</Button>

      <Table dataSource={results} columns={filteredColumns} rowKey="id" pagination={false} />

      <Pagination
        current={currentPage}
        pageSize={pageSize}
        total={total}
        onChange={handlePageChange}
      />
    </div>
  );
}

export default PaperSearchPage;
