import { useState } from 'react'
import api from '../api'

const RESOURCE_TYPES = [
  { value: 'food', label: 'Food Packets' },
  { value: 'water', label: 'Water' },
  { value: 'medical_kit', label: 'Medical Kits' },
  { value: 'shelter_kit', label: 'Shelter Kits' },
]

export default function Logistics() {
  const [resourceType, setResourceType] = useState('food')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const runAllocation = () => {
    setLoading(true)
    setError(null)
    api.post('?path=logistics/allocate', { resource_type: resourceType })
      .then(res => setResult(res.data))
      .catch(err => {
        console.error(err)
        setError('Could not run allocation — check that depots have stock for this resource type.')
      })
      .finally(() => setLoading(false))
  }

  const coveragePct = result && result.total_demand > 0
    ? Math.round((result.total_allocated / result.total_demand) * 100)
    : null

  return (
    <>
      <div className="page-title">
        <h1>Logistics</h1>
        <p>AI-optimized allocation of depot stock to demand zones, with real road-route distance (OR-Tools + OSRM)</p>
      </div>

      <div className="panel" style={{ marginBottom: 16 }}>
        <div className="panel-header"><h2>Run Allocation</h2></div>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
          <select
            value={resourceType}
            onChange={e => setResourceType(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: 8, border: '1px solid var(--border)', fontSize: 13.5, color: 'var(--text-primary)', background: '#fff' }}
          >
            {RESOURCE_TYPES.map(rt => (
              <option key={rt.value} value={rt.value}>{rt.label}</option>
            ))}
          </select>
          <button
            onClick={runAllocation}
            disabled={loading}
            style={{ padding: '8px 18px', borderRadius: 8, border: 'none', background: 'var(--brand)', color: '#fff', fontSize: 13.5, fontWeight: 600, cursor: loading ? 'default' : 'pointer', opacity: loading ? 0.6 : 1 }}
          >
            {loading ? 'Allocating… (routing can take a few seconds)' : 'Allocate'}
          </button>
        </div>
        {error && <div style={{ marginTop: 12, color: 'var(--sev-critical)', fontSize: 13 }}>{error}</div>}
      </div>

      {result && (
        <>
          <div className="stat-grid">
            <div className="stat-card red">
              <div className="stat-label">Total Demand</div>
              <div className="stat-value">{result.total_demand.toLocaleString('en-IN')}</div>
              <div className="stat-sub">units requested</div>
            </div>
            <div className="stat-card green">
              <div className="stat-label">Total Allocated</div>
              <div className="stat-value">{result.total_allocated.toLocaleString('en-IN')}</div>
              <div className="stat-sub">{coveragePct}% coverage</div>
            </div>
            <div className="stat-card orange">
              <div className="stat-label">Unmet Demand</div>
              <div className="stat-value">{result.unmet_demand.toLocaleString('en-IN')}</div>
              <div className="stat-sub">units short</div>
            </div>
          </div>

          <div className="table-panel">
            <h2>Allocation Plan &amp; Delivery Routes</h2>
            {result.allocations.length === 0 ? (
              <div className="empty-note">
                No allocation possible — add depot stock for this resource type via <code>POST /api/depots/stock</code>.
              </div>
            ) : (
              <table className="incident-table">
                <thead>
                  <tr><th>Depot</th><th>→ Zone</th><th>Quantity</th><th>Distance</th><th>Est. Drive Time</th></tr>
                </thead>
                <tbody>
                  {result.allocations.map((a, i) => (
                    <tr key={i}>
                      <td>{a.depot_name}</td>
                      <td>{a.zone_name}</td>
                      <td>{a.quantity_allocated.toLocaleString('en-IN')}</td>
                      <td>
                        {a.distance_km != null ? `${a.distance_km} km` : '—'}
                        {a.route_source === 'straight_line_fallback' && (
                          <span style={{ color: 'var(--text-muted)', fontSize: 11 }}> (est.)</span>
                        )}
                      </td>
                      <td>{a.duration_min != null ? `${a.duration_min} min` : '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {result.allocations.some(a => a.route_source === 'straight_line_fallback') && (
              <div className="empty-note" style={{ borderTop: '1px solid var(--border)' }}>
                Some routes show straight-line estimates — the live road-routing service (OSRM) was unreachable for those pairs.
              </div>
            )}
          </div>
        </>
      )}
    </>
  )
}
