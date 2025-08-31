import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
} from '@mui/material';
import {
  People,
  PersonAdd,
  PersonRemove,
  TrendingUp,
  TrendingDown,
  Refresh,
} from '@mui/icons-material';
import { apiService, Report } from '../services/api';
import { format } from 'date-fns';

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [latestReport, setLatestReport] = useState<Report | null>(null);
  const [stats, setStats] = useState({
    followers: 0,
    following: 0,
    mutual: 0,
    followersOnly: 0,
    followingOnly: 0,
  });

  const fetchLatestReport = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getLatestReport();
      if (response.data.success) {
        setLatestReport(response.data.data);
        calculateStats(response.data.data);
      }
    } catch (err) {
      setError('Failed to fetch latest report');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateNewReport = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.generateReport();
      if (response.data.success) {
        setLatestReport(response.data.data);
        calculateStats(response.data.data);
      }
    } catch (err) {
      setError('Failed to generate new report');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (report: Report) => {
    const followers = report.users.filter(u => u.type?.includes('follower'));
    const following = report.users.filter(u => u.type?.includes('following'));
    const mutual = report.users.filter(u => 
      u.type?.includes('follower') && u.type?.includes('following')
    );

    setStats({
      followers: followers.length,
      following: following.length,
      mutual: mutual.length,
      followersOnly: followers.length - mutual.length,
      followingOnly: following.length - mutual.length,
    });
  };

  useEffect(() => {
    fetchLatestReport();
  }, []);

  const StatCard = ({ title, value, icon, color }: any) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="h6">
              {title}
            </Typography>
            <Typography variant="h4" component="div" color={color}>
              {value.toLocaleString()}
            </Typography>
          </Box>
          <Box color={color}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading && !latestReport) {
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
          Instagram Analytics Dashboard
        </Typography>
        <Button
          variant="contained"
          startIcon={<Refresh />}
          onClick={generateNewReport}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate New Report'}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {latestReport && (
        <Box mb={3}>
          <Typography variant="body2" color="textSecondary">
            Last updated: {format(new Date(latestReport.generated_at), 'PPP p')}
          </Typography>
        </Box>
      )}

      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={2}>
          <StatCard
            title="Followers"
            value={stats.followers}
            icon={<People fontSize="large" />}
            color="primary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <StatCard
            title="Following"
            value={stats.following}
            icon={<People fontSize="large" />}
            color="secondary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <StatCard
            title="Mutual"
            value={stats.mutual}
            icon={<People fontSize="large" />}
            color="success.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <StatCard
            title="Followers Only"
            value={stats.followersOnly}
            icon={<PersonAdd fontSize="large" />}
            color="info.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <StatCard
            title="Following Only"
            value={stats.followingOnly}
            icon={<PersonRemove fontSize="large" />}
            color="warning.main"
          />
        </Grid>
      </Grid>

      {latestReport && latestReport.stats && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Changes
                </Typography>
                <Box display="flex" flexDirection="column" gap={1}>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography>New Followers:</Typography>
                    <Chip
                      icon={<TrendingUp />}
                      label={latestReport.stats.new_followers_count || 0}
                      color="success"
                      size="small"
                    />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography>Lost Followers:</Typography>
                    <Chip
                      icon={<TrendingDown />}
                      label={latestReport.stats.lost_followers_count || 0}
                      color="error"
                      size="small"
                    />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography>New Following:</Typography>
                    <Chip
                      icon={<TrendingUp />}
                      label={latestReport.stats.new_following_count || 0}
                      color="success"
                      size="small"
                    />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography>Unfollowed:</Typography>
                    <Chip
                      icon={<TrendingDown />}
                      label={latestReport.stats.unfollowed_count || 0}
                      color="error"
                      size="small"
                    />
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Users
                </Typography>
                <List dense>
                  {latestReport.users.slice(0, 5).map((user) => (
                    <ListItem key={user.id}>
                      <ListItemAvatar>
                        <Avatar src={user.profile_pic_url} alt={user.username}>
                          {user.username.charAt(0).toUpperCase()}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={user.full_name || user.username}
                        secondary={`@${user.username}`}
                      />
                      <Box>
                        {user.type?.map((type) => (
                          <Chip
                            key={type}
                            label={type}
                            size="small"
                            color={type === 'follower' ? 'primary' : 'secondary'}
                            sx={{ mr: 0.5 }}
                          />
                        ))}
                      </Box>
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default Dashboard;
