import { useEffect, useState, useMemo } from 'react'
import api from '../api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

const SEVERITY_ORDER = ['critical', 'high', 'moderate', 'low']
const RESOURCE_CATEGORIES = [
  { name: 'Food Pkts', weight: 0.2 },
  { name: 'Water', weight: 0.28 },
  { name: 'Med Kits', weight: 0.03 },
  { name: 'Tarpaulin', weight: 0.09 },
  { name: 'Blankets', weight: 0.09 },
  { name: 'Rescue', weight: 0.001 },
]

function severityToPriority(sev) {
  if (sev === 'critical') return 'Critical'
  if (sev === 'high') return 'High'
  if (sev === 'moderate') return 'Medium'
  return 'Low'
}

export default function Dashboard() {
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/api/zones/')
      .then(res => setZones(res.data))
      .catch(err => console.error('Failed to load zones:', err))
      .finally(() => setLoading(false))
  }, [])

  const sortedZones = useMemo(() => {
    return [...zones].sort(
      (a, b) => SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity)
    )
  }, [zones])

  const criticalCount = zones.filter(z => z.severity === 'critical').length
  const totalAffected = zones.reduce((sum, z) => sum + (z.population_estimate || 0), 0)

  const statusCounts = {
    critical: zones.filter(z => z.severity === 'critical').length,
    high: zones.filter(z => z.severity === 'high').length,
    medium: zones.filter(z => z.severity === 'moderate').length,
    recovery: zones.filter(z => z.severity === 'low').length,
  }

  const resourceData = RESOURCE_CATEGORIES.map(cat => ({
    name: cat.name,
    units: Math.round(totalAffected * cat.weight),
  }))

  return (
    <>
      <div className="page-title">
        <h1>Disaster Relief Dashboard</h1>
        <p>AI-optimized resource allocation for emergency response</p>
      </div>

      <div className="stat-grid">
        <div className="stat-card red">
          <div className="stat-label">Active Incidents</div>
          <div className="stat-value">{zones.length}</div>
          <div className="stat-sub">{criticalCount} critical</div>
        </div>
        <div className="stat-card orange">
          <div className="stat-label">Resources Deployed</div>
          <div className="stat-value">{resourceData.reduce((s, r) => s + r.units, 0).toLocaleString('en-IN')}</div>
          <div className="stat-sub">across {zones.length} zones</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Population at Risk</div>
          <div className="stat-value">{totalAffected.toLocaleString('en-IN')}</div>
          <div className="stat-sub">this event</div>
        </div>
        <div className="stat-card purple">
          <div className="stat-label">Zones Monitored</div>
          <div className="stat-value">{zones.length}</div>
          <div className="stat-sub">live tracking</div>
        </div>
      </div>

      <div className="panel-row">
        <div className="panel">
          <div className="panel-header">
            <h2>Resource Allocation by Category (Units Deployed)</h2>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={resourceData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid vertical={false} stroke="#eceef1" />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#6b6e76' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#6b6e76' }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ fill: '#f4f5f7' }} />
              <Bar dataKey="units" fill="#8a2332" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Incident Status</h2>
            <span className="live-badge"><span className="dot" />Live</span>
          </div>
          <div className="status-list">
            <div className="status-row">
              <span className="left"><span className="swatch" style={{ background: 'var(--sev-critical)' }} />Critical (life risk)</span>
              <span className="count">{statusCounts.critical}</span>
            </div>
            <div className="status-row">
              <span className="left"><span className="swatch" style={{ background: 'var(--sev-high)' }} />High (shelter need)</span>
              <span className="count">{statusCounts.high}</span>
            </div>
            <div className="status-row">
              <span className="left"><span className="swatch" style={{ background: 'var(--sev-medium)' }} />Medium (food/water)</span>
              <span className="count">{statusCounts.medium}</span>
            </div>
            <div className="status-row">
              <span className="left"><span className="swatch" style={{ background: 'var(--sev-recovery)' }} />Recovery phase</span>
              <span className="count">{statusCounts.recovery}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="table-panel">
        <h2>Active Incident Summary</h2>
        {loading && <div className="empty-note">Loading incidents…</div>}
        {!loading && zones.length === 0 && (
          <div className="empty-note">No zones registered yet. Add one via <code>POST /api/zones</code>.</div>
        )}
        {!loading && zones.length > 0 && (
          <table className="incident-table">
            <thead>
              <tr>
                <th>Zone</th>
                <th>Event</th>
                <th>Affected</th>
                <th>Vulnerable %</th>
                <th>Priority</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {sortedZones.map(z => (
                <tr key={z.id}>
                  <td>{z.name}</td>
                  <td>{z.disaster_event}</td>
                  <td>{z.population_estimate.toLocaleString('en-IN')}</td>
                  <td>{Math.round(z.vulnerable_population_pct * 100)}%</td>
                  <td>
                    <span className={`priority-chip ${z.severity === 'moderate' ? 'medium' : z.severity}`}>
                      {severityToPriority(z.severity)}
                    </span>
                  </td>
                  <td>
                    <span className={`status-pill ${z.severity === 'critical' ? 'active' : z.severity === 'high' ? 'stabilising' : z.severity === 'moderate' ? 'ongoing' : 'closed'}`}>
                      {z.severity === 'critical' ? 'Active' : z.severity === 'high' ? 'Stabilising' : z.severity === 'moderate' ? 'Ongoing' : 'Recovery'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}
