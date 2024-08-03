import React from 'react';
import { Layout, Menu } from 'antd';
import OntologyDropdowns from './components/OntologyDropdowns';

const { Header, Content, Footer } = Layout;

const App = () => {
    return (
        <Layout className="layout">
            <Header>
                <div className="logo" />
                <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
                    <Menu.Item key="1">Ontology Similarity</Menu.Item>
                </Menu>
            </Header>
            <Content style={{ padding: '0 50px' }}>
                <div className="site-layout-content" style={{ marginTop: 50 }}>
                    <OntologyDropdowns />
                </div>
            </Content>
            <Footer style={{ textAlign: 'center' }}>Ontology and Semantic Web - Summer Course 2024</Footer>
        </Layout>
    );
};

export default App;
