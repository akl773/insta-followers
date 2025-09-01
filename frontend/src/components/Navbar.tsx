import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Dashboard,
  Assessment,
  People,
  Analytics,
  LightMode,
  DarkMode,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useThemeMode } from '../context/ThemeContext';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const { mode, toggleColorMode } = useThemeMode();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <Dashboard /> },
    { path: '/reports', label: 'Reports', icon: <Assessment /> },
    { path: '/not-following-back', label: 'Not Following Back', icon: <People /> },
    { path: '/analytics', label: 'Analytics', icon: <Analytics /> },
  ];

  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.secondary.main, 0.1)} 100%)`,
        backdropFilter: 'blur(20px)',
        borderBottom: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
      }}
    >
      <Toolbar sx={{ px: { xs: 2, md: 4 } }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: 2,
              background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 'bold',
              fontSize: '1.2rem',
            }}
          >
            IG
          </Box>
          <Typography
            variant="h6"
            component="div"
            sx={{
              fontWeight: 700,
              background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Instagram Analytics
          </Typography>
        </Box>

        <Box sx={{ flexGrow: 1 }} />

        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              sx={{
                color: theme.palette.text.primary,
                backgroundColor: location.pathname === item.path
                  ? alpha(theme.palette.primary.main, 0.1)
                  : 'transparent',
                border: location.pathname === item.path
                  ? `1px solid ${alpha(theme.palette.primary.main, 0.3)}`
                  : '1px solid transparent',
                borderRadius: 2,
                px: 2,
                py: 1,
                fontWeight: 500,
                '&:hover': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.08),
                  border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                },
                transition: 'all 0.2s ease-in-out',
              }}
            >
              {item.label}
            </Button>
          ))}

          <IconButton
            onClick={toggleColorMode}
            sx={{
              ml: 2,
              p: 1.5,
              border: `1px solid ${alpha(theme.palette.divider, 0.3)}`,
              borderRadius: 2,
              '&:hover': {
                backgroundColor: alpha(theme.palette.primary.main, 0.08),
                border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,
              },
              transition: 'all 0.2s ease-in-out',
            }}
          >
            {mode === 'dark' ? <LightMode /> : <DarkMode />}
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
