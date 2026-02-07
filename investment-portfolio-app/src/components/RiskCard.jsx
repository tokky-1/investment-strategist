import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'

const EXPLANATIONS = {
  low: 'Low risk: Emphasizes bonds and stable assets. Lower volatility, lower expected returns.',
  medium: 'Medium risk: Balanced mix of equities and bonds. Aims for growth with moderation.',
  high: 'High risk: Equity-heavy; higher potential returns and higher volatility.'
}

export default function RiskCard({ risk }) {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="subtitle1">Risk Summary</Typography>
        <Typography variant="h6" sx={{ mt: 1, textTransform: 'capitalize' }}>
          {risk}
        </Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>
          FX exposure: Prices shown assume a representative FX rate. {EXPLANATIONS[risk]}
        </Typography>
      </CardContent>
    </Card>
  )
}
