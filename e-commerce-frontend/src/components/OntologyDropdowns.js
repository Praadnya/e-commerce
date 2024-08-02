import React, { useState, useEffect } from 'react';
import { Select, Button, notification } from 'antd';
import axios from 'axios';

const { Option } = Select;

const OntologyDropdowns = () => {
    const [classes, setClasses] = useState([]);
    const [selectedClass, setSelectedClass] = useState(null);
    const [instances, setInstances] = useState([]);
    const [selectedInstance1, setSelectedInstance1] = useState(null);
    const [selectedInstance2, setSelectedInstance2] = useState(null);
    const [similarityScore, setSimilarityScore] = useState(null);

    useEffect(() => {
        axios.get('http://localhost:8000/classes')
            .then(response => setClasses(response.data))
            .catch(error => console.error('Error fetching classes:', error));
    }, []);

    useEffect(() => {
        if (selectedClass) {
            axios.post('http://localhost:8000/instances', { class_name: selectedClass })
                .then(response => setInstances(response.data))
                .catch(error => console.error('Error fetching instances:', error));
        }
    }, [selectedClass]);

    const handleCompare = () => {
        if (selectedInstance1 && selectedInstance2 && selectedInstance1 !== selectedInstance2) {
            axios.post('http://localhost:8000/similarity', {
                instance1: selectedInstance1,
                instance2: selectedInstance2
            })
                .then(response => setSimilarityScore(response.data.similarity_score))
                .catch(error => console.error('Error fetching similarity score:', error));
        } else {
            notification.error({
                message: 'Selection Error',
                description: 'Please select two different instances.',
            });
        }
    };

    return (
        <div>
            <Select
                placeholder="Select a class"
                onChange={value => setSelectedClass(value)}
                style={{ width: '100%', marginBottom: 20 }}
            >
                {classes.map(cls => (
                    <Option key={cls} value={cls}>{cls}</Option>
                ))}
            </Select>
            <Select
                placeholder="Select instance 1"
                onChange={value => setSelectedInstance1(value)}
                style={{ width: '100%', marginBottom: 20 }}
                disabled={!selectedClass}
            >
                {instances.map(inst => (
                    <Option key={inst} value={inst}>{inst}</Option>
                ))}
            </Select>
            <Select
                placeholder="Select instance 2"
                onChange={value => setSelectedInstance2(value)}
                style={{ width: '100%', marginBottom: 20 }}
                disabled={!selectedClass}
            >
                {instances.map(inst => (
                    <Option key={inst} value={inst}>{inst}</Option>
                ))}
            </Select>
            <Button type="primary" onClick={handleCompare}>Compare</Button>
            {similarityScore !== null && (
                <div style={{ marginTop: 20 }}>
                    Similarity Score: {similarityScore}
                </div>
            )}
        </div>
    );
};

export default OntologyDropdowns;
