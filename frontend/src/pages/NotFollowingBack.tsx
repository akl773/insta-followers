import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar,
  Button,
  CircularProgress,
  Alert,
  Chip,
  Grid,
  useTheme,
  alpha,
  Paper,
  Fade,
} from '@mui/material';
import { Instagram, OpenInNew, PersonRemove, Refresh } from '@mui/icons-material';
import { apiService, NotFollowingBackUser } from '../services/api';
import UserProfile from '../components/UserProfile';

const NotFollowingBack: React.FC = () => {
  const theme = useTheme();
  const [users, setUsers] = useState<NotFollowingBackUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [userProfileOpen, setUserProfileOpen] = useState(false);

  useEffect(() => {
    fetchNotFollowingBack();
  }, []);

  const fetchNotFollowingBack = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getNotFollowingBack();
      if (response.data.success) {
        setUsers(response.data.data);
      }
    } catch (err) {
      setError('Failed to fetch users not following back');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openInstagramProfile = (url: string) => {
    window.open(url, '_blank');
  };

  const handleUserClick = (username: string) => {
    setSelectedUser(username);
    setUserProfileOpen(true);
  };

  const handleCloseUserProfile = () => {
    setUserProfileOpen(false);
    setSelectedUser(null);
  };

  if (loading) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
        gap={2}
      >
        <CircularProgress size={60} thickness={4} />
        <Typography variant="h6" color="text.secondary">
          Loading users not following back...
        </Typography>
      </Box>
    );
  }

  return (
    <Fade in timeout={500}>
      <Box>
        {/* Header Section */}
        <Paper
          sx={{
            p: 4,
            mb: 4,
            background: `linear-gradient(135deg, ${alpha(theme.palette.warning.main, 0.05)}, ${alpha(theme.palette.error.main, 0.05)})`,
            border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
            borderRadius: 3,
          }}
        >
          <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
            <Box>
              <Typography
                variant="h3"
                component="h1"
                sx={{
                  fontWeight: 800,
                  mb: 1,
                  background: `linear-gradient(135deg, ${theme.palette.warning.main}, ${theme.palette.error.main})`,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Not Following Back
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ fontWeight: 500 }}>
                Users you follow who don't follow you back
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <Chip
                icon={<PersonRemove />}
                label={`${users.length} users`}
                sx={{
                  backgroundColor: alpha(theme.palette.warning.main, 0.1),
                  color: theme.palette.warning.main,
                  fontWeight: 600,
                  fontSize: '0.875rem',
                }}
              />
              <Button
                variant="contained"
                size="large"
                startIcon={<Refresh />}
                onClick={fetchNotFollowingBack}
                disabled={loading}
                sx={{
                  px: 3,
                  py: 1.5,
                  borderRadius: 2,
                  fontWeight: 600,
                  background: `linear-gradient(135deg, ${theme.palette.warning.main}, ${theme.palette.error.main})`,
                  '&:hover': {
                    background: `linear-gradient(135deg, ${theme.palette.warning.dark}, ${theme.palette.error.dark})`,
                    transform: 'translateY(-2px)',
                    boxShadow: theme.shadows[8],
                  },
                  transition: 'all 0.2s ease-in-out',
                }}
              >
                Refresh
              </Button>
            </Box>
          </Box>
        </Paper>

        {error && (
          <Alert
            severity="error"
            sx={{
              mb: 4,
              borderRadius: 2,
              '& .MuiAlert-icon': {
                fontSize: '1.5rem',
              },
            }}
          >
            {error}
          </Alert>
        )}

        {users.length === 0 ? (
          <Card sx={{ borderRadius: 3 }}>
            <CardContent sx={{ p: 6, textAlign: 'center' }}>
              <Box
                sx={{
                  width: 80,
                  height: 80,
                  borderRadius: '50%',
                  background: `linear-gradient(135deg, ${alpha(theme.palette.success.main, 0.1)}, ${alpha(theme.palette.success.main, 0.05)})`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 3,
                }}
              >
                <Instagram sx={{ fontSize: 40, color: theme.palette.success.main }} />
              </Box>
              <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                Great news! 🎉
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 1 }}>
                No users found who are not following back!
              </Typography>
              <Typography variant="body2" color="text.secondary">
                This means everyone you follow follows you back, or no reports have been generated yet.
              </Typography>
            </CardContent>
          </Card>
        ) : (
          <Card sx={{ borderRadius: 3 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography
                variant="h5"
                component="h2"
                sx={{
                  mb: 3,
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1,
                }}
              >
                <PersonRemove color="warning" />
                Users Not Following Back ({users.length})
              </Typography>

              <Grid container spacing={2}>
                {users.map((user) => (
                  <Grid item xs={12} sm={6} md={4} lg={3} key={user.username}>
                    <Card
                      sx={{
                        borderRadius: 2,
                        border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
                        '&:hover': {
                          transform: 'translateY(-4px)',
                          boxShadow: theme.shadows[8],
                          borderColor: alpha(theme.palette.warning.main, 0.3),
                        },
                        transition: 'all 0.2s ease-in-out',
                        cursor: 'pointer',
                      }}
                      onClick={() => handleUserClick(user.username)}
                    >
                      <CardContent sx={{ p: 3, textAlign: 'center' }}>
                        <Avatar
                          src={user.profile_pic_url}
                          sx={{
                            width: 64,
                            height: 64,
                            mx: 'auto',
                            mb: 2,
                            border: `3px solid ${alpha(theme.palette.warning.main, 0.2)}`,
                          }}
                        >
                          {user.username[0].toUpperCase()}
                        </Avatar>
                        <Typography
                          variant="subtitle1"
                          sx={{
                            fontWeight: 600,
                            mb: 0.5,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          @{user.username}
                        </Typography>
                        {user.full_name && (
                          <Typography
                            variant="body2"
                            color="text.secondary"
                            sx={{
                              mb: 2,
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                            }}
                          >
                            {user.full_name}
                          </Typography>
                        )}
                        <Button
                          variant="outlined"
                          size="small"
                          startIcon={<OpenInNew />}
                          onClick={(e) => {
                            e.stopPropagation();
                            openInstagramProfile(user.instagram_url);
                          }}
                          sx={{
                            borderColor: alpha(theme.palette.warning.main, 0.3),
                            color: theme.palette.warning.main,
                            '&:hover': {
                              borderColor: theme.palette.warning.main,
                              backgroundColor: alpha(theme.palette.warning.main, 0.1),
                            },
                          }}
                        >
                          View Profile
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        )}

        {/* User Profile Dialog */}
        {selectedUser && (
          <UserProfile
            open={userProfileOpen}
            onClose={handleCloseUserProfile}
            username={selectedUser}
          />
        )}
      </Box>
    </Fade>
  );
};

export default NotFollowingBack;
