import React from 'react';
import { useState } from 'react';
import "./URLScan.css";

function URLScan(){
    const [url, setUrl] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleScan = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        
        try {
            
            const response = await fetch('http://127.0.0.1:5000/predict',{
                method: 'POST',
                headers: {
                    'Content-Type' : 'application/json',
                },
                body: JSON.stringify({url}),
            });
            const data = await response.json(); 
            setResult(data);
        } catch (err) {
            setError("Error scanning URL! Please try again.");
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="url-scan" id="#URLInput">
            <h2>URL Scanner</h2>
            <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter URL to scan"
            />
            <button onClick={handleScan} disabled={loading}>
                {loading ? 'Scanning...' : 'Scan URL'}
            </button>

            {error && <div className="error">{error}</div>}
            {result && result.prediction && (
                <div className={`result ${result.prediction.toLowerCase() === 'phishing' ? 'phishing' : 'safe'}`}>
                    <h3>Scan Result:</h3>
                    <p><strong>Status:</strong> {result.prediction.toLowerCase() === 'phishing' ? 'Phishing' : 'Safe'}</p>
                    <p>URL: {result.url}</p>
                    <p>Result: {result.prediction.toLowerCase() === 'phishing' ? 'This URL is dangerous' : 'This URL is safe.'}</p>
                </div>
            )}
        </div>
    );
}

export default URLScan;