import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Avatar,
  Typography,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Chip,
  Divider,
  CircularProgress,
  Alert,
  IconButton,
  Link,
  Paper,
} from '@mui/material';
import {
  Close,
  Verified,
  Lock,
  Public,
  Favorite,
  ChatBubble,
  CalendarToday,
  Language,
  Instagram,
  OpenInNew,
} from '@mui/icons-material';
import { apiService, UserDetails } from '../services/api';
import { format } from 'date-fns';

interface UserProfileProps {
  open: boolean;
  onClose: () => void;
  username: string;
}

const UserProfile: React.FC<UserProfileProps> = ({ open, onClose, username }) => {
  const [userDetails, setUserDetails] = useState<UserDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open && username) {
      fetchUserDetails();
    }
  }, [open, username]);

  const fetchUserDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getUserDetails(username);
      if (response.data.success) {
        setUserDetails(response.data.data);
      } else {
        setError('Failed to fetch user details');
      }
    } catch (err) {
      setError('Failed to fetch user details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openInstagramProfile = () => {
    window.open(`https://www.instagram.com/${username}/`, '_blank');
  };

  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
  };

  const getMediaTypeIcon = (mediaType: number) => {
    switch (mediaType) {
      case 1: // Photo
        return null;
      case 2: // Video
        return '🎥';
      case 8: // Album
        return '📷';
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
        <DialogContent>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
            <CircularProgress />
          </Box>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">User Profile</Typography>
          <IconButton onClick={onClose}>
            <Close />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {userDetails && (
          <Box>
            {/* Profile Header */}
            <Box display="flex" alignItems="center" mb={3}>
              <Avatar
                src={userDetails.profile_pic_url}
                alt={userDetails.username}
                sx={{ width: 80, height: 80, mr: 3 }}
              >
                {userDetails.username.charAt(0).toUpperCase()}
              </Avatar>
              
              <Box flex={1}>
                <Box display="flex" alignItems="center" mb={1}>
                  <Typography variant="h5" component="div" sx={{ mr: 1 }}>
                    {userDetails.username}
                  </Typography>
                  {userDetails.is_verified && (
                    <Verified color="primary" sx={{ mr: 1 }} />
                  )}
                  {userDetails.is_private ? (
                    <Lock color="action" />
                  ) : (
                    <Public color="action" />
                  )}
                </Box>
                
                <Typography variant="body1" color="textSecondary" mb={1}>
                  {userDetails.full_name}
                </Typography>
                
                {userDetails.website && (
                  <Link
                    href={userDetails.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{ display: 'flex', alignItems: 'center', mb: 1 }}
                  >
                    <Language sx={{ mr: 0.5, fontSize: 16 }} />
                    {userDetails.website}
                  </Link>
                )}
                
                <Button
                  variant="outlined"
                  startIcon={<Instagram />}
                  onClick={openInstagramProfile}
                  size="small"
                >
                  View on Instagram
                </Button>
              </Box>
            </Box>

            {/* Stats */}
            <Paper sx={{ p: 2, mb: 3 }}>
              <Grid container spacing={2} textAlign="center">
                <Grid item xs={3}>
                  <Typography variant="h6">{formatNumber(userDetails.media_count)}</Typography>
                  <Typography variant="body2" color="textSecondary">Posts</Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h6">{formatNumber(userDetails.followers_count)}</Typography>
                  <Typography variant="body2" color="textSecondary">Followers</Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h6">{formatNumber(userDetails.following_count)}</Typography>
                  <Typography variant="body2" color="textSecondary">Following</Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h6">
                    {userDetails.relationship_status.is_mutual ? 'Mutual' : 'Not Mutual'}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">Connection</Typography>
                </Grid>
              </Grid>
            </Paper>

            {/* Biography */}
            {userDetails.biography && (
              <Box mb={3}>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                  {userDetails.biography}
                </Typography>
              </Box>
            )}

            {/* Relationship Status */}
            <Box mb={3}>
              <Typography variant="h6" gutterBottom>Relationship Status</Typography>
              <Box display="flex" gap={1} flexWrap="wrap">
                <Chip
                  label={userDetails.relationship_status.is_following_us ? 'Follows You' : 'Doesn\'t Follow You'}
                  color={userDetails.relationship_status.is_following_us ? 'success' : 'default'}
                  size="small"
                />
                <Chip
                  label={userDetails.relationship_status.we_are_following ? 'You Follow Them' : 'You Don\'t Follow'}
                  color={userDetails.relationship_status.we_are_following ? 'primary' : 'default'}
                  size="small"
                />
                {userDetails.relationship_status.is_mutual && (
                  <Chip
                    label="Mutual Connection"
                    color="secondary"
                    size="small"
                  />
                )}
              </Box>
            </Box>

            <Divider sx={{ my: 3 }} />

            {/* Recent Posts */}
            <Typography variant="h6" gutterBottom>Recent Posts</Typography>
            {userDetails.recent_posts.length > 0 ? (
              <Grid container spacing={2}>
                {userDetails.recent_posts.map((post) => (
                  <Grid item xs={12} sm={6} md={4} key={post.id}>
                    <Card>
                      <CardMedia
                        component="img"
                        height="200"
                        image={post.thumbnail_url || post.media_url || ''}
                        alt="Post"
                        sx={{ objectFit: 'cover' }}
                      />
                      <CardContent sx={{ p: 1 }}>
                        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                          <Box display="flex" alignItems="center" gap={0.5}>
                            <Favorite fontSize="small" color="error" />
                            <Typography variant="caption">
                              {formatNumber(post.like_count)}
                            </Typography>
                          </Box>
                          <Box display="flex" alignItems="center" gap={0.5}>
                            <ChatBubble fontSize="small" color="action" />
                            <Typography variant="caption">
                              {formatNumber(post.comment_count)}
                            </Typography>
                          </Box>
                        </Box>
                        
                        {post.caption && (
                          <Typography variant="caption" color="textSecondary" sx={{
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical',
                            overflow: 'hidden',
                          }}>
                            {post.caption}
                          </Typography>
                        )}
                        
                        {post.taken_at && (
                          <Box display="flex" alignItems="center" mt={1}>
                            <CalendarToday fontSize="small" color="action" sx={{ mr: 0.5 }} />
                            <Typography variant="caption" color="textSecondary">
                              {format(new Date(post.taken_at), 'MMM dd, yyyy')}
                            </Typography>
                          </Box>
                        )}
                        
                        {getMediaTypeIcon(post.media_type) && (
                          <Typography variant="caption" sx={{ ml: 1 }}>
                            {getMediaTypeIcon(post.media_type)}
                          </Typography>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Typography variant="body2" color="textSecondary" align="center">
                No recent posts available
              </Typography>
            )}
          </Box>
        )}
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
        {userDetails && (
          <Button
            variant="contained"
            startIcon={<OpenInNew />}
            onClick={openInstagramProfile}
          >
            Open Instagram Profile
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default UserProfile;
