# 🚀 Quick Setup Guide

Get your backend running in 5 minutes!

## Step 1: Get Your API Keys

### Google Gemini API Key (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)

### Finnhub API Key (Required)
1. Go to [Finnhub](https://finnhub.io/register)
2. Sign up for free account
3. Copy your API key from dashboard

### ExchangeRate API (Optional - has fallback)
1. Go to [ExchangeRate-API](https://www.exchangerate-api.com/)
2. Sign up for free
3. Copy your API key

## Step 2: Install Python Dependencies

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# or
code .env
# or
notepad .env
```

**Add your API keys:**
```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXX
FINNHUB_API_KEY=your_finnhub_key_here
EXCHANGE_RATE_API_KEY=your_exchange_key_here
```

**Save and close!**

## Step 4: Run the Server

```bash
# Make sure you're in the backend folder
# and your virtual environment is activated

python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 5: Test It!

### Option A: Using Your Browser
Open: http://localhost:8000/docs

This opens the **interactive API documentation** where you can test all endpoints!

### Option B: Using the Test Script
```bash
# In a NEW terminal (keep the server running)
cd backend
source venv/bin/activate  # Activate venv again
python test_backend.py
```

### Option C: Using cURL
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test portfolio building
curl -X POST http://localhost:8000/api/portfolio/build \
  -H "Content-Type: application/json" \
  -d '{"budget_ngn": 50000, "risk_level": "medium", "time_horizon": "1_year"}'
```

## ✅ Success Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] API keys added to `.env` file
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Health check returns 200 OK
- [ ] Portfolio building works

## 🐛 Common Issues

### "ModuleNotFoundError: No module named 'fastapi'"
**Fix:** Make sure virtual environment is activated and run `pip install -r requirements.txt`

### "ValueError: Invalid API key"
**Fix:** Check your `.env` file. Keys should have no quotes or extra spaces:
```env
# ❌ Wrong
GEMINI_API_KEY="AIza..."
# ✅ Correct
GEMINI_API_KEY=AIza...
```

### "Address already in use"
**Fix:** Change the port in `.env` or kill the existing process
```bash
# Use different port
uvicorn main:app --port 8001

# Or kill existing process (Mac/Linux)
lsof -ti:8000 | xargs kill -9
```

### "Cannot connect to server"
**Fix:** Make sure the server is actually running:
```bash
# Check if process is running
ps aux | grep uvicorn

# Restart the server
python main.py
```

## 🎯 Next Steps

1. **Test all endpoints** using the interactive docs at `/docs`
2. **Try uploading a PDF** to test SEC filing analysis
3. **Build a test portfolio** with different risk levels
4. **Connect your frontend** (if you have one)

## 📞 Need Help?

- Check the main [README.md](README.md) for detailed API documentation
- Review error messages in the terminal where the server is running
- Make sure all API keys are valid and have the correct permissions

## 🎉 You're Ready!

Your backend is now running and ready to serve Nigerian investors with AI-powered investment insights!

Test endpoint: http://localhost:8000/health
API Docs: http://localhost:8000/docs
