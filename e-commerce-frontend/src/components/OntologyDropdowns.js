import React, { useState, useEffect } from 'react';
import { Select, Button, notification } from 'antd';
import axios from 'axios';
import FormItemLabel from 'antd/es/form/FormItemLabel';

const { Option } = Select;

const OntologyDropdowns = () => {
    const [classes, setClasses] = useState([]);
    const [selectedClass, setSelectedClass] = useState(null);
    const [instances, setInstances] = useState([]);
    const [selectedInstance1, setSelectedInstance1] = useState(null);
    const [selectedInstance2, setSelectedInstance2] = useState(null);
    const [jaccardScore, setJaccardScore] = useState(null);
    const [cosineSimilarity, setCosineSimilarity] = useState(null);
    const [euclideanScore, setEuclideanScore] = useState(null);

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

    const cleanAndSetValues = (jaccard_similarity, cosine_similarity, euclidean_distance) => {
        setJaccardScore((parseFloat(jaccard_similarity)).toFixed(3));
        setCosineSimilarity((parseFloat(cosine_similarity)).toFixed(3));
        setEuclideanScore((parseFloat(euclidean_distance).toFixed(2)))

    }
    
    const handleCompare = () => {
        if (selectedInstance1 && selectedInstance2 && selectedInstance1 !== selectedInstance2) {
            axios.post('http://localhost:8000/similarity', {
                instance1: selectedInstance1,
                instance2: selectedInstance2
            })
                .then(response => cleanAndSetValues(response.data.jaccard_similarity, response.data.cosine_similarity, response.data.euclidean_distance))
                .catch(error => console.error('Error fetching similarity score:', error));
        } else {
            notification.error({
                message: 'Selection Error',
                description: 'Please select two different instances.',
            });
        }
    };

    const labelForInput = {
        fontWeight: 500,
        fontSize: 16
    }

    const displayScore = { display: "flex", flexDirection: "row", fontSize: 18 }
    const scoreData = {display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", marginBottom: 20}

    return (
        <div>
            <div style={scoreData}>
                <div style={{fontSize: 28, fontWeight: 700}}>
                    Computed Scores!
                </div>
                <div style={{marginTop: 10}}>
                    <div style={displayScore}>
                        <div style={{marginRight: 5}}>Jaccard's Similarity:</div>
                        <div style={{fontWeight: 500}}>{jaccardScore !== null ? jaccardScore : 0.0}</div>
                    </div>
                    <div style={displayScore}>
                        <div style={{marginRight: 5}}>Cosine Similarity:</div>
                        <div style={{fontWeight: 500}}>{cosineSimilarity !== null ? cosineSimilarity : 0.0}</div>
                    </div>
                    <div style={displayScore}>
                        <div style={{marginRight: 5}}>Euclidean Distance</div>
                        <div style={{fontWeight: 500}}>{euclideanScore !== null ? euclideanScore : 0.0}</div>
                    </div>
                </div>
            </div>

            <div style={labelForInput}>Select a class</div>
            <Select
                placeholder="Select a class"
                onChange={value => setSelectedClass(value)}
                style={{ width: '100%', marginBottom: 20 }}
            >
                {classes.map(cls => (
                    <Option key={cls} value={cls}>{cls}</Option>
                ))}
            </Select>
            <div style={labelForInput}>Select an instance</div>
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
            <div style={labelForInput}>Select an instance</div>
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

            {/* Cosine Similarity: {consineScore}
            Euclidean Distance: {euclideanScore} */}


            <Button type="primary" onClick={handleCompare}>Compare</Button>
        </div>
    );
};

export default OntologyDropdowns;
