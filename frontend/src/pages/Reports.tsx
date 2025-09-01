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
  useTheme,
  alpha,
  Fade,
} from '@mui/material';
import { ExpandMore, TrendingUp, TrendingDown, Assessment } from '@mui/icons-material';
import { apiService, Report } from '../services/api';
import { format } from 'date-fns';

const Reports: React.FC = () => {
  const theme = useTheme();
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

  const handleUserClick = (username: string) => {
    window.open(`https://instagram.com/${username}`, '_blank', 'noopener,noreferrer');
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
          Loading reports...
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
            background: `linear-gradient(135deg, ${alpha(theme.palette.info.main, 0.05)}, ${alpha(theme.palette.primary.main, 0.05)})`,
            border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
            borderRadius: 3,
          }}
        >
          <Box display="flex" alignItems="center" gap={2}>
            <Assessment sx={{ fontSize: 40, color: theme.palette.info.main }} />
            <Box>
              <Typography
                variant="h3"
                component="h1"
                sx={{
                  fontWeight: 800,
                  mb: 1,
                  background: `linear-gradient(135deg, ${theme.palette.info.main}, ${theme.palette.primary.main})`,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Analytics Reports
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ fontWeight: 500 }}>
                Click on any username to view their Instagram profile
              </Typography>
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

        {reports.length === 0 ? (
          <Card sx={{ borderRadius: 3 }}>
            <CardContent sx={{ p: 6, textAlign: 'center' }}>
              <Typography variant="h6" color="text.secondary">
                No reports available
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Generate your first report to see analytics data here.
              </Typography>
            </CardContent>
          </Card>
        ) : (
          <Box sx={{ mb: 3 }}>
            {reports.map((report, index) => (
              <Accordion
                key={report._id}
                defaultExpanded={index === 0}
                sx={{
                  mb: 2,
                  borderRadius: 2,
                  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
                  '&:before': {
                    display: 'none',
                  },
                  '&.Mui-expanded': {
                    margin: '0 0 16px 0',
                  },
                }}
              >
                <AccordionSummary
                  expandIcon={<ExpandMore />}
                  sx={{
                    background: `linear-gradient(135deg, ${alpha(theme.palette.info.main, 0.05)}, ${alpha(theme.palette.primary.main, 0.02)})`,
                    borderRadius: '8px 8px 0 0',
                    '&.Mui-expanded': {
                      borderRadius: '8px 8px 0 0',
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      Report - {format(new Date(report.generated_at), 'PPP')}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, ml: 'auto', mr: 2 }}>
                      <Chip
                        label={`${report.num_followers} followers`}
                        size="small"
                        sx={{
                          backgroundColor: alpha(theme.palette.primary.main, 0.1),
                          color: theme.palette.primary.main,
                        }}
                      />
                      <Chip
                        label={`${report.num_following} following`}
                        size="small"
                        sx={{
                          backgroundColor: alpha(theme.palette.secondary.main, 0.1),
                          color: theme.palette.secondary.main,
                        }}
                      />
                    </Box>
                  </Box>
                </AccordionSummary>
                <AccordionDetails sx={{ p: 0 }}>
                  {report.stats && (
                    <Box sx={{ p: 3, borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}` }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        Changes from Previous Report
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                        <Chip
                          icon={<TrendingUp />}
                          label={`+${report.stats.new_followers_count} new followers`}
                          sx={{
                            backgroundColor: alpha(theme.palette.success.main, 0.1),
                            color: theme.palette.success.main,
                          }}
                        />
                        <Chip
                          icon={<TrendingDown />}
                          label={`-${report.stats.lost_followers_count} lost followers`}
                          sx={{
                            backgroundColor: alpha(theme.palette.error.main, 0.1),
                            color: theme.palette.error.main,
                          }}
                        />
                        <Chip
                          label={`Net: ${report.stats.net_follower_change >= 0 ? '+' : ''}${report.stats.net_follower_change}`}
                          sx={{
                            backgroundColor: report.stats.net_follower_change >= 0
                              ? alpha(theme.palette.success.main, 0.1)
                              : alpha(theme.palette.error.main, 0.1),
                            color: report.stats.net_follower_change >= 0
                              ? theme.palette.success.main
                              : theme.palette.error.main,
                          }}
                        />
                      </Box>
                    </Box>
                  )}

                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell sx={{ fontWeight: 600 }}>Username</TableCell>
                          <TableCell sx={{ fontWeight: 600 }}>Full Name</TableCell>
                          <TableCell sx={{ fontWeight: 600 }}>Type</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {report.users.slice(0, 50).map((user) => (
                          <TableRow
                            key={user.id}
                            sx={{
                              '&:hover': {
                                backgroundColor: alpha(theme.palette.primary.main, 0.05),
                                cursor: 'pointer',
                              },
                              transition: 'all 0.2s ease-in-out',
                            }}
                            onClick={() => handleUserClick(user.username)}
                          >
                            <TableCell>
                              <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                @{user.username}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Typography variant="body2">
                                {user.full_name || 'N/A'}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
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
                                      fontSize: '0.75rem',
                                    }}
                                  />
                                ))}
                              </Box>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>

                  {report.users.length > 50 && (
                    <Box sx={{ p: 2, textAlign: 'center', borderTop: `1px solid ${alpha(theme.palette.divider, 0.1)}` }}>
                      <Typography variant="body2" color="text.secondary">
                        Showing first 50 of {report.users.length} users
                      </Typography>
                    </Box>
                  )}
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        )}
      </Box>
    </Fade>
  );
};

export default Reports;
