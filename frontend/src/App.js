import React, { createContext, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import PaperSearchPage from './pages/PaperSearchPage';
import PaperDetailPage from './pages/PaperDetailsPage';
import KnowledgeGraphPage from './pages/KnowledgeGraphPage';
import SpiderManagementPage from './pages/SpiderManagementPage';
import CommunityDetectionPage from './pages/CommunityDetectionPage';
import AppLayout from './components/AppLayout'


// 创建一个上下文，初始值为null
export const SearchContext = createContext(null);

function App() {
  // 在App组件中创建状态，存储搜索结果和分页信息
  const [results, setResults] = useState([]);
  const [total, setTotal] = useState(0);

  return (
    <SearchContext.Provider value={{ results, setResults, total, setTotal }}>
      <BrowserRouter>
        <AppLayout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/search" element={<PaperSearchPage />} />
            <Route path="/paper-detail/:uid" element={<PaperDetailPage />} />
            <Route path="/knowledge-graph" element={<KnowledgeGraphPage />} />
            <Route path='/spider-management' element={<SpiderManagementPage />} />
            <Route path='/community-detection' element={<CommunityDetectionPage />} />
          </Routes>
        </AppLayout>
      </BrowserRouter>
    </SearchContext.Provider>
  );
}

export default App;
