import React, {useState, useEffect} from 'react';
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
    Divider,
    CircularProgress,
    Alert,
    IconButton,
    Link,
    Paper,
    useTheme,
    alpha,
    Slide,
    Chip,
} from '@mui/material';
import {
    Close,
    Verified,
    Lock,
    Public,
    Language,
    Instagram,
    OpenInNew,
    Person,
    Groups,
    PhotoCamera,
} from '@mui/icons-material';
import {apiService, UserDetails} from '../services/api';

const Transition = React.forwardRef(function Transition(props: any, ref: React.Ref<unknown>) {
  return <Slide direction="up" ref={ref} {...props} />;
});

interface UserProfileProps {
    open: boolean;
    onClose: () => void;
    username: string;
}

const UserProfile: React.FC<UserProfileProps> = ({open, onClose, username}) => {
    const theme = useTheme();
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

    const formatNumber = (num: number) => {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    };

    const StatItem = ({ icon, label, value, color }: any) => (
        <Paper
            sx={{
                p: 3,
                textAlign: 'center',
                background: `linear-gradient(135deg, ${alpha(color, 0.05)}, ${alpha(color, 0.02)})`,
                border: `1px solid ${alpha(color, 0.1)}`,
                borderRadius: 3,
                '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: theme.shadows[4],
                },
                transition: 'all 0.2s ease-in-out',
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    mb: 2,
                    color: color,
                }}
            >
                {icon}
            </Box>
            <Typography
                variant="h4"
                sx={{
                    fontWeight: 700,
                    mb: 1,
                    background: `linear-gradient(135deg, ${color}, ${alpha(color, 0.7)})`,
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                }}
            >
                {formatNumber(value)}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 500 }}>
                {label}
            </Typography>
        </Paper>
    );

    return (
        <Dialog
            open={open}
            onClose={onClose}
            maxWidth="md"
            fullWidth
            TransitionComponent={Transition}
            sx={{
                '& .MuiDialog-paper': {
                    borderRadius: 3,
                    background: theme.palette.mode === 'dark'
                        ? `linear-gradient(135deg, ${alpha(theme.palette.background.paper, 0.9)}, ${alpha(theme.palette.background.paper, 0.8)})`
                        : `linear-gradient(135deg, ${alpha(theme.palette.background.paper, 0.95)}, ${alpha(theme.palette.background.paper, 0.9)})`,
                    backdropFilter: 'blur(20px)',
                },
            }}
        >
            <DialogTitle
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    pb: 2,
                    background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)}, ${alpha(theme.palette.secondary.main, 0.05)})`,
                    borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
                }}
            >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Instagram color="primary" />
                    <Typography variant="h5" sx={{ fontWeight: 700 }}>
                        User Profile
                    </Typography>
                </Box>
                <IconButton
                    onClick={onClose}
                    sx={{
                        border: `1px solid ${alpha(theme.palette.divider, 0.3)}`,
                        '&:hover': {
                            backgroundColor: alpha(theme.palette.error.main, 0.1),
                            borderColor: alpha(theme.palette.error.main, 0.3),
                        },
                    }}
                >
                    <Close />
                </IconButton>
            </DialogTitle>

            <DialogContent sx={{ p: 4 }}>
                {loading && (
                    <Box display="flex" flexDirection="column" alignItems="center" py={6} gap={2}>
                        <CircularProgress size={60} thickness={4} />
                        <Typography variant="h6" color="text.secondary">
                            Loading profile...
                        </Typography>
                    </Box>
                )}

                {error && (
                    <Alert
                        severity="error"
                        sx={{
                            borderRadius: 2,
                            '& .MuiAlert-icon': {
                                fontSize: '1.5rem',
                            },
                        }}
                    >
                        {error}
                    </Alert>
                )}

                {userDetails && !loading && (
                    <Box>
                        {/* Profile Header */}
                        <Paper
                            sx={{
                                p: 4,
                                mb: 4,
                                background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)}, ${alpha(theme.palette.secondary.main, 0.05)})`,
                                border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
                                borderRadius: 3,
                            }}
                        >
                            <Box display="flex" alignItems="center" gap={3} mb={3}>
                                <Avatar
                                    src={userDetails.profile_pic_url}
                                    sx={{
                                        width: 100,
                                        height: 100,
                                        border: `4px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                                        boxShadow: theme.shadows[4],
                                    }}
                                >
                                    {username[0].toUpperCase()}
                                </Avatar>
                                <Box flex={1}>
                                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                                        <Typography variant="h4" sx={{ fontWeight: 700 }}>
                                            @{username}
                                        </Typography>
                                        {userDetails.is_verified && (
                                            <Verified color="primary" />
                                        )}
                                        {userDetails.is_private && (
                                            <Chip
                                                icon={<Lock />}
                                                label="Private"
                                                size="small"
                                                sx={{
                                                    backgroundColor: alpha(theme.palette.warning.main, 0.1),
                                                    color: theme.palette.warning.main,
                                                }}
                                            />
                                        )}
                                    </Box>
                                    {userDetails.full_name && (
                                        <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
                                            {userDetails.full_name}
                                        </Typography>
                                    )}
                                    {userDetails.biography && (
                                        <Typography variant="body1" sx={{ mb: 2 }}>
                                            {userDetails.biography}
                                        </Typography>
                                    )}
                                    {userDetails.external_url && (
                                        <Link
                                            href={userDetails.external_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            sx={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: 1,
                                                color: theme.palette.primary.main,
                                                textDecoration: 'none',
                                                '&:hover': {
                                                    textDecoration: 'underline',
                                                },
                                            }}
                                        >
                                            <Language />
                                            {userDetails.external_url}
                                            <OpenInNew fontSize="small" />
                                        </Link>
                                    )}
                                </Box>
                            </Box>
                        </Paper>

                        {/* Stats Grid */}
                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={4}>
                                <StatItem
                                    icon={<PhotoCamera fontSize="large" />}
                                    label="Posts"
                                    value={userDetails.media_count || 0}
                                    color={theme.palette.primary.main}
                                />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <StatItem
                                    icon={<Person fontSize="large" />}
                                    label="Followers"
                                    value={userDetails.follower_count || 0}
                                    color={theme.palette.secondary.main}
                                />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <StatItem
                                    icon={<Groups fontSize="large" />}
                                    label="Following"
                                    value={userDetails.following_count || 0}
                                    color={theme.palette.success.main}
                                />
                            </Grid>
                        </Grid>
                    </Box>
                )}
            </DialogContent>

            <DialogActions
                sx={{
                    p: 3,
                    borderTop: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
                    background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.02)}, ${alpha(theme.palette.secondary.main, 0.02)})`,
                }}
            >
                <Button
                    onClick={onClose}
                    variant="contained"
                    sx={{
                        px: 4,
                        py: 1.5,
                        borderRadius: 2,
                        fontWeight: 600,
                        background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                        '&:hover': {
                            background: `linear-gradient(135deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`,
                            transform: 'translateY(-1px)',
                            boxShadow: theme.shadows[4],
                        },
                        transition: 'all 0.2s ease-in-out',
                    }}
                >
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default UserProfile;

