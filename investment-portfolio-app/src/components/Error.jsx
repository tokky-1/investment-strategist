import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'

export default function ErrorBox({ message }) {
  return (
    <Card className="error-box">
      <CardContent>
        <Typography variant="subtitle1" color="error">
          {message}
        </Typography>
      </CardContent>
    </Card>
  )
}
