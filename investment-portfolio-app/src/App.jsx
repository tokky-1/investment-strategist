import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Divider,
  Chip,
  Stack,
  Fade,
} from "@mui/material";
import BudgetInput from "./components/BudgetInput";
import RiskSelector from "./components/RiskSelector";
import TimeHorizon from "./components/TimeHorizon";
import PortfolioTable from "./components/PortfolioTable";
import AllocationChart from "./components/AllocationChart";
import RiskCard from "./components/RiskCard";
import ProjectionCard from "./components/ProjectionCard";
import Notification from "./components/Notification";
import Footer from "./components/Footer";
import ThemeToggle from "./components/ThemeToggle";
import Report from "./components/Report";
import ConceptLookup from "./components/ConceptLookup";
// import AIAnalyst from "./components/AIAnalysts";
import { fetchPortfolio } from "./utils/portfolio";

export default function App() {
  const [budget, setBudget] = useState(50000);
  const [risk, setRisk] = useState("medium");
  const [horizon, setHorizon] = useState("1y");
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState("");
  const [error, setError] = useState(null);
  const [portfolio, setPortfolio] = useState([]);
  const [aiExplanation, setAiExplanation] = useState("");
  const [projections, setProjections] = useState(null);
  const [reportData, setReportData] = useState("");
  const [fxRate, setFxRate] = useState(null);

  // Fetch Live FX Rate on Load   // change here
  useEffect(() => {
    fetch("`${process.env.REACT_APP_API_URL}/api/market/fx-rate`")
      .then((res) => res.json())
      .then((data) => setFxRate(data.rate))
      .catch((err) => console.error("FX fetch failed", err));
  }, []);

  const buildPortfolio = async () => {
    setError(null);
    setReportData("");
    setAiExplanation("");
    setProjections(null);

    const nBudget = Number(budget);
    if (!nBudget || nBudget <= 0) {
      setError("Please enter a budget greater than 0 ₦.");
      return;
    }

    setLoading(true);
    const loadingSeq = [
      "Analyzing your budget…",
      "Connecting to market data…",
      "Gemini AI is crafting your strategy…",
    ];
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));

    try {
      for (const m of loadingSeq) {
        setLoadingMessage(m);
        await wait(700);
      }

      const data = await fetchPortfolio({ budget: nBudget, risk, horizon });

      if (!data.success)
        throw new Error(data.error?.message || "Failed to build portfolio");

      const portfolioItems = data.portfolio.portfolio.map((item) => ({
        symbol: item.symbol,
        type: item.type,
        allocationPercent: item.allocation_percent,
        priceUSD: item.price_usd,
        amountNGN: item.amount_ngn,
        estimatedShares: item.fractional_shares,
      }));

      setPortfolio(portfolioItems);
      setAiExplanation(data.ai_explanation);
      setProjections(data.portfolio.projection);
      const reportText = `
# INVESTMENT PORTFOLIO REPORT
**Generated:** ${new Date().toLocaleString()}
**Budget:** NGN ${nBudget.toLocaleString()}
**Risk Level:** ${risk.toUpperCase()}
**Time Horizon:** ${horizon}

## AI INVESTMENT STRATEGY
${data.ai_explanation.replace(/₦/g, "NGN ")}

## ASSET ALLOCATION
${portfolioItems.map((p) => `- **${p.symbol}**: NGN ${p.amountNGN.toLocaleString()} (${p.allocationPercent}%)`).join("\n")}

***
**DISCLAIMER:** ${data.portfolio.disclaimer}
`;

      setReportData(reportText);
    } catch (err) {
      setError(err.message || "Connection error. Ensure backend is running.");
      setPortfolio([]);
    } finally {
      setLoading(false);
      setLoadingMessage("");
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "var(--bg)", pb: 8 }}>
      <Container maxWidth="lg" sx={{ py: 6 }}>
        {/* Modern Header Section */}
        <Box
          display="flex"
          alignItems="flex-end"
          justifyContent="space-between"
          sx={{ mb: 6 }}
        >
          <Box>
            <Typography
              variant="overline"
              sx={{ letterSpacing: 2, color: "var(--accent)", fontWeight: 700 }}
            >
              Binary Intelligence
            </Typography>
            <Typography variant="h3" sx={{ fontWeight: 800, mt: -1 }}>
              Investment Strategist
            </Typography>
            {fxRate && (
              <Chip
                label={`1 USD = ₦${fxRate.toLocaleString()}`}
                variant="outlined"
                size="small"
                sx={{
                  mt: 1,
                  fontWeight: 600,
                  borderColor: "var(--accent)",
                  color: "var(--accent)",
                }}
              />
            )}
          </Box>
          <ThemeToggle />
        </Box>

        {/* Global Input Bar - Glassmorphism style */}
        <Card className="glass-card" sx={{ mb: 6, p: 1 }}>
          <CardContent>
            <Grid container spacing={3} alignItems="center">
              <Grid item xs={12} md={3}>
                <BudgetInput value={budget} onChange={setBudget} />
              </Grid>
              <Grid item xs={12} md={4}>
                <RiskSelector value={risk} onChange={setRisk} />
              </Grid>
              <Grid item xs={12} md={3}>
                <TimeHorizon value={horizon} onChange={setHorizon} />
              </Grid>
              <Grid item xs={12} md={2}>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={buildPortfolio}
                  disabled={loading}
                  sx={{
                    height: 56,
                    borderRadius: "12px",
                    boxShadow: "0 8px 16px rgba(25, 118, 210, 0.3)",
                    background: "linear-gradient(45deg, #1976d2, #42a5f5)",
                  }}
                >
                  {loading ? "Processing..." : "Generate Strategy"}
                </Button>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {loading && <Notification message={loadingMessage} />}
        {error && <Notification message={error} error />}

        {!loading && !error && portfolio.length > 0 && (
          <Fade in={true} timeout={800}>
            <Box>
              <Grid container spacing={4}>
                {/* Main Content Area */}
                <Grid item xs={12} md={8}>
                  <Stack spacing={4}>
                    <PortfolioTable rows={portfolio} />

                    {aiExplanation && (
                      <Card
                        sx={{
                          border: "none",
                          background:
                            "linear-gradient(135deg, rgba(25, 118, 210, 0.05) 0%, rgba(255,255,255,0) 100%)",
                          borderLeft: "6px solid var(--accent)",
                          position: "relative",
                          overflow: "hidden",
                        }}
                      >
                        <CardContent sx={{ p: 4 }}>
                          <Box
                            display="flex"
                            alignItems="center"
                            gap={1}
                            mb={2}
                          >
                            <Typography variant="h5" sx={{ fontWeight: 700 }}>
                              Strategic Rationale
                            </Typography>
                            <Chip
                              label="AI Powered"
                              color="primary"
                              size="small"
                              sx={{ fontWeight: 700 }}
                            />
                          </Box>

                          {/* Markdown Rendering Fix */}
                        <Box
  sx={{
    lineHeight: 1.8,
    fontSize: "1.05rem",
    color: "text.primary !important",
    "& p": { 
      mb: 2,
      color: "text.primary !important",
    },
    "& strong": {
      color: "primary.main",
      fontWeight: 700,
    },
    "& ul, & ol": { 
      pl: 3, 
      mb: 2,
      color: "text.primary !important",
    },
    "& li": { 
      mb: 1,
      color: "text.primary !important",
    },
  }}
>
  <ReactMarkdown>{aiExplanation}</ReactMarkdown>
</Box>
                        </CardContent>
                      </Card>
                    )}
                    <Report data={reportData} />
                  </Stack>
                </Grid>

                {/* Sidebar - Grouped Intelligence */}
                <Grid item xs={12} md={4}>
                  <Stack spacing={3}>
                    <AllocationChart data={portfolio} />
                    <Typography
                      variant="subtitle2"
                      sx={{
                        opacity: 0.6,
                        letterSpacing: 1,
                        textTransform: "uppercase",
                        px: 1,
                      }}
                    >
                      Deep Analysis Tools
                    </Typography>
                  
                    <ConceptLookup />
                    <Divider />
                    <ProjectionCard backendData={projections} />
                    <RiskCard risk={risk} />
                  </Stack>
                </Grid>
              </Grid>
            </Box>
          </Fade>
        )}
        <Footer />
      </Container>
    </Box>
  );
}
