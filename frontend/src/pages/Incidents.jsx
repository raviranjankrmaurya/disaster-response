import { useEffect, useState } from 'react'
import api from '../api'

const SEVERITY_ORDER = ['critical', 'high', 'moderate', 'low']

export default function Incidents() {
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    api.get('/api/zones/')
      .then(res => setZones(res.data))
      .catch(err => console.error('Failed to load zones:', err))
      .finally(() => setLoading(false))
  }, [])

  const filtered = zones
    .filter(z => filter === 'all' || z.severity === filter)
    .sort((a, b) => SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity))

  return (
    <>
      <div className="page-title">
        <h1>Active Incidents</h1>
        <p>Every registered disaster zone, filterable by severity</p>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16, flexWrap: 'wrap' }}>
        {['all', 'critical', 'high', 'moderate', 'low'].map(s => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            style={{
              padding: '6px 14px', borderRadius: 999, border: '1px solid var(--border)',
              background: filter === s ? 'var(--brand)' : 'var(--surface)',
              color: filter === s ? '#fff' : 'var(--text-secondary)',
              fontSize: 12.5, fontWeight: 600, textTransform: 'capitalize', cursor: 'pointer',
            }}
          >
            {s}
          </button>
        ))}
      </div>

      <div className="table-panel">
        <h2>Incident Register ({filtered.length})</h2>
        {loading && <div className="empty-note">Loading incidents…</div>}
        {!loading && filtered.length === 0 && (
          <div className="empty-note">No incidents match this filter.</div>
        )}
        {!loading && filtered.length > 0 && (
          <table className="incident-table">
            <thead>
              <tr>
                <th>Zone</th>
                <th>Event</th>
                <th>Population</th>
                <th>Vulnerable %</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(z => (
                <tr key={z.id}>
                  <td>{z.name}</td>
                  <td>{z.disaster_event}</td>
                  <td>{z.population_estimate.toLocaleString('en-IN')}</td>
                  <td>{Math.round(z.vulnerable_population_pct * 100)}%</td>
                  <td>
                    <span className={`priority-chip ${z.severity === 'moderate' ? 'medium' : z.severity}`}>
                      {z.severity}
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
