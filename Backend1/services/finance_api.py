"""
finance_api.py
Backend Service: Market Data & Financial Logic

Responsibilities:
- Fetch live US stock prices (USD)
- Fetch NGN/USD exchange rate
- Perform all financial calculations (budget → USD → shares)
- Return deterministic, clean data to main.py

Author: Backend Dev 2 - Market Data & Logic Engineer
"""

import requests
from typing import Any, Dict, List, Optional


class FinanceAPIService:
    """
    Handles all external market data fetching and financial calculations.
    No AI logic - only numbers and data.
    """
    
    def __init__(self):
        """Initialize API keys and base URLs"""
        from config import settings
        # API Keys from config
        self.finnhub_api_key = settings.finnhub_api_key
        self.exchange_rate_api_key = settings.exchange_rate_api_key
        
        # Base URLs
        self.finnhub_base_url = "https://finnhub.io/api/v1"
        self.exchange_rate_base_url = "https://api.exchangerate-api.com/v4/latest/USD"
        
        # Pre-approved asset universe (hackathon-safe)
        self.approved_assets = {
            "VOO": "ETF",
            "SPY": "ETF",
            "AAPL": "Stock",
            "MSFT": "Stock",
            "JNJ": "Stock",
            "KO": "Stock"
        }
        
        # Asset characteristics for realistic modeling
        # Based on 30+ years of historical data
        self.asset_characteristics = {
            # S&P 500 ETFs
            "VOO": {
                "expected_return": 0.10,   # 10% annually
                "volatility": 0.18,        # 18% annual volatility
                "asset_class": "Broad Market ETF"
            },
            "SPY": {
                "expected_return": 0.10,
                "volatility": 0.18,
                "asset_class": "Broad Market ETF"
            },
            # Large-cap Tech
            "AAPL": {
                "expected_return": 0.15,   # 15% annually (higher growth)
                "volatility": 0.25,        # 25% annual volatility (higher risk)
                "asset_class": "Large-Cap Tech"
            },
            "MSFT": {
                "expected_return": 0.15,
                "volatility": 0.25,
                "asset_class": "Large-Cap Tech"
            },
            # Defensive Stocks
            "JNJ": {
                "expected_return": 0.07,   # 7% annually (lower growth)
                "volatility": 0.15,        # 15% annual volatility (lower risk)
                "asset_class": "Defensive"
            },
            "KO": {
                "expected_return": 0.07,
                "volatility": 0.15,
                "asset_class": "Defensive"
            }
        }
        
        # FX parameters (NGN/USD)
        self.fx_characteristics = {
            "expected_depreciation": -0.04,  # Naira typically depreciates 4% annually
            "fx_volatility": 0.10            # 10% annual FX volatility
        }
    
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """
        Fetch current stock price in USD from Finnhub.
        
        Args:
            symbol: Stock ticker symbol (e.g., "AAPL")
        
        Returns:
            Current price in USD, or None if request fails
        """
        try:
            url = f"{self.finnhub_base_url}/quote"
            params = {
                "symbol": symbol,
                "token": self.finnhub_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current_price = data.get("c")  # 'c' is current price in Finnhub
            
            if current_price and current_price > 0:
                return round(float(current_price), 2)
            else:
                # Fallback for demo/testing purposes
                return self._get_fallback_price(symbol)
                
        except Exception as e:
            print(f"Error fetching price for {symbol}: {str(e)}")
            return self._get_fallback_price(symbol)
    
    def _get_fallback_price(self, symbol: str) -> float:
        """
        Fallback prices for demo resilience.
        These are approximate prices as of Jan 2025.
        """
        fallback_prices = {
            "VOO": 520.00,
            "SPY": 580.00,
            "AAPL": 230.00,
            "MSFT": 425.00,
            "JNJ": 155.00,
            "KO": 62.00
        }
        return fallback_prices.get(symbol, 100.00)
    
    def get_fx_rate(self) -> Optional[float]:
        """
        Fetch current NGN/USD exchange rate.
        
        Returns:
            Exchange rate (how many Naira per 1 USD), or fallback rate
        """
        try:
            response = requests.get(self.exchange_rate_base_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get("rates", {})
            ngn_rate = rates.get("NGN")
            
            if ngn_rate and ngn_rate > 0:
                return round(float(ngn_rate), 2)
            else:
                return self._get_fallback_fx_rate()
                
        except Exception as e:
            print(f"Error fetching FX rate: {str(e)}")
            return self._get_fallback_fx_rate()
    
    def _get_fallback_fx_rate(self) -> float:
        """
        Fallback FX rate for demo resilience.
        Approximate NGN/USD rate as of Jan 2025.
        """
        return 1540.00
    
    def calculate_usd_buying_power(self, budget_ngn: float, fx_rate: float) -> float:
        """
        Convert Naira budget to USD buying power.
        
        Formula: USD Buying Power = Budget (₦) / Exchange Rate (₦/USD)
        
        Args:
            budget_ngn: Budget in Nigerian Naira
            fx_rate: NGN/USD exchange rate
        
        Returns:
            USD equivalent of the budget
        """
        if fx_rate <= 0:
            raise ValueError("FX rate must be positive")
        
        usd_power = budget_ngn / fx_rate
        return round(usd_power, 2)
    
    def calculate_allocation(
        self, 
        budget_ngn: float, 
        allocation_percent: float, 
        fx_rate: float
    ) -> Dict[str, float]:
        """
        Calculate allocation amounts in both NGN and USD.
        
        Args:
            budget_ngn: Total budget in Naira
            allocation_percent: Percentage allocated to this asset (0-100)
            fx_rate: NGN/USD exchange rate
        
        Returns:
            Dictionary with 'amount_ngn' and 'amount_usd'
        """
        allocation_ngn = budget_ngn * (allocation_percent / 100)
        allocation_usd = allocation_ngn / fx_rate
        
        return {
            "amount_ngn": round(allocation_ngn, 2),
            "amount_usd": round(allocation_usd, 2)
        }
    
    def calculate_fractional_shares(
        self, 
        allocation_usd: float, 
        stock_price_usd: float
    ) -> float:
        """
        Calculate fractional shares affordable with USD allocation.
        
        Formula: Fractional Shares = Allocation (USD) / Stock Price (USD)
        
        Args:
            allocation_usd: Amount in USD allocated to this asset
            stock_price_usd: Current price of the stock in USD
        
        Returns:
            Number of fractional shares (e.g., 0.11)
        """
        if stock_price_usd <= 0:
            raise ValueError("Stock price must be positive")
        
        fractional_shares = allocation_usd / stock_price_usd
        return round(fractional_shares, 3)
    
    def get_allocation_template(self, risk_level: str) -> List[Dict[str, Any]]:
        """
        Return pre-defined allocation template based on risk level.
        
        These templates are FIXED for stability and demo reliability.
        Backend enforces max 4 assets, no penny stocks, no leverage.
        
        Args:
            risk_level: "low" | "medium" | "high"
        
        Returns:
            List of asset allocations with symbol, type, and percentage
        """
        templates = {
            "low": [
                {"symbol": "VOO", "type": "ETF", "percent": 70},
                {"symbol": "JNJ", "type": "Stock", "percent": 30}
            ],
            "medium": [
                {"symbol": "SPY", "type": "ETF", "percent": 50},
                {"symbol": "AAPL", "type": "Stock", "percent": 30},
                {"symbol": "KO", "type": "Stock", "percent": 20}
            ],
            "high": [
                {"symbol": "VOO", "type": "ETF", "percent": 40},
                {"symbol": "AAPL", "type": "Stock", "percent": 35},
                {"symbol": "MSFT", "type": "Stock", "percent": 25}
            ]
        }
        
        return templates.get(risk_level.lower(), templates["medium"])
    
    def build_portfolio(
        self, 
        budget_ngn: float, 
        risk_level: str, 
        time_horizon: str | int
    ) -> Dict:
        """
        Main orchestration function: builds complete portfolio with all calculations.
        
        This is the core function that main.py will call.
        
        Process:
        1. Fetch FX rate
        2. Get allocation template for risk level
        3. Fetch prices for all assets
        4. Calculate allocations and fractional shares
        5. Return clean JSON
        
        Args:
            budget_ngn: Budget in Nigerian Naira
            risk_level: "low" | "medium" | "high"
            time_horizon: Either "6_months" | "1_year" | "3_years" OR integer months (1-120)
        
        Returns:
            Complete portfolio dictionary matching backend spec
        """
        # Step 1: Fetch FX rate
        fx_rate = self.get_fx_rate()
        if fx_rate is None:
            raise ValueError("Failed to fetch FX rate")
        usd_buying_power = self.calculate_usd_buying_power(budget_ngn, fx_rate)
        
        # Step 2: Get allocation template
        allocation_template = self.get_allocation_template(risk_level)
        
        # Step 3: Build portfolio with pricing
        portfolio = []
        
        for asset in allocation_template:
            symbol = asset["symbol"]
            asset_type = asset["type"]
            percent = asset["percent"]
            
            # Fetch current price
            price_usd = self.get_stock_price(symbol)
            
            if price_usd is None:
                continue  # Skip if price unavailable
            
            # Calculate allocation amounts
            allocation = self.calculate_allocation(budget_ngn, percent, fx_rate)
            
            # Calculate fractional shares
            fractional_shares = self.calculate_fractional_shares(
                allocation["amount_usd"], 
                price_usd
            )
            
            # Build asset entry
            portfolio.append({
                "symbol": symbol,
                "type": asset_type,
                "allocation_percent": percent,
                "price_usd": price_usd,
                "amount_ngn": allocation["amount_ngn"],
                "fractional_shares": fractional_shares
            })
        
        # Step 4: Build projection (educational estimate with realistic modeling)
        projection = self._generate_projection(budget_ngn, risk_level, time_horizon, portfolio)
        
        # Step 5: Return complete response
        return {
            "budget_ngn": budget_ngn,
            "fx_rate": fx_rate,
            "usd_buying_power": usd_buying_power,
            "risk_level": risk_level,
            "time_horizon": time_horizon,
            "portfolio": portfolio,
            "projection": projection,
            "disclaimer": "This is an educational simulation and not financial advice. Returns are not guaranteed."
        }
    
    def _generate_projection(
        self, 
        budget_ngn: float, 
        risk_level: str, 
        time_horizon: str | int,
        portfolio: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Generate realistic projection using lognormal distribution model.
        
        This model:
        1. Uses asset-specific expected returns and volatility
        2. Accounts for FX (NGN/USD) impact
        3. Uses proper compounding (geometric returns)
        4. Provides three scenarios: pessimistic, expected, optimistic
        
        Mathematical approach:
        - Lognormal distribution (industry standard for stock returns)
        - Compound annual growth rate (CAGR)
        - FX risk modeled separately and combined
        
        Args:
            budget_ngn: Original budget
            risk_level: Risk level (used for validation)
            time_horizon: Investment period (string like "1_year" or integer months)
            portfolio: List of portfolio assets with allocations
        
        Returns:
            Detailed projection with scenarios and assumptions
        """
        import math
        
        # Handle both string formats and integer months
        if isinstance(time_horizon, int):
            years = time_horizon / 12.0
            horizon_display = f"{time_horizon} months" if time_horizon != 12 else "1 year"
        else:
            horizon_map = {
                "3_months": 0.25,
                "6_months": 0.5,
                "1_year": 1.0,
                "2_years": 2.0,
                "3_years": 3.0,
                "4_years": 4.0,
                "5_years": 5.0,
                "6_years": 6.0,
                "7_years": 7.0,
                "8_years": 8.0,
                "9_years": 9.0,
                "10_years": 10.0
            }
            years = horizon_map.get(time_horizon, 1.0)
            horizon_display = time_horizon.replace("_", " ")
        
        # Calculate portfolio-weighted return and volatility
        if portfolio and len(portfolio) > 0:
            portfolio_stats = self._calculate_portfolio_statistics(portfolio)
            portfolio_return = portfolio_stats["expected_return"]
            portfolio_volatility = portfolio_stats["volatility"]
        else:
            # Fallback to risk-based estimates
            fallback_stats = {
                "low": {"return": 0.08, "volatility": 0.15},
                "medium": {"return": 0.10, "volatility": 0.18},
                "high": {"return": 0.13, "volatility": 0.22}
            }
            stats = fallback_stats.get(risk_level.lower(), fallback_stats["medium"])
            portfolio_return = stats["return"]
            portfolio_volatility = stats["volatility"]
        
        # Add FX impact (critical for Nigerian investors)
        fx_drift = self.fx_characteristics["expected_depreciation"]
        fx_vol = self.fx_characteristics["fx_volatility"]
        
        # Combined return (stock return in USD + FX change)
        # Note: Negative FX drift means Naira depreciates, which INCREASES NGN value of USD assets
        total_return = portfolio_return - fx_drift  # Subtract because depreciation helps us
        
        # Combined volatility (using correlation = 0.3 between stocks and FX)
        # sqrt(σ_stock² + σ_fx² + 2*ρ*σ_stock*σ_fx)
        correlation = 0.3
        total_volatility = math.sqrt(
            portfolio_volatility**2 + 
            fx_vol**2 + 
            2 * correlation * portfolio_volatility * fx_vol
        )
        
        # Lognormal distribution parameters
        drift = (total_return - 0.5 * total_volatility**2) * years
        diffusion = total_volatility * math.sqrt(years)
        
        # Calculate scenarios using percentiles
        # 25th percentile (pessimistic - 25% chance of worse)
        pessimistic_multiplier = math.exp(drift - 0.674 * diffusion)
        pessimistic_value = budget_ngn * pessimistic_multiplier
        
        # 50th percentile (expected/median - most likely)
        expected_multiplier = math.exp(drift)
        expected_value = budget_ngn * expected_multiplier
        
        # 75th percentile (optimistic - 25% chance of better)
        optimistic_multiplier = math.exp(drift + 0.674 * diffusion)
        optimistic_value = budget_ngn * optimistic_multiplier
        
        # Calculate returns as percentages
        pessimistic_return = (pessimistic_multiplier - 1) * 100
        expected_return = (expected_multiplier - 1) * 100
        optimistic_return = (optimistic_multiplier - 1) * 100
        
        # Build comprehensive projection response
        return {
            "initial_investment": f"₦{budget_ngn:,.0f}",
            "time_horizon": horizon_display,
            "scenarios": {
                "pessimistic": {
                    "value": f"₦{pessimistic_value:,.0f}",
                    "return_percent": f"{pessimistic_return:+.1f}%",
                    "description": "Pessimistic scenario (25% chance of worse outcome)"
                },
                "expected": {
                    "value": f"₦{expected_value:,.0f}",
                    "return_percent": f"{expected_return:+.1f}%",
                    "description": "Most likely outcome based on historical patterns"
                },
                "optimistic": {
                    "value": f"₦{optimistic_value:,.0f}",
                    "return_percent": f"{optimistic_return:+.1f}%",
                    "description": "Optimistic scenario (25% chance of better outcome)"
                }
            },
            "assumptions": {
                "stock_return_usd": f"{portfolio_return * 100:.1f}% annually",
                "fx_impact": f"{-fx_drift * 100:+.1f}% (Naira depreciation benefit)",
                "total_expected_return": f"{total_return * 100:.1f}% in Naira terms",
                "portfolio_volatility": f"{total_volatility * 100:.1f}% annually"
            },
            "methodology": "Lognormal distribution with geometric compounding",
            "risk_factors": self._get_risk_factors(years, total_volatility),
            "disclaimer": "These projections are based on historical market behavior and assume normal market conditions. Actual outcomes may vary significantly due to market volatility, geopolitical events, and FX fluctuations. Past performance does not guarantee future results."
        }
    
    def _calculate_portfolio_statistics(self, portfolio: List[Dict]) -> Dict[str, float]:
        """
        Calculate weighted expected return and volatility for the portfolio.
        
        Uses Modern Portfolio Theory (MPT) principles.
        
        Args:
            portfolio: List of assets with symbols and allocation percentages
        Returns:
            Dictionary with expected_return and volatility
        """
        import math
        
        total_weight = 0
        weighted_return = 0
        weighted_variance = 0
        
        for asset in portfolio:
            symbol = asset["symbol"]
            weight = asset["allocation_percent"] / 100.0
            
            # Get asset characteristics
            chars = self.asset_characteristics.get(symbol, {
                "expected_return": 0.10,
                "volatility": 0.18
            })
            
            # Weighted return
            weighted_return += weight * chars["expected_return"]
            
            # Weighted variance (simplified - assumes low correlation between assets)
            weighted_variance += (weight * chars["volatility"])**2
            
            total_weight += weight
        
        # Portfolio volatility is sqrt of weighted variance
        portfolio_volatility = math.sqrt(weighted_variance)
        
        return {
            "expected_return": weighted_return,
            "volatility": portfolio_volatility
        }
    
    def _get_risk_factors(self, years: float, volatility: float) -> List[str]:
        """
        Generate contextual risk factors based on time horizon and volatility.
        
        Args:
            years: Investment time horizon in years
            volatility: Total portfolio volatility
        
        Returns:
            List of relevant risk factor descriptions
        """
        risk_factors = []
        
        # Time-based risks
        if years < 1:
            risk_factors.append("Short-term investments are highly volatile - expect significant fluctuations")
        elif years < 2:
            risk_factors.append("Medium-term horizon allows some volatility smoothing but remains uncertain")
        else:
            risk_factors.append("Long-term horizon reduces impact of short-term volatility")
        
        # Volatility-based risks
        if volatility > 0.20:
            risk_factors.append("High portfolio volatility - value may swing ±30% or more")
        elif volatility > 0.15:
            risk_factors.append("Moderate volatility - expect fluctuations of ±20-30%")
        else:
            risk_factors.append("Lower volatility portfolio - relatively stable growth expected")
        
        # Nigerian-specific risks
        risk_factors.append("FX risk: Naira depreciation increases USD asset value but also increases local currency "
                            "volatility")
        risk_factors.append("Market access: Liquidity depends on broker availability and FX regulations")
        
        return risk_factors
    """
     Returns:
            Detailed projection with scenarios and assumptions
     """
    def calculate_projections(
        self, 
        budget_ngn: float, 
        risk_level: str, 
        time_horizon: str,
        portfolio: Optional[List[Dict[str, Any]]] = None
        ) -> Dict:
            return self._generate_projection(
                budget_ngn=budget_ngn,
                risk_level=risk_level,
                time_horizon=time_horizon,
                portfolio=portfolio
            )


# Example usage and testing
if __name__ == "__main__":
    """
    Test the finance API service with sample inputs.
    Run this file directly to verify everything works.
    """
    
    # Initialize service
    service = FinanceAPIService()
    
    # Test Case 1: Medium risk, 1 year, ₦50,000 budget
    print("=" * 60)
    print("TEST CASE 1: Medium Risk Portfolio")
    print("=" * 60)
    
    portfolio = service.build_portfolio(
        budget_ngn=50000,
        risk_level="medium",
        time_horizon="1_year"
    )
    
    import json
    print(json.dumps(portfolio, indent=2))
    
    # Test Case 2: Low risk, 6 months, ₦20,000 budget
    print(" " + "=" * 60)
    print("TEST CASE 2: Low Risk Portfolio")
    print("=" * 60)
    
    portfolio_low = service.build_portfolio(
        budget_ngn=20000,
        risk_level="low",
        time_horizon="6_months"
    )
    
    print(json.dumps(portfolio_low, indent=2))