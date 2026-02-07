"""
gemini_service.py
Backend Service: Gemini 3 Multimodal AI Engine

Responsibilities:
- Analyze SEC PDF filings (10-K, 10-Q) and extract key insights
- Transcribe and analyze earnings call audio
- Translate financial jargon into Nigerian context
- Provide budget-aware, FX-sensitive investment explanations

Author: Backend Dev 1 - AI/ML Engineer
"""

from typing import Dict, Any

import google.generativeai as genai
from config import settings


class GeminiService:
    """
    Handles all Gemini AI interactions for financial analysis and Nigerian localization.
    """

    def __init__(self):
        """Initialize Gemini API with configuration"""
        # Get API key from config
        self.api_key = settings.gemini_api_key

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Use Gemini 2.0 Flash for multimodal capabilities
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        # Nigerian context constants
        self.ngn_usd_context = """
        NIGERIAN INVESTOR CONTEXT:
        - Exchange Rate: Naira (₦) to USD fluctuates (currently ~₦1,540/$1)
        - FX Volatility: Naira typically depreciates 4-6% annually
        - Small Budgets: Many Nigerian investors start with ₦20,000-₦100,000 (~$13-$65)
        - Fractional Shares: Critical for affordability
        - Local Purchasing Power: ₦50,000 = 1-2 months minimum wage
        """

    def analyze_sec_pdf(self, pdf_file_path: str, stock_symbol: str) -> Dict[str, Any]:
        """
        Analyze SEC filing PDF (10-K, 10-Q) and provide Nigerian-focused summary.
        
        Args:
            pdf_file_path: Path to the SEC PDF file
            stock_symbol: Stock ticker symbol (e.g., "AAPL")
        
        Returns:
            Dictionary with simplified financial insights
        """
        try:
            # Upload PDF to Gemini using File API
            uploaded_file = genai.upload_file(path=pdf_file_path)
            
            # Create Nigerian-focused analysis prompt
            prompt = f"""
            You are analyzing a SEC filing for {stock_symbol} for a Nigerian retail investor.
            
            {self.ngn_usd_context}
            
            ANALYSIS INSTRUCTIONS:
            1. Extract ONLY the most critical information:
               - Company's main business (in simple terms)
               - Recent financial performance (revenue, profit trends)
               - Key risks mentioned
               - Future outlook/guidance
            
            2. TRANSLATE to Nigerian context:
               - Use simple English (no Wall Street jargon)
               - Reference Nigerian examples where possible
               - Explain WHY this matters to someone investing small amounts
               - Mention FX impact on returns
            
            3. FORMAT your response as JSON with these keys:
               - "company_overview": Brief description (2-3 sentences)
               - "financial_health": Revenue/profit summary in simple terms
               - "key_risks": List of 3-5 main risks
               - "investment_takeaway": Should a Nigerian investor consider this? (2-3 sentences)
               - "fx_consideration": How FX volatility affects this investment
            
            Keep everything concise and actionable. Avoid technical accounting terms.
            """

            # Generate analysis
            response = self.model.generate_content([uploaded_file, prompt])

            # Parse response (assuming JSON format)
            import json
            analysis = json.loads(response.text.strip().replace("```json", "").replace("```", ""))

            # Add metadata
            analysis["symbol"] = stock_symbol
            analysis["document_type"] = "SEC Filing"
            analysis["analysis_timestamp"] = self._get_timestamp()

            return analysis

        except Exception as e:
            # Check if it's a network-related error
            error_str = str(e).lower()
            network_keywords = ['network', 'connection', 'timeout', 'unreachable', 'failed to connect', '503', 'handshaker', 'tcp']
            if any(keyword in error_str for keyword in network_keywords):
                return {
                    "error": True,
                    "message": "The AI analysis service is currently unavailable due to network issues. Please check your internet connection and try again later.",
                    "symbol": stock_symbol
                }
            else:
                return {
                    "error": True,
                    "message": "The AI analysis service is currently unavailable. Please try again later.",
                    "symbol": stock_symbol
                }

    def analyze_earnings_audio(self, audio_file_path: str, stock_symbol: str) -> Dict[str, Any]:
        """
        Transcribe and analyze earnings call audio for Nigerian investors.
        
        Args:
            audio_file_path: Path to earnings call audio file
            stock_symbol: Stock ticker symbol
        
        Returns:
            Dictionary with CEO outlook and key takeaways
        """
        try:
            # Upload audio to Gemini using File API
            uploaded_file = genai.upload_file(path=pdf_file_path)

            # Create earnings call analysis prompt
            prompt = f"""
            You are analyzing an earnings call for {stock_symbol} for a Nigerian retail investor.
            
            {self.ngn_usd_context}
            
            ANALYSIS INSTRUCTIONS:
            1. Listen for:
               - CEO/CFO tone and confidence level
               - Revenue and profit performance
               - Future guidance and plans
               - Risks or challenges mentioned
               - Q&A concerns from analysts
            
            2. SIMPLIFY for Nigerian investor:
               - What did the CEO say in plain English?
               - Are they optimistic or worried? Why?
               - Any red flags or concerns?
               - What should a small investor know?
            
            3. FORMAT as JSON:
               - "executive_summary": 2-3 sentence overview
               - "ceo_outlook": CEO's tone (optimistic/neutral/cautious) + why
               - "key_numbers": Revenue/profit highlights in simple terms
               - "risks_mentioned": Main concerns discussed
               - "investor_takeaway": Should Nigerians pay attention? (2-3 sentences)
               - "next_steps": What to watch for next quarter
            
            Be conversational and honest. If the call was boring, say so.
            """

            # Generate analysis
            response = self.model.generate_content([uploaded_file, prompt])

            # Parse response
            import json
            analysis = json.loads(response.text.strip().replace("```json", "").replace("```", ""))

            # Add metadata
            analysis["symbol"] = stock_symbol
            analysis["document_type"] = "Earnings Call"
            analysis["analysis_timestamp"] = self._get_timestamp()

            return analysis

        except Exception as e:
            # Check if it's a network-related error
            error_str = str(e).lower()
            network_keywords = ['network', 'connection', 'timeout', 'unreachable', 'failed to connect', '503', 'handshaker', 'tcp']
            if any(keyword in error_str for keyword in network_keywords):
                return {
                    "error": True,
                    "message": "The AI analysis service is currently unavailable due to network issues. Please check your internet connection and try again later.",
                    "symbol": stock_symbol
                }
            else:
                return {
                    "error": True,
                    "message": "The AI analysis service is currently unavailable. Please try again later.",
                    "symbol": stock_symbol
                }

    def explain_portfolio_recommendation(
            self,
            portfolio_data: Dict[str, Any],
            budget_ngn: float,
            risk_level: str
    ) -> str:
        """
        Generate Nigerian-context explanation for portfolio recommendation.
        
        Args:
            portfolio_data: Portfolio dict from FinanceAPIService
            budget_ngn: Investment budget in Naira
            risk_level: Risk appetite (low/medium/high)
        
        Returns:
            Human-readable explanation string
        """
        try:
            prompt = f"""
            You are explaining an investment portfolio to a Nigerian investor.
            
            {self.ngn_usd_context}
            
            PORTFOLIO DETAILS:
            {portfolio_data}
            
            INVESTOR PROFILE:
            - Budget: ₦{budget_ngn:,}
            - Risk Tolerance: {risk_level}
            
            YOUR TASK:
            Write a friendly, conversational explanation (3-4 paragraphs) that:
            
            1. OPENS with what they're getting:
               - "With your ₦{budget_ngn:,}, here's what we recommend..."
               - Mention the stocks/ETFs in simple terms
            
            2. EXPLAINS each asset like you're talking to a friend:
               - What does this company do?
               - Why is it in your portfolio?
               - How much are you putting in it?
               - Use Nigerian analogies (e.g., "Apple is like Dangote - a giant everyone knows")
            
            3. ADDRESSES FX reality:
               - "Remember, you're buying in dollars but thinking in Naira"
               - Explain how Naira depreciation actually HELPS dollar investments
               - Be honest about FX risk
            
            4. CLOSES with expectations:
               - Realistic timeframe for seeing returns
               - What could go wrong (be honest!)
               - Encouragement to stay invested
            
            TONE: Friendly Nigerian English. Like a financial advisor who's also your big brother/sister.
            Use "you" and "your". No bullet points - write flowing paragraphs.
            """

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            # Check if it's a network-related error
            error_str = str(e).lower()
            network_keywords = ['network', 'connection', 'timeout', 'unreachable', 'failed to connect', '503', 'handshaker', 'tcp']
            if any(keyword in error_str for keyword in network_keywords):
                return "The AI explanation service is currently unavailable due to network issues. Please check your internet connection and try again later."
            else:
                return "The AI explanation service is currently unavailable. Please try again later."

    def explain_projections(
            self,
            projections_data: Dict[str, Any],
            budget_ngn: float,
            time_horizon: str
    ) -> str:
        """
        Explain future value projections in Nigerian context.
        
        Args:
            projections_data: Projections dict from FinanceAPIService
            budget_ngn: Initial investment in Naira
            time_horizon: Investment period
        
        Returns:
            Human-readable explanation
        """
        try:
            prompt = f"""
            You are explaining investment projections to a Nigerian investor.
            
            {self.ngn_usd_context}
            
            PROJECTION DATA:
            {projections_data}
            
            YOUR TASK:
            Write 2-3 paragraphs explaining:
            
            1. WHAT THESE NUMBERS MEAN:
               - Starting with ₦{budget_ngn:,}
               - Over {time_horizon.replace('_', ' ')}
               - Three scenarios: pessimistic, expected, optimistic
            
            2. REALISTIC EXPECTATIONS:
               - "In the best case, your money could grow to..."
               - "Most likely, you'll end up with..."
               - "Even in the worst case, you might have..."
               - Explain these are NOT guarantees
            
            3. NIGERIAN CONTEXT:
               - Compare to keeping money in Naira (loses value to inflation)
               - Compare to savings account (usually 5-8% annually)
               - Mention that USD assets protect against Naira depreciation
            
            TONE: Honest and educational. Don't oversell. Be realistic about risks.
            Use relatable examples like "enough for a new generator" or "1 month rent".
            """

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            # Check if it's a network-related error
            error_str = str(e).lower()
            network_keywords = ['network', 'connection', 'timeout', 'unreachable', 'failed to connect', '503', 'handshaker', 'tcp']
            if any(keyword in error_str for keyword in network_keywords):
                return "The AI projection service is currently unavailable due to network issues. Please check your internet connection and try again later."
            else:
                return "The AI projection service is currently unavailable. Please try again later."

    def simplify_financial_concept(self, concept: str, context: str = "") -> str:
        """
        Translate complex financial concepts into Nigerian plain English.
        
        Args:
            concept: Financial term or concept to explain
            context: Additional context if needed
        
        Returns:
            Simple explanation
        """
        try:
            prompt = f"""
            Explain this financial concept to a Nigerian investor who's new to US stocks:
            
            CONCEPT: {concept}
            {f"CONTEXT: {context}" if context else ""}
            
            {self.ngn_usd_context}
            
            REQUIREMENTS:
            - Use simple Nigerian English
            - Give a relatable local example if possible
            - Keep it to 2-3 sentences max
            - Avoid jargon
            
            Example format:
            "A 10-K filing is like a company's report card - it shows all their income, expenses, and plans for the year, just like how a business owner would review their books at year-end."
            """

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            # Check if it's a network-related error
            error_str = str(e).lower()
            network_keywords = ['network', 'connection', 'timeout', 'unreachable', 'failed to connect', '503', 'handshaker', 'tcp']
            if any(keyword in error_str for keyword in network_keywords):
                return "The AI service is currently unavailable due to network issues. Please check your internet connection and try again later."
            else:
                return "The AI service is currently unavailable. Please try again later."

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()


# Testing and example usage
if __name__ == "__main__":
    """
    Test the Gemini service with sample data.
    Note: Requires valid GEMINI_API_KEY environment variable.
    """

    # Initialize service
    service = GeminiService()

    # Test Case 1: Explain a sample portfolio
    print("=" * 60)
    print("TEST CASE 1: Portfolio Explanation")
    print("=" * 60)

    sample_portfolio = {
        "budget_ngn": 50000,
        "budget_usd": 32.47,
        "portfolio": [
            {
                "symbol": "VOO",
                "name": "Vanguard S&P 500 ETF",
                "allocation_percent": 60,
                "allocation_usd": 19.48,
                "shares": 0.0375
            },
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "allocation_percent": 40,
                "allocation_usd": 12.99,
                "shares": 0.0565
            }
        ]
    }

    explanation = service.explain_portfolio_recommendation(
        portfolio_data=sample_portfolio,
        budget_ngn=50000,
        risk_level="medium"
    )

    print(explanation)
    print("\n")

    # Test Case 2: Simplify a financial concept
    print("=" * 60)
    print("TEST CASE 2: Concept Simplification")
    print("=" * 60)

    concept_explanation = service.simplify_financial_concept(
        concept="P/E Ratio",
        context="Comparing tech stocks"
    )

    print(concept_explanation)