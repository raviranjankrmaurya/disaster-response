import { useEffect, useState } from 'react'
import api from '../api'

export default function Resources() {
  const [zones, setZones] = useState([])

  useEffect(() => {
    api.get('?path=zones/')
      .then(res => setZones(res.data))
      .catch(err => console.error('Failed to load zones:', err))
  }, [])

  const totalPop = zones.reduce((s, z) => s + (z.population_estimate || 0), 0)

  const categories = [
    { name: 'Food Packets', unit: 'packets', weight: 0.6 },
    { name: 'Drinking Water', unit: 'litres', weight: 3.0 },
    { name: 'Medical Kits', unit: 'kits', weight: 0.02 },
    { name: 'Tarpaulin Sheets', unit: 'sheets', weight: 0.09 },
    { name: 'Blankets', unit: 'units', weight: 0.15 },
    { name: 'Rescue Boats', unit: 'boats', weight: 0.0005 },
  ]

  return (
    <>
      <div className="page-title">
        <h1>Resources</h1>
        <p>Estimated requirement by category, based on population across active zones</p>
      </div>

      <div className="table-panel">
        <h2>Resource Requirement Estimate</h2>
        <table className="incident-table">
          <thead>
            <tr><th>Category</th><th>Estimated Need</th><th>Unit</th></tr>
          </thead>
          <tbody>
            {categories.map(cat => (
              <tr key={cat.name}>
                <td>{cat.name}</td>
                <td>{Math.round(totalPop * cat.weight).toLocaleString('en-IN')}</td>
                <td>{cat.unit}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="empty-note" style={{ marginTop: 16 }}>
        Depot inventory tracking is available via <code>POST /api/depots</code> and{' '}
        <code>POST /api/depots/stock</code>.
      </div>
    </>
  )
}
