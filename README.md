# ROCKFALL_PREDICTION

## AI-Based Rockfall Prediction & Alert System

A full-stack hybrid application combining **Python ML**, **Node.js**, and **React** to predict rockfall risk based on environmental conditions.

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │ ───▶ │  Node.js     │ ───▶ │  Python ML  │
│  Frontend   │      │  Express API │      │  Flask API  │
│  (Port 3001)│ ◀─── │  (Port 3000) │ ◀─── │  (Port 5000)│
└─────────────┘      └──────────────┘      └─────────────┘
```

## 📁 Project Structure

```
rockfall_prototype/
├── python_ml/          # Python ML Service
│   ├── train.py        # Train & save model
│   ├── predict.py      # Flask prediction API
│   ├── requirements.txt
│   └── models/         # Saved ML models (auto-created)
│
├── backend/            # Node.js Express API
│   ├── server.js       # Express server
│   ├── package.json
│   └── .env
│
└── frontend/           # React UI
   ├── public/
   ├── src/
   │   ├── App.js      # Main component
   │   ├── App.css
   │   └── index.js
   └── package.json
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

---

### Step 1: Python ML Service

```powershell
# Navigate to python_ml folder
cd python_ml

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python train.py

# Start Flask API
python predict.py
```

Flask API runs at http://localhost:5000

---

### Step 2: Node.js Backend

Open a new terminal:

```powershell
# Navigate to backend folder
cd backend

# Install dependencies
npm install

# Start Express server
npm start
```

Express API runs at http://localhost:3000

---

### Step 3: React Frontend

Open a third terminal:

```powershell
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start React app
npm start
```

React app opens at http://localhost:3001

---

## 🎯 Usage

1. Open http://localhost:3001
2. Enter values:
  - Slope Angle: 0–90°
  - Rainfall: 0–500 mm
  - Temperature: −50 to 60°C
3. Click "Predict Risk"
4. View results: risk level, confidence, probabilities, message

---

## 🔧 API Endpoints

### Python Flask API (Port 5000)
- GET /health
- POST /predict

### Node.js Express API (Port 3000)
- GET /api/health
- POST /api/predict
- GET /api/history

---

## 🧠 ML Model Details

- Algorithm: Random Forest Classifier
- Features: 15 engineered features (slope, rainfall flag, temp, etc.)
- Output: Risk level (Low/Medium/High)
- Model and metadata saved under python_ml/models/

---

## Notes

- Ensure all three services are running
- Train the model before predictions
- CORS is enabled for local development

---

## License

MIT License
