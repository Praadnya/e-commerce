import React, { useState } from 'react';
import { Layout, Select, Table, Typography, Spin } from 'antd';

const { Header, Content } = Layout;
const { Option } = Select;
const { Title } = Typography;

const App = () => {
  const [queryName, setQueryName] = useState(null);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleQueryChange = async (value) => {
    setQueryName(value);
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/execute_query?query_name=${value}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      setData(result.results.map((row, index) => ({ key: index, row })));
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'Result',
      dataIndex: 'row',
      key: 'row',
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ backgroundColor: '#001529', padding: '0 20px' }}>
        <Title style={{ color: '#fff', margin: 0 }} level={3}>
          SPARQL Query Executor
        </Title>
      </Header>
      <Content style={{ padding: '20px 50px' }}>
        <div style={{ marginBottom: '20px', textAlign: 'center' }}>
          <Select
            style={{ width: 300 }}
            placeholder="Select a query"
            onChange={handleQueryChange}
            value={queryName}
          >
            <Option value="Bought-Together">Bought-Together</Option>
            <Option value="Gold-Customers-infos">Gold-Customers-infos</Option>
            <Option value="One-Category-Buyers">One-Category-Buyers</Option>
            <Option value="Product-Recommendation">Product-Recommendation</Option>
            <Option value="Product-Retrieval">Product-Retrieval</Option>
            <Option value="Related-Products">Related-Products</Option>
            <Option value="Similar-Customers-Brand">Similar-Customers-Brand</Option>
            <Option value="Similar-Customers-Purchases">Similar-Customers-Purchases</Option>
            <Option value="User-History">User-History</Option>
            <Option value="Verified-Purchase">Verified-Purchase</Option>
          </Select>
        </div>
        {loading ? (
          <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table
            columns={columns}
            dataSource={data}
            loading={loading}
            style={{ marginTop: 20 }}
            pagination={{ pageSize: 10 }}
          />
        )}
      </Content>
    </Layout>
  );
};

export default App;
