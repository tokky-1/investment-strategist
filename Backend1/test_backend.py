"""
test_backend.py
Quick test script to verify backend functionality

Run this after setting up your .env file to make sure everything works.
"""

import requests
import json

class BackendTester:
    """Test suite for the Intelligent Investment Strategist API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
    
    def print_header(self, title: str):
        """Print formatted test section header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def print_result(self, test_name: str, passed: bool, details: str = ""):
        """Print test result"""
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
        if details:
            print(f"   Details: {details}")
        self.test_results.append((test_name, passed))
    
    def test_health_check(self):
        """Test if server is running"""
        self.print_header("Health Check")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            passed = response.status_code == 200
            self.print_result(
                "Server Health Check",
                passed,
                f"Status: {response.status_code}"
            )
            if passed:
                print(f"   Response: {json.dumps(response.json(), indent=2)}")
            return passed
        except requests.exceptions.ConnectionError:
            self.print_result(
                "Server Health Check",
                False,
                "Cannot connect to server. Is it running?"
            )
            return False
        except Exception as e:
            self.print_result(
                "Server Health Check",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_fx_rate(self):
        """Test FX rate endpoint"""
        self.print_header("FX Rate Endpoint")
        try:
            response = requests.get(f"{self.base_url}/api/market/fx-rate")
            passed = response.status_code == 200
            self.print_result(
                "Get NGN/USD Exchange Rate",
                passed,
                f"Status: {response.status_code}"
            )
            if passed:
                data = response.json()
                print(f"   Current Rate: {data.get('description', 'N/A')}")
            return passed
        except Exception as e:
            self.print_result(
                "Get NGN/USD Exchange Rate",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_stock_price(self):
        """Test stock price endpoint"""
        self.print_header("Stock Price Endpoint")
        try:
            payload = {"symbol": "AAPL"}
            response = requests.post(
                f"{self.base_url}/api/market/stock-price",
                json=payload
            )
            passed = response.status_code == 200
            self.print_result(
                "Get Stock Price (AAPL)",
                passed,
                f"Status: {response.status_code}"
            )
            if passed:
                data = response.json()
                print(f"   AAPL Price: ${data.get('price_usd', 'N/A')}")
            return passed
        except Exception as e:
            self.print_result(
                "Get Stock Price",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_portfolio_build(self):
        """Test portfolio building endpoint"""
        self.print_header("Portfolio Building Endpoint")
        try:
            payload = {
                "budget_ngn": 50000,
                "risk_level": "medium",
                "time_horizon": "1_year"
            }
            response = requests.post(
                f"{self.base_url}/api/portfolio/build",
                json=payload
            )
            passed = response.status_code == 200
            self.print_result(
                "Build Portfolio (₦50,000, Medium Risk)",
                passed,
                f"Status: {response.status_code}"
            )
            if passed:
                data = response.json()
                portfolio = data.get('portfolio', {})
                print(f"   Budget (NGN): ₦{portfolio.get('budget_ngn', 'N/A'):,}")
                print(f"   Budget (USD): ${portfolio.get('budget_usd', 'N/A')}")
                print(f"   Assets Allocated: {len(portfolio.get('portfolio', []))}")
                
                # Print AI explanation preview
                explanation = data.get('ai_explanation', '')
                if explanation:
                    preview = explanation[:200] + "..." if len(explanation) > 200 else explanation
                    print(f"   AI Explanation Preview:\n   {preview}")
            return passed
        except Exception as e:
            self.print_result(
                "Build Portfolio",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_projections(self):
        """Test projections endpoint"""
        self.print_header("Projections Endpoint")
        try:
            payload = {
                "budget_ngn": 50000,
                "risk_level": "medium",
                "time_horizon": "1_year"
            }
            response = requests.post(
                f"{self.base_url}/api/portfolio/projections",
                json=payload
            )
            passed = response.status_code == 200
            self.print_result(
                "Calculate Projections (1 Year)",
                passed,
                f"Status: {response.status_code}"
            )
            if passed:
                data = response.json()
                projections = data.get('projections', {})
                scenarios = projections.get('scenarios', {})
                
                print(f"   Initial Investment: {projections.get('initial_investment', 'N/A')}")
                print(f"   Time Horizon: {projections.get('time_horizon', 'N/A')}")
                
                if scenarios:
                    print(f"   Pessimistic: {scenarios.get('pessimistic', {}).get('value', 'N/A')}")
                    print(f"   Expected: {scenarios.get('expected', {}).get('value', 'N/A')}")
                    print(f"   Optimistic: {scenarios.get('optimistic', {}).get('value', 'N/A')}")
            return passed
        except Exception as e:
            self.print_result(
                "Calculate Projections",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_approved_assets(self):
        """Test approved assets endpoint"""
        self.print_header("Approved Assets Endpoint")
        try:
            response = requests.get(f"{self.base_url}/api/market/approved-assets")
            passed = response.status_code == 200
            self.print_result(
                "Get Approved Assets List",
                passed,
                f"Status: {response.status_code}"
            )
            if passed:
                data = response.json()
                assets = data.get('assets', {})
                print(f"   Total Assets: {len(assets)}")
                print(f"   Assets: {', '.join(assets.keys())}")
            return passed
        except Exception as e:
            self.print_result(
                "Get Approved Assets",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_risk_levels(self):
        """Test risk levels utility endpoint"""
        self.print_header("Risk Levels Utility")
        try:
            response = requests.get(f"{self.base_url}/api/utils/risk-levels")
            passed = response.status_code == 200
            self.print_result(
                "Get Risk Levels Info",
                passed,
                f"Status: {response.status_code}"
            )
            if passed:
                data = response.json()
                risk_levels = data.get('risk_levels', {})
                print(f"   Available Risk Levels: {', '.join(risk_levels.keys())}")
            return passed
        except Exception as e:
            self.print_result(
                "Get Risk Levels",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        total = len(self.test_results)
        passed = sum(1 for _, result in self.test_results if result)
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n❌ Failed Tests:")
            for name, result in self.test_results:
                if not result:
                    print(f"   - {name}")
        else:
            print("\n🎉 All tests passed! Backend is working perfectly!")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("\n" + "🚀 Starting Backend Tests ".center(70, "="))
        print(f"Testing API at: {self.base_url}")
        
        # Critical tests first
        if not self.test_health_check():
            print("\n❌ Server is not running. Please start the backend first:")
            print("   python main.py")
            return
        
        # Run all endpoint tests
        self.test_fx_rate()
        self.test_stock_price()
        self.test_approved_assets()
        self.test_risk_levels()
        self.test_portfolio_build()
        self.test_projections()
        
        # Print summary
        self.print_summary()


def main():
    """Main test execution"""
    tester = BackendTester()
    tester.run_all_tests()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║  Intelligent Investment Strategist - Backend Test Suite        ║
    ║  Testing all API endpoints and functionality                   ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    main()
