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
  useTheme,
  alpha,
  Paper,
  Fade,
} from '@mui/material';
import {
  People,
  PersonAdd,
  PersonRemove,
  TrendingUp,
  TrendingDown,
  Refresh,
  Instagram,
} from '@mui/icons-material';
import { apiService, Report } from '../services/api';
import { format } from 'date-fns';

const Dashboard: React.FC = () => {
  const theme = useTheme();
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
      // For now, we'll just refetch the latest report since generateReport endpoint doesn't exist
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

  const handleUserClick = (username: string) => {
    window.open(`https://instagram.com/${username}`, '_blank', 'noopener,noreferrer');
  };

  useEffect(() => {
    fetchLatestReport();
  }, []);

  const StatCard = ({ title, value, icon, color, trend }: any) => (
    <Card
      sx={{
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        '&:hover': {
          transform: 'translateY(-4px)',
          transition: 'all 0.3s ease-in-out',
          boxShadow: theme.shadows[8],
        },
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          right: 0,
          width: 80,
          height: 80,
          background: `linear-gradient(135deg, ${alpha(color, 0.1)}, ${alpha(color, 0.05)})`,
          borderRadius: '0 0 0 80px',
        }}
      />
      <CardContent sx={{ position: 'relative', zIndex: 1 }}>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Box
            sx={{
              p: 1.5,
              borderRadius: 2,
              background: `linear-gradient(135deg, ${alpha(color, 0.1)}, ${alpha(color, 0.05)})`,
              color: color,
            }}
          >
            {icon}
          </Box>
          {trend && (
            <Chip
              label={trend}
              size="small"
              sx={{
                backgroundColor: alpha(theme.palette.success.main, 0.1),
                color: theme.palette.success.main,
                fontWeight: 600,
              }}
            />
          )}
        </Box>
        <Typography
          variant="h3"
          component="div"
          sx={{
            fontWeight: 700,
            mb: 1,
            background: `linear-gradient(135deg, ${color}, ${alpha(color, 0.7)})`,
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          {value.toLocaleString()}
        </Typography>
        <Typography
          color="text.secondary"
          variant="body2"
          sx={{ fontWeight: 500 }}
        >
          {title}
        </Typography>
      </CardContent>
    </Card>
  );

  if (loading && !latestReport) {
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
          Loading analytics...
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
            background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)}, ${alpha(theme.palette.secondary.main, 0.05)})`,
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
                  background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Analytics Dashboard
              </Typography>
              {latestReport && (
                <Typography variant="body1" color="text.secondary" sx={{ fontWeight: 500 }}>
                  Last updated: {format(new Date(latestReport.generated_at), 'PPP p')}
                </Typography>
              )}
            </Box>
            <Button
              variant="contained"
              size="large"
              startIcon={<Refresh />}
              onClick={generateNewReport}
              disabled={loading}
              sx={{
                px: 3,
                py: 1.5,
                borderRadius: 2,
                fontWeight: 600,
                background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                '&:hover': {
                  background: `linear-gradient(135deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`,
                  transform: 'translateY(-2px)',
                  boxShadow: theme.shadows[8],
                },
                transition: 'all 0.2s ease-in-out',
              }}
            >
              {loading ? 'Generating...' : 'Generate New Report'}
            </Button>
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

        {/* Stats Grid */}
        <Grid container spacing={3} mb={4}>
          <Grid item xs={12} sm={6} lg={2.4}>
            <StatCard
              title="Total Followers"
              value={stats.followers}
              icon={<People fontSize="large" />}
              color={theme.palette.primary.main}
              trend="+12%"
            />
          </Grid>
          <Grid item xs={12} sm={6} lg={2.4}>
            <StatCard
              title="Following"
              value={stats.following}
              icon={<PersonAdd fontSize="large" />}
              color={theme.palette.secondary.main}
              trend="+5%"
            />
          </Grid>
          <Grid item xs={12} sm={6} lg={2.4}>
            <StatCard
              title="Mutual Follows"
              value={stats.mutual}
              icon={<TrendingUp fontSize="large" />}
              color={theme.palette.success.main}
              trend="+8%"
            />
          </Grid>
          <Grid item xs={12} sm={6} lg={2.4}>
            <StatCard
              title="Followers Only"
              value={stats.followersOnly}
              icon={<TrendingDown fontSize="large" />}
              color={theme.palette.info.main}
            />
          </Grid>
          <Grid item xs={12} sm={6} lg={2.4}>
            <StatCard
              title="Following Only"
              value={stats.followingOnly}
              icon={<PersonRemove fontSize="large" />}
              color={theme.palette.warning.main}
            />
          </Grid>
        </Grid>

        {/* Recent Activity */}
        {latestReport && latestReport.users.length > 0 && (
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
                <Instagram color="primary" />
                Recent Activity - Click to view on Instagram
              </Typography>
              <List sx={{ maxHeight: 400, overflow: 'auto' }}>
                {latestReport.users.slice(0, 10).map((user) => (
                  <ListItem
                    key={user.username}
                    sx={{
                      borderRadius: 2,
                      mb: 1,
                      border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
                      '&:hover': {
                        backgroundColor: alpha(theme.palette.primary.main, 0.05),
                        cursor: 'pointer',
                        transform: 'translateY(-2px)',
                        boxShadow: theme.shadows[4],
                      },
                      transition: 'all 0.2s ease-in-out',
                    }}
                    onClick={() => handleUserClick(user.username)}
                  >
                    <ListItemAvatar>
                      <Avatar
                        src={user.profile_pic_url}
                        sx={{
                          width: 48,
                          height: 48,
                          border: `2px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                        }}
                      >
                        {user.username[0].toUpperCase()}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          @{user.username}
                        </Typography>
                      }
                      secondary={
                        <Box sx={{ mt: 0.5 }}>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            {user.full_name}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                            {user.type?.map((type) => (
                              <Chip
                                key={type}
                                label={type}
                                size="small"
                                sx={{
                                  backgroundColor: type === 'follower'
                                    ? alpha(theme.palette.primary.main, 0.1)
                                    : alpha(theme.palette.secondary.main, 0.1),
                                  color: type === 'follower'
                                    ? theme.palette.primary.main
                                    : theme.palette.secondary.main,
                                  fontWeight: 500,
                                }}
                              />
                            ))}
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        )}
      </Box>
    </Fade>
  );
};

export default Dashboard;
