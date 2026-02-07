# 📁 Project Structure

Complete overview of the backend file organization.

```
backend/
│
├── main.py                              # 🚀 FastAPI application (START HERE)
│   ├── All API endpoints
│   ├── Request/Response models (Pydantic)
│   └── Error handlers
│
├── config.py                            # ⚙️ Configuration management
│   ├── Environment variables
│   ├── API keys loader
│   └── App settings
│
├── services/                            # 🧠 Core business logic
│   ├── __init__.py
│   ├── gemini_service.py               # AI/Gemini integration
│   │   ├── analyze_sec_pdf()           # PDF analysis
│   │   ├── analyze_earnings_audio()    # Audio transcription
│   │   ├── explain_portfolio_recommendation()
│   │   ├── explain_projections()
│   │   └── simplify_financial_concept()
│   │
│   └── finance_api.py                  # Market data & calculations
│       ├── get_stock_price()           # Finnhub API
│       ├── get_fx_rate()               # FX rates
│       ├── build_portfolio()           # Portfolio builder
│       ├── calculate_projections()     # Future value
│       └── Financial calculation helpers
│
├── prompts/                             # 📝 AI prompt templates (future)
│   └── __init__.py
│
├── requirements.txt                     # 📦 Python dependencies
│   ├── FastAPI
│   ├── Google Generative AI
│   ├── Requests
│   └── Other packages
│
├── .env.example                         # 🔐 Environment template
│   ├── GEMINI_API_KEY
│   ├── FINNHUB_API_KEY
│   └── EXCHANGE_RATE_API_KEY
│
├── .gitignore                          # 🚫 Git ignore rules
│   ├── .env (protect API keys!)
│   ├── __pycache__
│   └── venv/
│
├── README.md                           # 📖 Main documentation
│   ├── API endpoint reference
│   ├── Usage examples
│   └── Troubleshooting
│
├── SETUP_GUIDE.md                      # 🎯 Quick start guide
│   ├── Step-by-step setup
│   ├── API key instructions
│   └── Common issues
│
├── test_backend.py                     # 🧪 Test suite
│   ├── All endpoint tests
│   └── Automated verification
│
└── Intelligent_Investment_Strategist.postman_collection.json
    └── 📮 Postman API collection for testing

```

## 🎯 File Purposes

### Core Application Files

**main.py**
- Entry point for the FastAPI application
- Defines all API routes and endpoints
- Handles HTTP requests/responses
- Implements error handling
- **Start here to understand the API structure**

**config.py**
- Loads environment variables from `.env`
- Provides centralized settings
- Manages API keys securely
- **Use `get_settings()` to access configuration**

### Service Layer

**services/gemini_service.py**
- All Gemini AI interactions
- PDF and audio analysis
- Nigerian-context prompt engineering
- Financial concept simplification
- **This is where the AI magic happens**

**services/finance_api.py**
- Market data fetching (Finnhub)
- FX rate retrieval
- Portfolio building logic
- Financial calculations
- Risk assessment
- **All financial logic lives here**

### Configuration Files

**.env.example**
- Template for environment variables
- **Copy to `.env` and add your API keys**
- Never commit `.env` to git!

**requirements.txt**
- All Python package dependencies
- **Run `pip install -r requirements.txt`**

**.gitignore**
- Prevents committing sensitive files
- Protects API keys
- **Review before pushing to GitHub**

### Documentation

**README.md**
- Complete API documentation
- Endpoint reference
- Usage examples
- Troubleshooting guide

**SETUP_GUIDE.md**
- Quick 5-minute setup
- Step-by-step instructions
- Common issues and fixes

**PROJECT_STRUCTURE.md** (this file)
- File organization explanation
- Purpose of each file
- How everything connects

### Testing

**test_backend.py**
- Automated test suite
- Tests all endpoints
- Verifies functionality
- **Run after setup to ensure everything works**

**Intelligent_Investment_Strategist.postman_collection.json**
- Postman collection
- Pre-configured API requests
- **Import into Postman for easy testing**

## 🔄 How It All Connects

```
User Request
    ↓
main.py (FastAPI Routes)
    ↓
    ├── Portfolio Request? → finance_api.py → build_portfolio()
    │                              ↓
    │                       gemini_service.py → explain_portfolio()
    │                              ↓
    │                         Return to main.py
    │                              ↓
    │                         JSON Response
    │
    ├── PDF Upload? → main.py saves temp file
    │                      ↓
    │               gemini_service.py → analyze_sec_pdf()
    │                      ↓
    │                 Return analysis
    │                      ↓
    │                JSON Response
    │
    └── Market Data? → finance_api.py → get_stock_price()
                              ↓
                      External API (Finnhub)
                              ↓
                      Return to main.py
                              ↓
                        JSON Response
```

## 📊 Data Flow Example

**Building a Portfolio:**

1. Frontend sends POST to `/api/portfolio/build`
   ```json
   {
     "budget_ngn": 50000,
     "risk_level": "medium",
     "time_horizon": "1_year"
   }
   ```

2. `main.py` receives request, validates with Pydantic

3. Calls `finance_api.build_portfolio()`:
   - Gets current FX rate
   - Fetches stock prices
   - Calculates allocations
   - Returns portfolio data

4. Calls `gemini_service.explain_portfolio_recommendation()`:
   - Sends portfolio data to Gemini
   - Gets Nigerian-context explanation
   - Returns human-readable text

5. `main.py` combines both responses:
   ```json
   {
     "success": true,
     "portfolio": { ... },
     "ai_explanation": "With your ₦50,000..."
   }
   ```

6. Returns to frontend

## 🎨 Best Practices

### When Adding New Features

1. **New Endpoint?** → Add to `main.py`
2. **New AI Feature?** → Add to `gemini_service.py`
3. **New Calculation?** → Add to `finance_api.py`
4. **New Config?** → Add to `config.py`
5. **New Dependency?** → Add to `requirements.txt`

### File Modification Guidelines

- ✅ `main.py` - Add new routes, modify request/response models
- ✅ `services/*.py` - Add new business logic functions
- ✅ `config.py` - Add new configuration options
- ⚠️ `.env` - Add API keys (NEVER COMMIT!)
- ✅ `requirements.txt` - Add new packages
- ✅ `test_backend.py` - Add tests for new features

## 🔒 Security Notes

**Never Commit:**
- `.env` file (has API keys)
- `__pycache__/` folders
- `venv/` virtual environment
- Any files with credentials

**Always Include:**
- `.env.example` (template without real keys)
- `.gitignore` (protection)
- `requirements.txt` (dependencies)

## 📚 Further Reading

- See [README.md](README.md) for API documentation
- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for installation
- Check individual files for inline comments

---

**Questions?** Check the documentation files or review the inline code comments!
