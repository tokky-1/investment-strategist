import React from 'react'
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
import { Card, CardContent, Typography } from '@mui/material'

const COLORS = ['#4caf50', '#2196f3', '#ff9800', '#9c27b0', '#f44336', '#607d8b']

export default function AllocationChart({ data = [] }) {
  const pieData = data.map(({ symbol, allocationPercent }) => ({ name: symbol, value: allocationPercent }))

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="subtitle1" gutterBottom>Allocation</Typography>
        <PieChart width={260} height={220}>
          <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} label>
            {pieData.map((entry, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </CardContent>
    </Card>
  )
}

