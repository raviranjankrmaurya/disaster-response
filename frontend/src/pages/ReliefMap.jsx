import { useEffect, useState, Fragment } from 'react'
import { MapContainer, TileLayer, Polygon, Marker, Popup, GeoJSON, useMap } from 'react-leaflet'
import api from '../api'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import indiaOutline from '../data/india_outline.json'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

const SEVERITY_COLOR = {
  critical: '#d9455f',
  high: '#e8823a',
  moderate: '#d4a72c',
  low: '#34a468',
}

const INDIA_BOUNDS = [
  [6.5, 67.5],
  [37.5, 97.5],
]

const INDIA_OUTLINE_STYLE = {
  color: '#8a2332',
  weight: 2,
  fill: false,
}

function FitIndiaOnLoad() {
  const map = useMap()
  useEffect(() => {
    const id = setTimeout(() => {
      map.invalidateSize()
      map.fitBounds(INDIA_BOUNDS, { padding: [20, 20] })
    }, 100)
    return () => clearTimeout(id)
  }, [map])
  return null
}

export default function ReliefMap() {
  const [zones, setZones] = useState([])

  useEffect(() => {
    api.get('?path=zones/')
      .then(res => setZones(res.data))
      .catch(err => console.error('Failed to load zones:', err))
  }, [])

  return (
    <>
      <div className="page-title">
        <h1>Relief Map</h1>
        <p>{zones.length} zone{zones.length === 1 ? '' : 's'} currently tracked</p>
      </div>

      <div style={{ height: 520, borderRadius: 10, overflow: 'hidden', border: '1px solid var(--border)' }}>
        <MapContainer
          center={[22.5, 80]}
          zoom={5}
          minZoom={3}
          maxBounds={[[0, 55], [42, 110]]}
          maxBoundsViscosity={0.8}
          style={{ height: '100%', width: '100%' }}
        >
          <FitIndiaOnLoad />
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <GeoJSON data={indiaOutline} style={INDIA_OUTLINE_STYLE} />
          {zones.map(z => {
            const color = SEVERITY_COLOR[z.severity] || '#8a2332'
            const positions = (z.polygon || []).map(([lon, lat]) => [lat, lon])
            return (
              <Fragment key={z.id}>
                {positions.length > 0 && (
                  <Polygon
                    positions={positions}
                    pathOptions={{ color, fillColor: color, fillOpacity: 0.25, weight: 2 }}
                  />
                )}
                {z.centroid_lat && z.centroid_lon && (
                  <Marker position={[z.centroid_lat, z.centroid_lon]}>
                    <Popup>
                      <strong>{z.name}</strong><br />
                      {z.disaster_event}<br />
                      Severity: {z.severity}<br />
                      Population: {z.population_estimate.toLocaleString('en-IN')}
                    </Popup>
                  </Marker>
                )}
              </Fragment>
            )
          })}
        </MapContainer>
      </div>
    </>
  )
}
