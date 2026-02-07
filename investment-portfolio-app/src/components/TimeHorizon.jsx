import React from "react";
import {
  ToggleButtonGroup,
  ToggleButton,
  Box,
  Typography,
} from "@mui/material";

export default function TimeHorizon({ value, onChange }) {
  return (
    <Box sx={{ width: "100%" }}>
      <Typography
        variant="caption"
        sx={{ mb: 1, display: "block", color: "var(--muted)", fontWeight: 600 }}
      >
        INVESTMENT HORIZON
      </Typography>
      <Box
        sx={{
          overflowX: "auto",
          display: "flex",
          pb: 1, // Space for scrollbar
          "&::-webkit-scrollbar": {
            height: 4,
          },
          "&::-webkit-scrollbar-track": {
            background: "transparent",
          },
          "&::-webkit-scrollbar-thumb": {
            backgroundColor: "rgba(25, 118, 210, 0.2)",
            borderRadius: 10,
          },
          scrollbarWidth: "thin",
          scrollbarColor: "rgba(25, 118, 210, 0.2) transparent",
        }}
      >
        <ToggleButtonGroup
          value={value}
          exclusive
          onChange={(e, v) => v && onChange(v)}
          aria-label="time horizon"
          sx={{
            display: "flex",
            gap: 1,
            "& .MuiToggleButtonGroup-grouped": {
              border: "1px solid rgba(25, 118, 210, 0.12) !important",
              borderRadius: "20px !important", // Pill shape
              px: 2,
              py: 0.5,
              fontSize: "0.8rem",
              whiteSpace: "nowrap",
              backgroundColor: "var(--card-bg)",
              color: "var(--text)",
              transition: "all 0.2s ease-in-out",
              "&.Mui-selected": {
                backgroundColor: "rgba(25, 118, 210, 0.1) !important",
                color: "var(--accent) !important",
                borderColor: "var(--accent) !important",
                fontWeight: "bold",
              },
              "&:hover": {
                backgroundColor: "rgba(25, 118, 210, 0.05)",
                transform: "translateY(-1px)",
              },
            },
          }}
        >
          <ToggleButton value="6m">6 Months</ToggleButton>
          <ToggleButton value="1y">1 Year</ToggleButton>
          <ToggleButton value="2y">2 Years</ToggleButton>
          <ToggleButton value="3y">3 Years</ToggleButton>
          <ToggleButton value="4y">4 Years</ToggleButton>
        </ToggleButtonGroup>
      </Box>
    </Box>
  );
}
