import React, { useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
  Divider,
  CircularProgress,
} from "@mui/material";

export default function ConceptLookup() {
  const [concept, setConcept] = useState("");
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);

  const handleExplain = async () => {
    if (!concept) return;
    setLoading(true);
    try {
      const response = await fetch(   // here as well
       `${process.env.REACT_APP_API_URL}/api/ai/explain-concept`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ concept }),
        },
      );
      const data = await response.json();
      setExplanation(data.explanation);
    } catch (err) {
      setExplanation("Could not translate this jargon. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="subtitle1" gutterBottom>
          Translate Financial Jargon
        </Typography>
        <Box display="flex" gap={1} mb={2}>
          <TextField
            fullWidth
            size="small"
            placeholder="e.g. Dividend"
            value={concept}
            onChange={(e) => setConcept(e.target.value)}
          />
          <Button
            variant="contained"
            onClick={handleExplain}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : "Explain"}
          </Button>
        </Box>
        {explanation && (
          <>
            <Divider sx={{ my: 1 }} />
            <Typography
              variant="body2"
              sx={{ color: "text.secondary", fontStyle: "italic", mt: 1 }}
            >
              {explanation}
            </Typography>
          </>
        )}
      </CardContent>
    </Card>
  );
}
