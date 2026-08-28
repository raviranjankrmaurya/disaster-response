import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Incidents from './pages/Incidents'
import Resources from './pages/Resources'
import Volunteers from './pages/Volunteers'
import ReliefMap from './pages/ReliefMap'
import Logistics from './pages/Logistics'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/incidents" element={<Incidents />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/volunteers" element={<Volunteers />} />
          <Route path="/map" element={<ReliefMap />} />
          <Route path="/logistics" element={<Logistics />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
