import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:3000/api';

function App() {
  const [formData, setFormData] = useState({
    slope: '',
    rainfall: '',
    temperature: ''
  });
  
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await axios.post(`${API_URL}/predict`, {
        slope: parseFloat(formData.slope),
        rainfall: parseFloat(formData.rainfall),
        temperature: parseFloat(formData.temperature)
      });

      setPrediction(response.data.data);
    } catch (err) {
      setError(
        err.response?.data?.error || 
        'Failed to get prediction. Ensure backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    switch(level) {
      case 'Low': return '#10b981';
      case 'Medium': return '#f59e0b';
      case 'High': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🏔️ Rockfall Prediction System</h1>
          <p>AI-powered risk assessment for slope stability</p>
        </header>

        <form className="form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="slope">Slope Angle (degrees)</label>
            <input
              type="number"
              id="slope"
              name="slope"
              value={formData.slope}
              onChange={handleInputChange}
              placeholder="0 - 90"
              min="0"
              max="90"
              step="0.1"
              required
            />
            <span className="hint">Steeper slopes = higher risk</span>
          </div>

          <div className="input-group">
            <label htmlFor="rainfall">Rainfall (mm)</label>
            <input
              type="number"
              id="rainfall"
              name="rainfall"
              value={formData.rainfall}
              onChange={handleInputChange}
              placeholder="0 - 500"
              min="0"
              max="500"
              step="0.1"
              required
            />
            <span className="hint">Recent 24-hour rainfall</span>
          </div>

          <div className="input-group">
            <label htmlFor="temperature">Temperature (°C)</label>
            <input
              type="number"
              id="temperature"
              name="temperature"
              value={formData.temperature}
              onChange={handleInputChange}
              placeholder="-50 to 60"
              min="-50"
              max="60"
              step="0.1"
              required
            />
            <span className="hint">Current ambient temperature</span>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? '🔄 Analyzing...' : '🔍 Predict Risk'}
          </button>
        </form>

        {error && (
          <div className="alert alert-error">
            ❌ {error}
          </div>
        )}

        {prediction && (
          <div className="result-card">
            <div 
              className="risk-badge" 
              style={{ backgroundColor: getRiskColor(prediction.risk_level) }}
            >
              {prediction.risk_level} Risk
            </div>
            
            <div className="risk-message">
              {prediction.message}
            </div>

            <div className="confidence">
              <strong>Confidence:</strong> {prediction.confidence}%
            </div>

            <div className="probabilities">
              <h3>Risk Probabilities:</h3>
              <div className="prob-bars">
                <div className="prob-item">
                  <span>Low</span>
                  <div className="prob-bar">
                    <div 
                      className="prob-fill low" 
                      style={{ width: `${prediction.probabilities.low}%` }}
                    ></div>
                  </div>
                  <span>{prediction.probabilities.low}%</span>
                </div>
                <div className="prob-item">
                  <span>Medium</span>
                  <div className="prob-bar">
                    <div 
                      className="prob-fill medium" 
                      style={{ width: `${prediction.probabilities.medium}%` }}
                    ></div>
                  </div>
                  <span>{prediction.probabilities.medium}%</span>
                </div>
                <div className="prob-item">
                  <span>High</span>
                  <div className="prob-bar">
                    <div 
                      className="prob-fill high" 
                      style={{ width: `${prediction.probabilities.high}%` }}
                    ></div>
                  </div>
                  <span>{prediction.probabilities.high}%</span>
                </div>
              </div>
            </div>

            <div className="input-summary">
              <strong>Input Parameters:</strong>
              <p>Slope: {prediction.input.slope}° | Rainfall: {prediction.input.rainfall}mm | Temp: {prediction.input.temperature}°C</p>
            </div>
          </div>
        )}

        <footer className="footer">
          <p>Powered by Python ML + Node.js + React</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
