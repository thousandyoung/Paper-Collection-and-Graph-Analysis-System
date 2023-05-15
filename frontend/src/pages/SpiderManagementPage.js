import React, { useState, useEffect, useCallback } from 'react';
import { Table, Button, Modal, Form, Input, message, Progress, InputNumber } from 'antd';
import { fetchSpiders, addSpider, deleteSpider } from '../services/SpiderManagementService'

const { confirm } = Modal;

const SpiderManagementPage = () => {
    const [spiders, setSpiders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isAddModalVisible, setAddModalVisible] = useState(false);

    const handleAddSpider = async (values) => {
        try {
            setLoading(true);
            await addSpider(values);
            message.success('Spider added successfully');
            setAddModalVisible(false);
            fetchSpiders()
        } catch (error) {
            message.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteSpider = async (spider) => {
        confirm({
            title: `Are you sure you want to delete spider '${spider.name}'?`,
            onOk: async () => {
                try {
                    setLoading(true);
                    deleteSpider(spider)
                    message.success('Spider deleted successfully');
                    fetchSpiders();
                } catch (error) {
                    message.error('Failed to delete spider');
                } finally {
                    setLoading(false);
                }
            },
            onCancel() { },
        });
    };

    const columns = [{ title: 'Name', dataIndex: 'name', key: 'name', }, { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', }, { title: 'Total Pages', dataIndex: 'total_pages', key: 'total_pages', }, { title: 'Current Page', dataIndex: 'current_page', key: 'current_page', }, { title: 'Progress', key: 'progress', render: (text, record) => (<Progress percent={record.progress} />), }, { title: 'Status', dataIndex: 'status', key: 'status', }, { title: 'Actions', key: 'actions', render: (_, spider) => (<Button danger onClick={() => handleDeleteSpider(spider)}>                    Delete                </Button>), },];

    const fetchData = useCallback(() => {
        setLoading(true);
        fetchSpiders()
            .then((data) => {
                setLoading(false);
                setSpiders(data);
            })
            .catch((error) => {
                setLoading(false);
                message.error(error.message);
            });
    }, []);

    useEffect(() => {
        fetchData();
        const intervalId = setInterval(fetchData, 5000); // fetch data every 5 seconds
        return () => clearInterval(intervalId);
    }, [fetchData]);

    return (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <h1>Spider Management</h1>
            <Button type="primary" onClick={() => setAddModalVisible(true)}>
              Add Spider
            </Button>
          </div>
          <Table columns={columns} dataSource={spiders} loading={loading} rowKey="id" />
          <Modal
            visible={isAddModalVisible}
            onCancel={() => setAddModalVisible(false)}
            title="Add Spider"
            footer={null}
          >
            <Form onFinish={handleAddSpider}>
              <Form.Item
                label="Name"
                name="name"
                rules={[{ required: true, message: 'Please input spider name!' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Keyword"
                name="keyword"
                rules={[{ required: true, message: 'Please input spider keyword!' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Total Pages"
                name="total_pages"
                rules={[{ required: true, message: 'Please input the total number of pages!' }]}
              >
                <InputNumber min={1} />
              </Form.Item>
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  Add
                </Button>
              </Form.Item>
            </Form>
          </Modal>
        </div>
      );      
};
export default SpiderManagementPage;

