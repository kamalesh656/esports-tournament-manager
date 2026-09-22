import { useState, useEffect } from 'react';
import { api } from './api';

function AdminDashboard({ onLogout }) {
  const [tournaments, setTournaments] = useState([]);
  const [selectedTournament, setSelectedTournament] = useState(null);
  const [registrations, setRegistrations] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMyTournaments();
  }, []);

  const fetchMyTournaments = async () => {
    try {
      const res = await api.get('/my-tournaments/');
      setTournaments(res.data);
    } catch (err) {
      setMessage('Failed to load tournaments.');
    } finally {
      setLoading(false);
    }
  };

  const viewRegistrations = async (tournament) => {
    setSelectedTournament(tournament);
    try {
      const res = await api.get(`/tournaments/${tournament.id}/registrations/`);
      setRegistrations(res.data);
    } catch (err) {
      setMessage('Failed to load registrations.');
    }
  };

  const updateStatus = async (regId, newStatus) => {
    try {
      await api.patch(`/registrations/${regId}/update/`, { status: newStatus });
      setMessage(`Registration ${newStatus}! ✅`);
      viewRegistrations(selectedTournament);
    } catch (err) {
      setMessage('Failed to update registration.');
    }
  };

  const generateBracket = async (tournamentId) => {
    try {
      const res = await api.post(`/tournaments/${tournamentId}/generate-bracket/`);
      setMessage(res.data.message + ' 🏆');
    } catch (err) {
      setMessage(err.response?.data?.error || 'Failed to generate bracket.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    onLogout();
  };

  return (
    <div style={{ maxWidth: '800px', margin: '60px auto', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>🛠️ Organizer Dashboard</h2>
        <button onClick={handleLogout} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Logout
        </button>
      </div>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {loading && <p>Loading...</p>}

      <h3>My Tournaments</h3>
      {tournaments.length === 0 && !loading && <p>You haven't organized any tournaments yet.</p>}
      {tournaments.map((t) => (
        <div key={t.id} style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '12px', marginBottom: '10px' }}>
          <strong>{t.name}</strong> ({t.status})
          <div style={{ marginTop: '8px' }}>
            <button onClick={() => viewRegistrations(t)} style={{ marginRight: '8px', cursor: 'pointer' }}>
              View Registrations
            </button>
            <button onClick={() => generateBracket(t.id)} style={{ cursor: 'pointer' }}>
              Generate Bracket
            </button>
          </div>
        </div>
      ))}

      {selectedTournament && (
        <div style={{ marginTop: '24px' }}>
          <h3>Registrations for "{selectedTournament.name}"</h3>
          {registrations.length === 0 && <p>No registrations yet.</p>}
          {registrations.map((r) => (
            <div key={r.id} style={{ border: '1px solid #eee', padding: '10px', marginBottom: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>{r.team_name} — <em>{r.status}</em></span>
              <div>
                <button onClick={() => updateStatus(r.id, 'approved')} style={{ marginRight: '6px', cursor: 'pointer' }}>
                  Approve
                </button>
                <button onClick={() => updateStatus(r.id, 'rejected')} style={{ cursor: 'pointer' }}>
                  Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;