import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Shield, AlertTriangle, Activity, FileText, Loader, WifiOff, RefreshCw } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000/api';

function Dashboard() {
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const [alRes, incRes] = await Promise.all([
        axios.get(`${API_BASE}/alerts`),
        axios.get(`${API_BASE}/incidents`),
      ]);
      setAlerts(alRes.data);
      setIncidents(incRes.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching data", err);
      setError(err.message || "Failed to connect to backend API");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="status-screen">
        <Loader className="spin" size={48} color="var(--info)" />
        <h2>Loading Dashboard</h2>
        <p className="text-muted">Connecting to SentinelLab API…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="status-screen">
        <WifiOff size={48} color="var(--danger)" />
        <h2>Connection Error</h2>
        <p className="text-muted">{error}</p>
        <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
          Make sure the backend is running at <code>http://127.0.0.1:8000</code>
        </p>
        <button className="btn-retry" onClick={() => { setLoading(true); setError(null); fetchData(); }}>
          <RefreshCw size={16} /> Retry Connection
        </button>
      </div>
    );
  }

  const highCritical = alerts.filter(a => a.severity === 'HIGH' || a.severity === 'CRITICAL').length;
  const activeIncidents = incidents.filter(i => i.status !== 'RESOLVED').length;
  const resolvedIncidents = incidents.filter(i => i.status === 'RESOLVED').length;

  return (
    <div style={{ padding: '2rem' }}>
      <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Activity /> Active Overview
      </h2>
      
      <div className="stats-grid">
        <div className="card stat-card">
          <h3 className="stat-label">Total Alerts</h3>
          <p className="stat-value">{alerts.length}</p>
        </div>
        <div className="card stat-card">
          <h3 className="stat-label">High / Critical</h3>
          <p className="stat-value" style={{ color: highCritical > 0 ? 'var(--danger)' : 'var(--text-main)' }}>
            {highCritical}
          </p>
        </div>
        <div className="card stat-card">
          <h3 className="stat-label">Active Incidents</h3>
          <p className="stat-value" style={{ color: activeIncidents > 0 ? 'var(--warning)' : 'var(--text-main)' }}>
            {activeIncidents}
          </p>
        </div>
        <div className="card stat-card">
          <h3 className="stat-label">Resolved</h3>
          <p className="stat-value" style={{ color: 'var(--accent)' }}>
            {resolvedIncidents}
          </p>
        </div>
      </div>

      <div className="content-grid">
        <div className="card">
          <h3 className="section-title">
            <AlertTriangle size={18}/> Recent Alerts
          </h3>
          {alerts.length === 0 ? (
            <p className="text-muted" style={{ padding: '2rem', textAlign: 'center' }}>No alerts found. Run the seed script to populate sample data.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Time</th>
                  <th>Severity</th>
                  <th>Rule</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {alerts.slice(0, 10).map(a => (
                  <tr key={a.id}>
                    <td><code>{a.alert_id}</code></td>
                    <td>{a.timestamp ? new Date(a.timestamp).toLocaleTimeString() : '—'}</td>
                    <td>
                      <span className={`badge badge-${(a.severity || 'info').toLowerCase()}`}>
                        {a.severity || 'UNKNOWN'}
                      </span>
                    </td>
                    <td>{a.rule_name || '—'}</td>
                    <td style={{ fontFamily: 'monospace' }}>{a.source || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        
        <div className="card">
          <h3 className="section-title">
            <FileText size={18}/> Recent Incidents
          </h3>
          {incidents.length === 0 ? (
            <p className="text-muted" style={{ padding: '2rem', textAlign: 'center' }}>No incidents found.</p>
          ) : (
            <ul style={{ listStyle: 'none' }}>
              {incidents.slice(0, 5).map(inc => (
                <li key={inc.id} className="incident-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ fontWeight: 'bold' }}>{inc.incident_id}</span>
                    <span className={`badge badge-${(inc.severity || 'info').toLowerCase()}`}>
                      {inc.status || 'UNKNOWN'}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>{inc.title || '—'}</div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

function AlertsView() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE}/alerts`)
      .then(res => { setAlerts(res.data); setError(null); })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="status-screen"><Loader className="spin" size={36} color="var(--info)" /><p>Loading alerts…</p></div>;
  if (error) return <div className="status-screen"><WifiOff size={36} color="var(--danger)" /><p>{error}</p></div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <AlertTriangle /> All Alerts
      </h2>
      <div className="card">
        {alerts.length === 0 ? (
          <p className="text-muted" style={{ textAlign: 'center', padding: '2rem' }}>No alerts in the database.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Time</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Rule</th>
                <th>Source</th>
                <th>Evidence</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map(a => (
                <tr key={a.id}>
                  <td><code>{a.alert_id}</code></td>
                  <td>{a.timestamp ? new Date(a.timestamp).toLocaleString() : '—'}</td>
                  <td><span className={`badge badge-${(a.severity || 'info').toLowerCase()}`}>{a.severity}</span></td>
                  <td><span className={`badge badge-${(a.status || '').toLowerCase() === 'escalated' ? 'high' : 'info'}`}>{a.status}</span></td>
                  <td>{a.rule_name}</td>
                  <td style={{ fontFamily: 'monospace' }}>{a.source}</td>
                  <td style={{ maxWidth: '250px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{a.evidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function IncidentsView() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE}/incidents`)
      .then(res => { setIncidents(res.data); setError(null); })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="status-screen"><Loader className="spin" size={36} color="var(--info)" /><p>Loading incidents…</p></div>;
  if (error) return <div className="status-screen"><WifiOff size={36} color="var(--danger)" /><p>{error}</p></div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <FileText /> All Incidents
      </h2>
      {incidents.length === 0 ? (
        <div className="card"><p className="text-muted" style={{ textAlign: 'center', padding: '2rem' }}>No incidents in the database.</p></div>
      ) : (
        <div className="incidents-list">
          {incidents.map(inc => (
            <div key={inc.id} className="card incident-detail-card">
              <div className="incident-header">
                <div>
                  <code style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{inc.incident_id}</code>
                  <h3 style={{ marginTop: '0.25rem' }}>{inc.title}</h3>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
                  <span className={`badge badge-${(inc.severity || 'info').toLowerCase()}`}>{inc.severity}</span>
                  <span className={`badge badge-${inc.status === 'RESOLVED' ? 'low' : 'info'}`}>{inc.status}</span>
                </div>
              </div>
              <p style={{ color: 'var(--text-muted)', margin: '0.75rem 0' }}>{inc.description}</p>
              <div style={{ fontSize: '0.85rem' }}>
                <strong>Asset:</strong> <code>{inc.affected_asset}</code>
              </div>
              {inc.analyst_notes && (
                <div style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                  <strong>Analyst Notes:</strong> {inc.analyst_notes}
                </div>
              )}
              {inc.resolution_notes && (
                <div style={{ fontSize: '0.85rem', marginTop: '0.5rem', color: 'var(--accent)' }}>
                  <strong>Resolution:</strong> {inc.resolution_notes}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Layout({ children }) {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside className="sidebar">
        <div className="sidebar-brand">
          <Shield color="var(--info)" /> SentinelLab
        </div>
        <nav className="sidebar-nav">
          <Link to="/" className={`nav-link ${isActive('/') ? 'nav-active' : ''}`}>
            <Activity size={18}/> Dashboard
          </Link>
          <Link to="/alerts" className={`nav-link ${isActive('/alerts') ? 'nav-active' : ''}`}>
            <AlertTriangle size={18}/> Alerts
          </Link>
          <Link to="/incidents" className={`nav-link ${isActive('/incidents') ? 'nav-active' : ''}`}>
            <FileText size={18}/> Incidents
          </Link>
        </nav>
        <div className="sidebar-footer">
          <div className="pulse-dot"></div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>SOC Monitoring Active</span>
        </div>
      </aside>
      <main style={{ flex: 1 }}>
        <header className="top-header">
          <span style={{ color: 'var(--text-muted)' }}>Security Operations Center Simulator</span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </span>
        </header>
        {children}
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/alerts" element={<AlertsView />} />
          <Route path="/incidents" element={<IncidentsView />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
