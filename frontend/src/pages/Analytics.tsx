import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { apiService, Report } from '../services/api';
import { format } from 'date-fns';

const Analytics: React.FC = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getReports(30); // Get last 30 reports
      if (response.data.success) {
        setReports(response.data.data);
      }
    } catch (err) {
      setError('Failed to fetch reports for analytics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const prepareChartData = () => {
    return reports.map((report) => {
      const followers = report.users.filter(u => u.type?.includes('follower'));
      const following = report.users.filter(u => u.type?.includes('following'));
      const mutual = report.users.filter(u => 
        u.type?.includes('follower') && u.type?.includes('following')
      );

      return {
        date: format(new Date(report.generated_at), 'MMM dd'),
        followers: followers.length,
        following: following.length,
        mutual: mutual.length,
        followersOnly: followers.length - mutual.length,
        followingOnly: following.length - mutual.length,
        newFollowers: report.stats?.new_followers_count || 0,
        lostFollowers: report.stats?.lost_followers_count || 0,
        netChange: report.stats?.net_follower_change || 0,
      };
    }).reverse(); // Show oldest to newest
  };

  const preparePieData = () => {
    if (reports.length === 0) return [];
    
    const latestReport = reports[0];
    const followers = latestReport.users.filter(u => u.type?.includes('follower'));
    const following = latestReport.users.filter(u => u.type?.includes('following'));
    const mutual = latestReport.users.filter(u => 
      u.type?.includes('follower') && u.type?.includes('following')
    );

    return [
      { name: 'Mutual', value: mutual.length, color: '#4caf50' },
      { name: 'Followers Only', value: followers.length - mutual.length, color: '#2196f3' },
      { name: 'Following Only', value: following.length - mutual.length, color: '#ff9800' },
    ];
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  const chartData = prepareChartData();
  const pieData = preparePieData();

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Analytics & Trends
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {reports.length === 0 ? (
        <Card>
          <CardContent>
            <Typography variant="h6" align="center" color="textSecondary">
              No data available for analytics
            </Typography>
            <Typography variant="body2" align="center" color="textSecondary">
              Generate some reports first to see analytics and trends.
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {/* Follower Growth Trend */}
          <Grid item xs={12} lg={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Follower Growth Trend
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="followers"
                      stroke="#2196f3"
                      strokeWidth={2}
                      name="Followers"
                    />
                    <Line
                      type="monotone"
                      dataKey="following"
                      stroke="#ff9800"
                      strokeWidth={2}
                      name="Following"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Relationship Distribution */}
          <Grid item xs={12} lg={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Relationship Distribution
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Net Follower Changes */}
          <Grid item xs={12} lg={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Net Follower Changes
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar
                      dataKey="netChange"
                      fill={(entry) => entry.netChange >= 0 ? '#4caf50' : '#f44336'}
                      name="Net Change"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Detailed Breakdown */}
          <Grid item xs={12} lg={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Detailed Breakdown
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="newFollowers" fill="#4caf50" name="New Followers" />
                    <Bar dataKey="lostFollowers" fill="#f44336" name="Lost Followers" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Summary Statistics */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Summary Statistics
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="h4" color="primary">
                        {reports.length}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Total Reports
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="h4" color="success.main">
                        {chartData.length > 0 ? Math.max(...chartData.map(d => d.followers)) : 0}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Peak Followers
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="h4" color="info.main">
                        {chartData.reduce((sum, d) => sum + d.netChange, 0)}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Total Net Growth
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="h4" color="warning.main">
                        {chartData.length > 1 ? 
                          Math.round((chartData[chartData.length - 1].followers - chartData[0].followers) / chartData.length) : 0}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Avg Daily Growth
                      </Typography>
                    </Paper>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default Analytics;
