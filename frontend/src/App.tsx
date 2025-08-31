import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/material';

import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import NotFollowingBack from './pages/NotFollowingBack';
import Analytics from './pages/Analytics';
import UserProfile from './components/UserProfile';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [profileOpen, setProfileOpen] = useState(false);
  const [selectedUsername, setSelectedUsername] = useState('');

  const handleOpenProfile = (username: string) => {
    setSelectedUsername(username);
    setProfileOpen(true);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar />
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/not-following-back" element={<NotFollowingBack />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
            <UserProfile
              open={profileOpen}
              onClose={() => setProfileOpen(false)}
              username={selectedUsername}
            />
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
