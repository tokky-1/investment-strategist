import React, { useEffect, useState } from 'react'
import { IconButton, Tooltip } from '@mui/material'

export default function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('theme') || 'light'
    } catch {
      return 'light'
    }
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    try {
      localStorage.setItem('theme', theme)
    } catch {}
  }, [theme])

  const toggle = () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))

  return (
    <Tooltip title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}>
      <IconButton onClick={toggle} className="theme-toggle" aria-label="toggle theme">
        {theme === 'dark' ? '🌞' : '🌙'}
      </IconButton>
    </Tooltip>
  )
}
