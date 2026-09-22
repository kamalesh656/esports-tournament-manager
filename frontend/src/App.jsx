import { useState, useEffect } from 'react';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';
import AdminDashboard from './AdminDashboard';
import { authApi } from './api';

function App() {
  const [showRegister, setShowRegister] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchUserRole();
    } else {
      setCheckingAuth(false);
    }
  }, []);

  const fetchUserRole = async () => {
    try {
      const res = await authApi.get('/me/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
      });
      setUserRole(res.data.role);
      setIsLoggedIn(true);
    } catch (err) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } finally {
      setCheckingAuth(false);
    }
  };

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    fetchUserRole();
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserRole(null);
  };

  if (checkingAuth) {
    return <p style={{ textAlign: 'center', marginTop: '80px' }}>Loading...</p>;
  }

  if (isLoggedIn) {
    if (userRole === 'admin') {
      return <AdminDashboard onLogout={handleLogout} />;
    }
    return <Dashboard onLogout={handleLogout} />;
  }

  return (
    <div>
      {showRegister ? (
        <Register onSwitchToLogin={() => setShowRegister(false)} />
      ) : (
        <Login
          onSwitchToRegister={() => setShowRegister(true)}
          onLoginSuccess={handleLoginSuccess}
        />
      )}
    </div>
  );
}

export default App;