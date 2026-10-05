import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Shield, AlertTriangle, Activity, FileText } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000/api';

function Dashboard() {
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const alRes = await axios.get(`${API_BASE}/alerts`);
        const incRes = await axios.get(`${API_BASE}/incidents`);
        setAlerts(alRes.data);
        setIncidents(incRes.data);
      } catch (err) {
        console.error("Error fetching data", err);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Activity /> Active Overview
      </h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Total Alerts</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{alerts.length}</p>
        </div>
        <div className="card">
          <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>High/Critical</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--danger)' }}>
            {alerts.filter(a => a.severity === 'HIGH' || a.severity === 'CRITICAL').length}
          </p>
        </div>
        <div className="card">
          <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Active Incidents</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--warning)' }}>
            {incidents.filter(i => i.status !== 'RESOLVED').length}
          </p>
        </div>
        <div className="card">
          <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Resolved Incidents</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--info)' }}>
            {incidents.filter(i => i.status === 'RESOLVED').length}
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={18}/> Recent Alerts
          </h3>
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
                  <td>{a.alert_id}</td>
                  <td>{new Date(a.timestamp).toLocaleTimeString()}</td>
                  <td><span className={`badge badge-${a.severity.toLowerCase()}`}>{a.severity}</span></td>
                  <td>{a.rule_name}</td>
                  <td style={{ fontFamily: 'monospace' }}>{a.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="card">
          <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FileText size={18}/> Recent Incidents
          </h3>
          <ul style={{ listStyle: 'none' }}>
            {incidents.slice(0, 5).map(inc => (
              <li key={inc.id} style={{ marginBottom: '1rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                  <span style={{ fontWeight: 'bold' }}>{inc.incident_id}</span>
                  <span className={`badge badge-${inc.severity.toLowerCase()}`}>{inc.status}</span>
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>{inc.title}</div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

function Layout({ children }) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside style={{ width: '240px', background: 'var(--card-bg)', borderRight: '1px solid var(--border)', padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '2rem', color: 'white' }}>
          <Shield color="var(--info)" /> SentinelLab
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <Link to="/" style={{ padding: '0.5rem', borderRadius: '4px', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={18}/> Dashboard
          </Link>
          <Link to="/alerts" style={{ padding: '0.5rem', borderRadius: '4px', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={18}/> Alerts
          </Link>
          <Link to="/incidents" style={{ padding: '0.5rem', borderRadius: '4px', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FileText size={18}/> Incidents
          </Link>
        </nav>
      </aside>
      <main style={{ flex: 1 }}>
        <header style={{ height: '60px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', padding: '0 2rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>Security Operations Center Simulator</span>
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
          <Route path="/alerts" element={<div style={{padding:'2rem'}}><h2>Alerts View (Stub)</h2></div>} />
          <Route path="/incidents" element={<div style={{padding:'2rem'}}><h2>Incidents View (Stub)</h2></div>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
