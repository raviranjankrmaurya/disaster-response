import { useEffect, useState } from 'react'
import api from '../api'

export default function Volunteers() {
  const [volunteers, setVolunteers] = useState([])
  const [name, setName] = useState('')
  const [skill, setSkill] = useState('medical')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const load = () => {
    api.get('/api/volunteers/')
      .then(res => setVolunteers(res.data))
      .catch(err => console.error('Failed to load volunteers:', err))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const addVolunteer = () => {
    if (!name.trim()) return
    setError(null)
    api.post('/api/volunteers/', { name, skill })
      .then(() => { setName(''); load() })
      .catch(err => {
        console.error(err)
        setError('Could not add volunteer — write endpoints need the X-API-Key header.')
      })
  }

  return (
    <>
      <div className="page-title">
        <h1>Volunteers</h1>
        <p>Field team roster and deployment status</p>
      </div>

      <div className="panel" style={{ marginBottom: 16 }}>
        <div className="panel-header"><h2>Add Volunteer</h2></div>
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <input
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="Full name"
            style={{ flex: 1, padding: '8px 12px', borderRadius: 8, border: '1px solid var(--border)', fontSize: 13.5 }}
          />
          <select
            value={skill}
            onChange={e => setSkill(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: 8, border: '1px solid var(--border)', fontSize: 13.5 }}
          >
            <option value="medical">Medical</option>
            <option value="search_rescue">Search & Rescue</option>
            <option value="logistics">Logistics</option>
            <option value="general">General</option>
          </select>
          <button
            onClick={addVolunteer}
            style={{ padding: '8px 18px', borderRadius: 8, border: 'none', background: 'var(--brand)', color: '#fff', fontSize: 13.5, fontWeight: 600, cursor: 'pointer' }}
          >
            Add
          </button>
        </div>
        {error && <div style={{ marginTop: 12, color: 'var(--sev-critical)', fontSize: 13 }}>{error}</div>}
      </div>

      <div className="table-panel">
        <h2>Volunteer Roster ({volunteers.length})</h2>
        {loading && <div className="empty-note">Loading volunteers…</div>}
        {!loading && volunteers.length === 0 && (
          <div className="empty-note">No volunteers registered yet.</div>
        )}
        {!loading && volunteers.length > 0 && (
          <table className="incident-table">
            <thead>
              <tr><th>Name</th><th>Skill</th><th>Phone</th><th>Status</th></tr>
            </thead>
            <tbody>
              {volunteers.map(v => (
                <tr key={v.id}>
                  <td>{v.name}</td>
                  <td style={{ textTransform: 'capitalize' }}>{v.skill.replace('_', ' ')}</td>
                  <td>{v.phone || '—'}</td>
                  <td>
                    <span className={`status-pill ${v.status === 'deployed' ? 'stabilising' : v.status === 'available' ? 'closed' : 'ongoing'}`}>
                      {v.status.replace('_', ' ')}
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
