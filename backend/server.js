const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/api/health', async (req, res) => {
  try {
    // Check if Python API is running
    const pythonHealth = await axios.get(`${PYTHON_API_URL}/health`);
    res.json({
      status: 'healthy',
      backend: 'online',
      pythonML: pythonHealth.data
    });
  } catch (error) {
    res.status(503).json({
      status: 'degraded',
      backend: 'online',
      pythonML: 'offline',
      error: 'Python ML service unavailable'
    });
  }
});

// Predict rockfall risk (Bridge to Python API)
app.post('/api/predict', async (req, res) => {
  try {
    const { slope, rainfall, temperature } = req.body;

    // Validate input
    if (slope === undefined || rainfall === undefined || temperature === undefined) {
      return res.status(400).json({
        error: 'Missing required fields: slope, rainfall, temperature'
      });
    }

    // Forward request to Python ML service
    console.log(`📡 Forwarding prediction request to Python API...`);
    const pythonResponse = await axios.post(`${PYTHON_API_URL}/predict`, {
      slope: parseFloat(slope),
      rainfall: parseFloat(rainfall),
      temperature: parseFloat(temperature)
    });

    // Return prediction results
    console.log(`✅ Prediction received: ${pythonResponse.data.risk_level}`);
    res.json({
      success: true,
      data: pythonResponse.data,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('❌ Prediction error:', error.message);
    
    if (error.response) {
      // Python API returned an error
      return res.status(error.response.status).json({
        error: error.response.data.error || 'Prediction failed',
        details: error.response.data
      });
    }
    
    // Python API is not reachable
    res.status(503).json({
      error: 'Python ML service unavailable',
      message: 'Please ensure the Flask API is running on port 5000'
    });
  }
});

// Get prediction history (placeholder)
app.get('/api/history', (req, res) => {
  res.json({
    message: 'History feature coming soon',
    data: []
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'Rockfall Prediction API',
    version: '1.0.0',
    endpoints: {
      health: 'GET /api/health',
      predict: 'POST /api/predict',
      history: 'GET /api/history'
    }
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Express backend running on http://localhost:${PORT}`);
  console.log(`📡 Python ML API: ${PYTHON_API_URL}`);
  console.log(`\n📌 API Endpoints:`);
  console.log(`   - Health: GET  /api/health`);
  console.log(`   - Predict: POST /api/predict`);
});
