"""
main.py
FastAPI Backend: Intelligent Investment Strategist for Nigerian Investors

This is the main entry point for the backend API.
Handles all HTTP requests and orchestrates between Gemini AI and Finance services.

Author: Backend Team Lead
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse # REQUIRED for error handling fix
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import tempfile
import os
from pathlib import Path
from datetime import datetime

# Import our custom services
from services.gemini_service import GeminiService
from services.finance_api import FinanceAPIService


# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Investment Strategist API",
    description="AI-powered investment analysis for Nigerian retail investors",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
     allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",                           # Vite local dev
        "https://investment-strategist.vercel.app",        # Your Vercel URL
        "https://*.vercel.app",                       # All Vercel subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gemini_service = GeminiService()
finance_service = FinanceAPIService()


# ============================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

class PortfolioRequest(BaseModel):
    """Request model for portfolio building"""
    budget_ngn: float = Field(..., gt=0, description="Investment budget in Nigerian Naira")
    risk_level: str = Field(..., description="Risk tolerance: low, medium, or high")
    time_horizon: str = Field(
        default="1_year",
        description="Investment timeframe: 6_months, 1_year, 2_years, etc."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "budget_ngn": 50000,
                "risk_level": "medium",
                "time_horizon": "1_year"
            }
        }


class ProjectionRequest(BaseModel):
    """Request model for future value projections"""
    budget_ngn: float = Field(..., gt=0)
    risk_level: str = Field(...)
    time_horizon: str = Field(default="1_year")
    portfolio: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Optional portfolio composition for more accurate projections"
    )


class StockInfoRequest(BaseModel):
    """Request model for individual stock information"""
    symbol: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")


class ConceptExplanationRequest(BaseModel):
    """Request model for explaining financial concepts"""
    concept: str = Field(..., description="Financial term to explain")
    context: Optional[str] = Field(default="", description="Additional context")


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Intelligent Investment Strategist API",
        "version": "1.0.0",
        "message": "Backend is running successfully"
    }


@app.get("/health")
async def health_check():
    """Detailed health check with service status"""
    return {
        "status": "healthy",
        "services": {
            "gemini": "operational",
            "finance_api": "operational",
            "fx_data": "operational"
        },
        "timestamp":datetime.utcnow().isoformat() + "Z"
    }


# ============================================================================
# CORE INVESTMENT ENDPOINTS
# ============================================================================

@app.post("/api/portfolio/build")
async def build_portfolio(request: PortfolioRequest):
    """Build a diversified portfolio based on budget and risk tolerance."""
    try:
        portfolio_data = finance_service.build_portfolio(
            budget_ngn=request.budget_ngn,
            risk_level=request.risk_level,
            time_horizon=request.time_horizon
        )
        
        ai_explanation = gemini_service.explain_portfolio_recommendation(
            portfolio_data=portfolio_data,
            budget_ngn=request.budget_ngn,
            risk_level=request.risk_level
        )
        
        return {
            "success": True,
            "portfolio": portfolio_data,
            "ai_explanation": ai_explanation,
            "metadata": {
                "budget_ngn": request.budget_ngn,
                "risk_level": request.risk_level,
                "time_horizon": request.time_horizon
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build portfolio: {str(e)}"
        )


@app.post("/api/portfolio/projections")
async def calculate_projections(request: ProjectionRequest):
    """Calculate future value projections for an investment."""
    try:
        projections_data = finance_service.calculate_projections(
            budget_ngn=request.budget_ngn,
            risk_level=request.risk_level,
            time_horizon=request.time_horizon,
            portfolio=request.portfolio
        )
        
        ai_explanation = gemini_service.explain_projections(
            projections_data=projections_data,
            budget_ngn=request.budget_ngn,
            time_horizon=request.time_horizon
        )
        
        return {
            "success": True,
            "projections": projections_data,
            "ai_explanation": ai_explanation
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate projections: {str(e)}"
        )


# ============================================================================
# MARKET DATA ENDPOINTS
# ============================================================================

@app.post("/api/market/stock-price")
async def get_stock_price(request: StockInfoRequest):
    """Get current stock price in USD."""
    try:
        price = finance_service.get_stock_price(request.symbol)
        
        if price is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch price for {request.symbol}"
            )
        
        return {
            "success": True,
            "symbol": request.symbol,
            "price_usd": price,
            "currency": "USD"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock price: {str(e)}"
        )


@app.get("/api/market/fx-rate")
async def get_fx_rate():
    """Get current NGN/USD exchange rate."""
    try:
        fx_rate = finance_service.get_fx_rate()
        
        return {
            "success": True,
            "rate": fx_rate,
            "description": f"1 USD = ₦{fx_rate}",
            "currency_pair": "NGN/USD"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching FX rate: {str(e)}"
        )


@app.get("/api/market/approved-assets")
async def get_approved_assets():
    """Get list of pre-approved investment assets."""
    return {
        "success": True,
        "assets": finance_service.approved_assets,
        "asset_characteristics": finance_service.asset_characteristics
    }


# ============================================================================
# DOCUMENT ANALYSIS ENDPOINTS (Gemini Multimodal)
# ============================================================================

@app.post("/api/analysis/sec-filing")
async def analyze_sec_filing(
    file: UploadFile = File(...),
    symbol: str = Form(...)
):
    """Upload and analyze SEC filing (10-K, 10-Q) PDF."""
    tmp_path: Optional[str] = None
    try:
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        analysis = gemini_service.analyze_sec_pdf(
            pdf_file_path=tmp_path,
            stock_symbol=symbol.upper()
        )
        
        os.unlink(tmp_path)
        
        if analysis.get("error"):
            raise HTTPException(
                status_code=500,
                detail=analysis.get("message", "Analysis failed")
            )
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        if tmp_path is not None:
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze SEC filing: {str(e)}"
        )


@app.post("/api/analysis/earnings-call")
async def analyze_earnings_call(
    file: UploadFile = File(...),
    symbol: str = Form(...)
):
    """Upload and analyze earnings call audio."""
    tmp_path: Optional[str] = None
    try:
        valid_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
        if not file.filename or not any(file.filename.lower().endswith(ext) for ext in valid_extensions):
             raise HTTPException(    
                status_code=400,
                detail=f"Unsupported audio format. Supported: {', '.join(valid_extensions)}"
            )
        
        file_extension = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        analysis = gemini_service.analyze_earnings_audio(
            audio_file_path=tmp_path,
            stock_symbol=symbol.upper()
        )
        
        os.unlink(tmp_path)
        
        if analysis.get("error"):
            raise HTTPException(
                status_code=500,
                detail=analysis.get("message", "Analysis failed")
            )
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up temp file if it was created
        if tmp_path is not None:
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze earnings call: {str(e)}"
        )


# ============================================================================
# AI EXPLANATION ENDPOINTS
# ============================================================================

@app.post("/api/ai/explain-concept")
async def explain_financial_concept(request: ConceptExplanationRequest):
    """Get simple Nigerian-context explanation for financial terms."""
    try:
        explanation = gemini_service.simplify_financial_concept(
            concept=request.concept,
            context=request.context or ""
        )
        
        return {
            "success": True,
            "concept": request.concept,
            "explanation": explanation
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to explain concept: {str(e)}"
        )


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/api/utils/risk-levels")
async def get_risk_levels():
    """Get available risk level options and their descriptions."""
    return {
        "success": True,
        "risk_levels": {
            "low": {
                "label": "Conservative (Low Risk)",
                "description": "Focus on stable, defensive stocks and ETFs. Lower returns but safer.",
                "typical_assets": ["VOO", "SPY", "JNJ", "KO"],
                "volatility": "15-18% annually"
            },
            "medium": {
                "label": "Balanced (Medium Risk)",
                "description": "Mix of growth and stability. Good for most investors.",
                "typical_assets": ["VOO", "AAPL", "MSFT"],
                "volatility": "18-22% annually"
            },
            "high": {
                "label": "Aggressive (High Risk)",
                "description": "Growth-focused with tech stocks. Higher potential returns but volatile.",
                "typical_assets": ["AAPL", "MSFT", "VOO"],
                "volatility": "22-25% annually"
            }
        }
    }


@app.get("/api/utils/time-horizons")
async def get_time_horizons():
    """Get available investment time horizon options."""
    return {
        "success": True,
        "time_horizons": [
            {"value": "6_months", "label": "6 Months", "recommended_risk": ["low", "medium"]},
            {"value": "1_year", "label": "1 Year", "recommended_risk": ["low", "medium", "high"]},
            {"value": "2_years", "label": "2 Years", "recommended_risk": ["medium", "high"]},
            {"value": "3_years", "label": "3 Years", "recommended_risk": ["medium", "high"]},
            {"value": "5_years", "label": "5 Years", "recommended_risk": ["medium", "high"]},
            {"value": "10_years", "label": "10 Years", "recommended_risk": ["high"]}
        ]
    }


# ============================================================================
# ERROR HANDLERS (FIXED: Uses JSONResponse)
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler returning proper JSONResponse"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all exception handler returning proper JSONResponse"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "An unexpected error occurred",
                "detail": str(exc)
            }
        }
    )


# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True 
    )