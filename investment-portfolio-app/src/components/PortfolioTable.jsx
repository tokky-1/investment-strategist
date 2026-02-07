import React from 'react'
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material'

const HEADERS = ['Asset Symbol', 'Asset Type', 'Allocation %', 'Price (USD)', 'Amount (₦)', 'Estimated Shares']

export default function PortfolioTable({ rows = [] }) {
  return (
    <TableContainer component={Paper} sx={{ mb: 2 }}>
      <Table>
        <TableHead>
          <TableRow>{HEADERS.map((h) => <TableCell key={h}>{h}</TableCell>)}</TableRow>
        </TableHead>
        <TableBody>
          {rows.map(({ symbol, type, allocationPercent, priceUSD, amountNGN, estimatedShares }) => (
            <TableRow key={symbol}>
              <TableCell><Typography variant="subtitle2">{symbol}</Typography></TableCell>
              <TableCell>{type}</TableCell>
              <TableCell>{allocationPercent}%</TableCell>
              <TableCell>${priceUSD}</TableCell>
              <TableCell>₦{amountNGN.toLocaleString()}</TableCell>
              <TableCell>{estimatedShares}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}
