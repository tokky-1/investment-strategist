import React, { useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  Button,
  Stack,
  LinearProgress,
  Box,
  Chip,
  Divider,
  Fade,
} from "@mui/material";

export default function AIAnalyst({ symbol = "AAPL" }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async (file) => {
    if (!file) return;
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("symbol", symbol);

    try {
      // Endpoint updated to focus only on SEC filings // here
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/analysis/sec-filing`,
        {
          method: "POST",
          body: formData,
        },
      );
      const data = await response.json();
      if (data.success) {
        setResult(data.analysis);
      }
    } catch (err) {
      console.error("SEC Analysis failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="glass-card" sx={{ mb: 2, borderRadius: "16px" }}>
      <CardContent>
        <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 2 }}>
          SEC Filing Intelligence: {symbol}
        </Typography>

        <Stack direction="row" spacing={1} mb={2}>
          <Button
            variant="contained"
            component="label"
            size="small"
            fullWidth
            sx={{ borderRadius: "8px", textTransform: "none" }}
          >
            Upload 10-K / 10-Q (PDF)
            <input
              type="file"
              hidden
              accept="application/pdf"
              onChange={(e) => handleUpload(e.target.files[0])}
            />
          </Button>
        </Stack>

        {loading && (
          <Box sx={{ my: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Extracting insights from PDF...
            </Typography>
            <LinearProgress sx={{ mt: 1, borderRadius: 1 }} />
          </Box>
        )}

        {result && (
          <Fade in={true}>
            <Box
              sx={{ bgcolor: "rgba(0,0,0,0.03)", p: 2, borderRadius: 3, mt: 2 }}
            >
              <Typography
                variant="subtitle2"
                color="primary"
                sx={{ fontWeight: 700 }}
              >
                {result.document_type} Results
              </Typography>
              <Divider sx={{ my: 1.5, opacity: 0.5 }} />
              <Typography variant="body2" sx={{ lineHeight: 1.6, mb: 2 }}>
                {result.company_overview || result.investment_takeaway}
              </Typography>
              <Stack direction="row" spacing={1}>
                <Chip
                  label="Financials Extracted"
                  size="small"
                  variant="outlined"
                />
                <Chip label="FX Adjusted" size="small" variant="outlined" />
              </Stack>
            </Box>
          </Fade>
        )}
      </CardContent>
    </Card>
  );
}
