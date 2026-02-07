import React from 'react'

export default function Notification({ message, error }) {
  if (!message) return null
  return (
    <div style={{
      padding: 14,
      marginBottom: 12,
      background: error ? 'rgba(255,230,230,0.95)' : 'rgba(240,248,255,0.95)',
      border: error ? '1px solid #f5c2c2' : '1px solid rgba(30,144,255,0.14)',
      borderRadius: 8
    }}>
      <div style={{ color: error ? '#7f1d1d' : '#084298' }}>{message}</div>
    </div>
  )
}
