import { useState, useEffect } from 'react';
import { api } from './api';

function Dashboard({ onLogout }) {
  const [tournaments, setTournaments] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTournaments = async () => {
      try {
       const res = await api.get('/tournaments/');
        setTournaments(res.data);
      } catch (err) {
        setError('Failed to load tournaments.');
      } finally {
        setLoading(false);
      }
    };
    fetchTournaments();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    onLogout();
  };

  return (
    <div style={{ maxWidth: '700px', margin: '60px auto', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>🎮 Tournaments</h2>
        <button onClick={handleLogout} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Logout
        </button>
      </div>

      {loading && <p>Loading tournaments...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && tournaments.length === 0 && (
        <p>No tournaments yet.</p>
      )}

      <div>
        {tournaments.map((t) => (
          <div
            key={t.id}
            style={{
              border: '1px solid #ccc',
              borderRadius: '8px',
              padding: '16px',
              marginBottom: '12px',
            }}
          >
            <h3 style={{ margin: '0 0 8px 0' }}>{t.name}</h3>
            <p style={{ margin: '4px 0' }}>🎯 Game: {t.game_title}</p>
            <p style={{ margin: '4px 0' }}>💰 Entry Fee: ₹{t.entry_fee}</p>
            <p style={{ margin: '4px 0' }}>👥 Slots: {t.slot_limit}</p>
            <p style={{ margin: '4px 0' }}>📌 Status: {t.status}</p>
            <p style={{ margin: '4px 0' }}>🧑‍💼 Organizer: {t.organizer}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;