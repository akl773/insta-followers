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
} from '@mui/material';
import { Instagram, OpenInNew } from '@mui/icons-material';
import { apiService, NotFollowingBackUser } from '../services/api';
import UserProfile from '../components/UserProfile';

const NotFollowingBack: React.FC = () => {
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
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Not Following Back
        </Typography>
        <Chip
          icon={<Instagram />}
          label={`${users.length} users`}
          color="secondary"
        />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {users.length === 0 ? (
        <Card>
          <CardContent>
            <Typography variant="h6" align="center" color="textSecondary">
              No users found who are not following back!
            </Typography>
            <Typography variant="body2" align="center" color="textSecondary">
              This could mean everyone you follow follows you back, or no reports have been generated yet.
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={2}>
          {users.map((user) => (
            <Grid item xs={12} sm={6} md={4} key={user.username}>
              <Card 
                sx={{ cursor: 'pointer' }}
                onClick={() => handleUserClick(user.username)}
              >
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Avatar
                      src={user.profile_pic_url}
                      alt={user.username}
                      sx={{ width: 56, height: 56, mr: 2 }}
                    >
                      {user.username.charAt(0).toUpperCase()}
                    </Avatar>
                    <Box flex={1}>
                      <Typography variant="h6" component="div">
                        {user.full_name || user.username}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        @{user.username}
                      </Typography>
                    </Box>
                  </Box>
                  <Button
                    variant="outlined"
                    startIcon={<OpenInNew />}
                    onClick={(e) => {
                      e.stopPropagation();
                      openInstagramProfile(user.instagram_url);
                    }}
                    fullWidth
                    size="small"
                  >
                    View Profile
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {users.length > 0 && (
        <Box mt={3}>
          <Typography variant="body2" color="textSecondary">
            These are users you follow but who don't follow you back. 
            Click "View Profile" to open their Instagram profile in a new tab.
          </Typography>
        </Box>
      )}

      {/* User Profile Modal */}
      {selectedUser && (
        <UserProfile
          open={userProfileOpen}
          onClose={handleCloseUserProfile}
          username={selectedUser}
        />
      )}
    </Box>
  );
};

export default NotFollowingBack;
