import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import { ExpandMore, TrendingUp, TrendingDown } from '@mui/icons-material';
import { apiService, Report } from '../services/api';
import { format } from 'date-fns';

const Reports: React.FC = () => {
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
      const response = await apiService.getReports(20);
      if (response.data.success) {
        setReports(response.data.data);
      }
    } catch (err) {
      setError('Failed to fetch reports');
      console.error(err);
    } finally {
      setLoading(false);
    }
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
      <Typography variant="h4" component="h1" gutterBottom>
        Historical Reports
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <TableContainer component={Paper} sx={{ mb: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell align="right">Followers</TableCell>
              <TableCell align="right">Following</TableCell>
              <TableCell align="right">Mutual</TableCell>
              <TableCell align="right">New Followers</TableCell>
              <TableCell align="right">Lost Followers</TableCell>
              <TableCell align="right">Net Change</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reports.map((report) => {
              const followers = report.users.filter(u => u.type?.includes('follower'));
              const following = report.users.filter(u => u.type?.includes('following'));
              const mutual = report.users.filter(u => 
                u.type?.includes('follower') && u.type?.includes('following')
              );
              const netChange = (report.stats?.net_follower_change || 0);

              return (
                <TableRow key={report._id} hover>
                  <TableCell>
                    {format(new Date(report.generated_at), 'MMM dd, yyyy')}
                  </TableCell>
                  <TableCell align="right">{followers.length}</TableCell>
                  <TableCell align="right">{following.length}</TableCell>
                  <TableCell align="right">{mutual.length}</TableCell>
                  <TableCell align="right">
                    {report.stats?.new_followers_count || 0}
                  </TableCell>
                  <TableCell align="right">
                    {report.stats?.lost_followers_count || 0}
                  </TableCell>
                  <TableCell align="right">
                    <Chip
                      icon={netChange >= 0 ? <TrendingUp /> : <TrendingDown />}
                      label={netChange >= 0 ? `+${netChange}` : netChange}
                      color={netChange >= 0 ? 'success' : 'error'}
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="h5" gutterBottom>
        Detailed Reports
      </Typography>

      {reports.map((report) => (
        <Accordion key={report._id} sx={{ mb: 2 }}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Box display="flex" justifyContent="space-between" alignItems="center" width="100%">
              <Typography variant="h6">
                {format(new Date(report.generated_at), 'MMMM dd, yyyy')}
              </Typography>
              <Box display="flex" gap={2}>
                <Chip label={`${report.users.filter(u => u.type?.includes('follower')).length} Followers`} />
                <Chip label={`${report.users.filter(u => u.type?.includes('following')).length} Following`} />
              </Box>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              {report.stats && (
                <Box mb={3}>
                  <Typography variant="h6" gutterBottom>
                    Changes from Previous Report
                  </Typography>
                  <Box display="flex" gap={2} flexWrap="wrap">
                    <Chip
                      icon={<TrendingUp />}
                      label={`+${report.stats.new_followers_count || 0} New Followers`}
                      color="success"
                    />
                    <Chip
                      icon={<TrendingDown />}
                      label={`-${report.stats.lost_followers_count || 0} Lost Followers`}
                      color="error"
                    />
                    <Chip
                      icon={<TrendingUp />}
                      label={`+${report.stats.new_following_count || 0} New Following`}
                      color="success"
                    />
                    <Chip
                      icon={<TrendingDown />}
                      label={`-${report.stats.unfollowed_count || 0} Unfollowed`}
                      color="error"
                    />
                  </Box>
                </Box>
              )}

              <Typography variant="h6" gutterBottom>
                User Breakdown
              </Typography>
              <TableContainer component={Paper}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Username</TableCell>
                      <TableCell>Full Name</TableCell>
                      <TableCell>Type</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {report.users.slice(0, 10).map((user) => (
                      <TableRow key={user.id}>
                        <TableCell>@{user.username}</TableCell>
                        <TableCell>{user.full_name || '-'}</TableCell>
                        <TableCell>
                          <Box display="flex" gap={0.5}>
                            {user.type?.map((type) => (
                              <Chip
                                key={type}
                                label={type}
                                size="small"
                                color={type === 'follower' ? 'primary' : 'secondary'}
                              />
                            ))}
                          </Box>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
              {report.users.length > 10 && (
                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                  Showing first 10 users of {report.users.length} total
                </Typography>
              )}
            </Box>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
};

export default Reports;
