# Intelligent Investment Strategist Backend

AI-powered investment analysis platform for Nigerian retail investors using US stocks.

## 🎯 Core Features

- **Portfolio Building**: Budget-based, risk-aware portfolio recommendations
- **SEC Filing Analysis**: AI-powered PDF analysis with Nigerian context
- **Earnings Call Insights**: Audio transcription and sentiment analysis
- **Future Projections**: Realistic return scenarios with FX considerations
- **Nigerian Localization**: All explanations in plain Nigerian English

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.10+)
- **AI Engine**: Google Gemini 2.0 Flash (Multimodal)
- **Market Data**: Finnhub API
- **FX Data**: ExchangeRate API

## 📁 Project Structure

```
backend/
├── main.py                  # FastAPI application & endpoints
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── services/
│   ├── gemini_service.py   # Gemini AI integration
│   └── finance_api.py      # Market data & calculations
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- API keys for:
  - Google Gemini AI
  - Finnhub (stock data)
  - ExchangeRate API (optional)

### 2. Installation

```bash
# Clone the repository
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Use your favorite text editor (nano, vim, VSCode, etc.)
nano .env
```

Add your API keys:
```env
GEMINI_API_KEY=your-actual-gemini-key
FINNHUB_API_KEY=your-actual-finnhub-key
EXCHANGE_RATE_API_KEY=your-actual-exchange-key
```

### 4. Run the Server

```bash
# Development mode (auto-reload enabled)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

### 5. Test the API

Open your browser and visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### Core Investment Endpoints

#### 1. Build Portfolio
```http
POST /api/portfolio/build
Content-Type: application/json

{
  "budget_ngn": 50000,
  "risk_level": "medium",
  "time_horizon": "1_year"
}
```

**Response**:
```json
{
  "success": true,
  "portfolio": {
    "budget_ngn": 50000,
    "budget_usd": 32.47,
    "portfolio": [...]
  },
  "ai_explanation": "With your ₦50,000, here's what we recommend..."
}
```

#### 2. Calculate Projections
```http
POST /api/portfolio/projections
Content-Type: application/json

{
  "budget_ngn": 50000,
  "risk_level": "medium",
  "time_horizon": "1_year"
}
```

### Market Data Endpoints

#### 3. Get Stock Price
```http
POST /api/market/stock-price
Content-Type: application/json

{
  "symbol": "AAPL"
}
```

#### 4. Get FX Rate
```http
GET /api/market/fx-rate
```

#### 5. Get Approved Assets
```http
GET /api/market/approved-assets
```

### Document Analysis Endpoints

#### 6. Analyze SEC Filing
```http
POST /api/analysis/sec-filing
Content-Type: multipart/form-data

file: [PDF file]
symbol: AAPL
```

#### 7. Analyze Earnings Call
```http
POST /api/analysis/earnings-call
Content-Type: multipart/form-data

file: [Audio file]
symbol: AAPL
```

### AI Explanation Endpoints

#### 8. Explain Financial Concept
```http
POST /api/ai/explain-concept
Content-Type: application/json

{
  "concept": "P/E Ratio",
  "context": "Comparing tech stocks"
}
```

### Utility Endpoints

#### 9. Get Risk Levels
```http
GET /api/utils/risk-levels
```

#### 10. Get Time Horizons
```http
GET /api/utils/time-horizons
```

## 🧪 Testing

### Test with cURL

```bash
# Health check
curl http://localhost:8000/health

# Build portfolio
curl -X POST http://localhost:8000/api/portfolio/build \
  -H "Content-Type: application/json" \
  -d '{
    "budget_ngn": 50000,
    "risk_level": "medium",
    "time_horizon": "1_year"
  }'

# Get FX rate
curl http://localhost:8000/api/market/fx-rate
```

### Test with Python

```python
import requests

# Build portfolio
response = requests.post(
    "http://localhost:8000/api/portfolio/build",
    json={
        "budget_ngn": 50000,
        "risk_level": "medium",
        "time_horizon": "1_year"
    }
)

print(response.json())
```

## 🔧 Configuration

### Modifying API Keys

Edit your `.env` file:
```bash
nano .env
```

### Changing Server Port

In `.env`:
```env
API_PORT=8080
```

Or directly:
```bash
uvicorn main:app --port 8080
```

### Adding New Assets

Edit `services/finance_api.py`:
```python
self.approved_assets = {
    "VOO": "ETF",
    "SPY": "ETF",
    "AAPL": "Stock",
    "MSFT": "Stock",
    "GOOGL": "Stock",  # Add new asset
    # ... add more
}
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Invalid API Key"
```bash
# Check your .env file
cat .env

# Make sure API keys are valid (no quotes, no spaces)
GEMINI_API_KEY=AIzaSy...
```

### Issue: "Port already in use"
```bash
# Change port
uvicorn main:app --port 8001

# Or kill existing process
# Mac/Linux:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: "CORS Error from Frontend"
Update `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini AI Docs](https://ai.google.dev/docs)
- [Finnhub API Docs](https://finnhub.io/docs/api)

## 🤝 Contributing

This is a hackathon project. Feel free to:
- Add more financial APIs
- Improve Nigerian localization
- Add more asset classes
- Enhance AI prompts

## 📝 License

MIT License - feel free to use and modify!

## 👥 Authors

Backend Team - Intelligent Investment Strategist
Nigerian Fintech Hackathon 2025
