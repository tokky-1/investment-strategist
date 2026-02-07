import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import { motion } from 'framer-motion'

export default function LoadingBox({ message }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <Card className="loading-box">
        <CardContent>
          <Typography variant="subtitle1">{message}</Typography>
        </CardContent>
      </Card>
    </motion.div>
  )
}
