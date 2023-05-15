import { Layout, Menu } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import { HomeOutlined, FileSearchOutlined, ClusterOutlined, BugOutlined, GlobalOutlined} from '@ant-design/icons';
import React, { ReactNode, useEffect, useState } from 'react';
const { Sider, Content } = Layout;

export default function AppLayout({ children }: { children: ReactNode }) {
  const location = useLocation();
  const [selectedKeys, setSelectedKeys] = useState<string[]>(['']);

  useEffect(() => {
    // 根据当前页面的路径来确定应该选中哪个菜单项
    switch (location.pathname) {
      case '/':
        setSelectedKeys(['home']);
        break;
      case '/search':
        setSelectedKeys(['search']);
        break;
      case '/knowledge-graph':
        setSelectedKeys(['knowledge-graph']);
        break;
      case '/spider-management':
        setSelectedKeys(['spider-management']);
        break;
      case '/community-detection':
      setSelectedKeys(['community-detection']);
      break;
      default:
        setSelectedKeys(['']);
        break;
    }
  }, [location]);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider>
        <div className="logo" />
        <Menu theme="dark" selectedKeys={selectedKeys} mode="inline">
          <Menu.Item key="home" icon={<HomeOutlined />}>
            <Link to="/">Home</Link>
          </Menu.Item>
          <Menu.Item key="search" icon={<FileSearchOutlined />}>
            <Link to="/search">Paper Search</Link>
          </Menu.Item>
          <Menu.Item key="knowledge-graph" icon={<ClusterOutlined />}>
            <Link to="/knowledge-graph">Knowledge Graph</Link>
          </Menu.Item>
          <Menu.Item key="spider-management" icon={<BugOutlined />}>
            <Link to="/spider-management">Spider Management</Link>
          </Menu.Item>
          <Menu.Item key="community-detection" icon={<GlobalOutlined />}>
            <Link to="/community-detection">community-detection</Link>
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout className="site-layout">
        <Content style={{ margin: '0 16px' }}>
          <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
            {children}
          </div>
        </Content>
      </Layout>
    </Layout>
  );
}
