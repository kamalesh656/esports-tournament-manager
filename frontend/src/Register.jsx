import { useState } from 'react';
import api from './api';

function Register({ onSwitchToLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'captain',
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await api.post('/register/', formData);
      setMessage('Registration successful! You can now login. ✅');
    } catch (err) {
      setMessage('Registration failed. Try a different username.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '80px auto', fontFamily: 'sans-serif' }}>
      <h2>Create Account</h2>
      <form onSubmit={handleRegister}>
        <div style={{ marginBottom: '12px' }}>
          <label>Username</label><br />
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '12px' }}>
          <label>Email</label><br />
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '12px' }}>
          <label>Password</label><br />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '12px' }}>
          <label>Role</label><br />
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px' }}
          >
            <option value="captain">Team Captain</option>
            <option value="player">Team Member</option>
            <option value="admin">Organizer/Admin</option>
          </select>
        </div>
        <button type="submit" style={{ padding: '10px 20px' }}>Register</button>
      </form>
      {message && <p>{message}</p>}
      <p>
        Already have an account?{' '}
        <button onClick={onSwitchToLogin} style={{ cursor: 'pointer' }}>
          Login here
        </button>
      </p>
    </div>
  );
}

export default Register;