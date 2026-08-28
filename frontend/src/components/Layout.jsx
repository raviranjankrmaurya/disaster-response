import { NavLink, Outlet } from 'react-router-dom'

const NAV_ITEMS = [
  { label: 'Dashboard', to: '/' },
  { label: 'Incidents', to: '/incidents' },
  { label: 'Resources', to: '/resources' },
  { label: 'Volunteers', to: '/volunteers' },
  { label: 'Map', to: '/map' },
  { label: 'Settings', to: '/settings' },
]

const SIDEBAR_ITEMS = [
  { label: 'Dashboard', to: '/' },
  { label: 'Active Incidents', to: '/incidents' },
  { label: 'Resources', to: '/resources' },
  { label: 'Volunteers', to: '/volunteers' },
  { label: 'Relief Map', to: '/map' },
  { label: 'Logistics', to: '/logistics' },
  { label: 'Reports', to: '/reports' },
  { label: 'Settings', to: '/settings' },
]

export default function Layout() {
  return (
    <div className="app-shell">
      <nav className="topnav">
        <div className="topnav-brand">
          <div className="mark">RG</div>
          <div>
            <div className="name">RakshaGrid</div>
            <div className="tagline">AI Disaster Relief Coordinator</div>
          </div>
        </div>
        <div className="topnav-links">
          {NAV_ITEMS.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) => (isActive ? 'active' : '')}
            >
              {item.label}
            </NavLink>
          ))}
        </div>
        <div className="topnav-user">
          <div>
            <div style={{ fontSize: 12.5, fontWeight: 600 }}>AP</div>
            <div className="role">Admin</div>
          </div>
          <div className="avatar">AP</div>
        </div>
      </nav>

      <div className="app-body">
        <aside className="sidebar">
          {SIDEBAR_ITEMS.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}
            >
              {item.label}
            </NavLink>
          ))}
        </aside>

        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
