import React from "react";
import { Card, CardContent, Typography, Box, Divider } from "@mui/material";

export default function ProjectionCard({ backendData }) {
  if (!backendData) return null;

  const { scenarios, assumptions, methodology } = backendData;

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="subtitle1" gutterBottom>
          Realistic Projections
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Horizon: {backendData.time_horizon}
        </Typography>

        <Box sx={{ mt: 2 }}>
          <Box display="flex" justifyContent="space-between">
            <Typography variant="body2" color="error">
              Pessimistic:
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {scenarios.pessimistic.value}
            </Typography>
          </Box>
          <Box display="flex" justifyContent="space-between" sx={{ my: 1 }}>
            <Typography variant="h6" color="primary">
              Expected:
            </Typography>
            <Typography variant="h6" fontWeight="bold">
              {scenarios.expected.value}
            </Typography>
          </Box>
          <Box display="flex" justifyContent="space-between">
            <Typography variant="body2" color="success.main">
              Optimistic:
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {scenarios.optimistic.value}
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Typography variant="caption" display="block">
          Stock Return: {assumptions.stock_return_usd}
        </Typography>
        <Typography variant="caption" display="block">
          FX Impact: {assumptions.fx_impact}
        </Typography>
        <Typography
          variant="caption"
          sx={{ mt: 1, display: "block", fontStyle: "italic" }}
        >
          Method: {methodology}
        </Typography>
      </CardContent>
    </Card>
  );
}
