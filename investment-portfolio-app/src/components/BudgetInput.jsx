import React from 'react'
import { TextField } from '@mui/material'

export default function BudgetInput({ value, onChange }) {
  return (
    <TextField
      label="Budget (₦)"
      type="number"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="50000"
      fullWidth
      inputProps={{ min: 1 }}
    />
  )
}
