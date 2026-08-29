import { useState } from 'react';
import api from './api';

function Login({ onSwitchToRegister, onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/login/', { username, password });
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      setMessage('Login successful! ✅');
      onLoginSuccess();
    } catch (err) {
      setMessage('Login failed. Check username/password.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '80px auto', fontFamily: 'sans-serif' }}>
      <h2>Esports Tournament Manager - Login</h2>
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: '12px' }}>
          <label>Username</label><br />
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '12px' }}>
          <label>Password</label><br />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
            required
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px' }}>Login</button>
      </form>
      {message && <p>{message}</p>}
      <p>
        Don't have an account?{' '}
        <button onClick={onSwitchToRegister} style={{ cursor: 'pointer' }}>
          Register here
        </button>
      </p>
    </div>
  );
}

export default Login;