import React from 'react'
import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material'

export default function RiskSelector({ value, onChange }) {
  return (
    <FormControl>
      <FormLabel>Risk</FormLabel>
      <RadioGroup row value={value} onChange={(e) => onChange(e.target.value)}>
        <FormControlLabel value="low" control={<Radio />} label="Low (Stable)" />
        <FormControlLabel value="medium" control={<Radio />} label="Medium (Balanced)" />
        <FormControlLabel value="high" control={<Radio />} label="High (Aggressive)" />
      </RadioGroup>
    </FormControl>
  )
}
