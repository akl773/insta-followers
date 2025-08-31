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
} from '@mui/material';
import {
    Close,
    Verified,
    Lock,
    Public,
    Language,
    Instagram,
    OpenInNew,
} from '@mui/icons-material';
import {apiService, UserDetails} from '../services/api';

interface UserProfileProps {
    open: boolean;
    onClose: () => void;
    username: string;
}

const UserProfile: React.FC<UserProfileProps> = ({open, onClose, username}) => {
    const [userDetails, setUserDetails] = useState<UserDetails | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (open && username) {
            (async () => {
                await fetchUserDetails();
            })();
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

    if (loading) {
        return (
            <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
                <DialogContent>
                    <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                        <CircularProgress/>
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
                        <Close/>
                    </IconButton>
                </Box>
            </DialogTitle>

            <DialogContent>
                {error && (
                    <Alert severity="error" sx={{mb: 2}}>
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
                                sx={{width: 80, height: 80, mr: 3}}
                            >
                                {userDetails.username.charAt(0).toUpperCase()}
                            </Avatar>

                            <Box flex={1}>
                                <Box display="flex" alignItems="center" mb={1}>
                                    <Typography variant="h5" component="div" sx={{mr: 1}}>
                                        {userDetails.username}
                                    </Typography>
                                    {userDetails.is_verified && (
                                        <Verified color="primary" sx={{mr: 1}}/>
                                    )}
                                    {userDetails.is_private ? (
                                        <Lock color="action"/>
                                    ) : (
                                        <Public color="action"/>
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
                                        sx={{display: 'flex', alignItems: 'center', mb: 1}}
                                    >
                                        <Language sx={{mr: 0.5, fontSize: 16}}/>
                                        {userDetails.website}
                                    </Link>
                                )}

                                <Button
                                    variant="outlined"
                                    startIcon={<Instagram/>}
                                    onClick={openInstagramProfile}
                                    size="small"
                                >
                                    View on Instagram
                                </Button>
                            </Box>
                        </Box>

                        {/* Stats */}
                        <Paper sx={{p: 2, mb: 3}}>
                            <Grid container spacing={2} textAlign="center">
                                <Grid item xs={4}>
                                    <Typography variant="h6">{formatNumber(userDetails.media_count)}</Typography>
                                    <Typography variant="body2" color="textSecondary">Posts</Typography>
                                </Grid>
                                <Grid item xs={4}>
                                    <Typography variant="h6">{formatNumber(userDetails.followers_count)}</Typography>
                                    <Typography variant="body2" color="textSecondary">Followers</Typography>
                                </Grid>
                                <Grid item xs={4}>
                                    <Typography variant="h6">{formatNumber(userDetails.following_count)}</Typography>
                                    <Typography variant="body2" color="textSecondary">Following</Typography>
                                </Grid>
                            </Grid>
                        </Paper>

                        {/* Biography */}
                        {userDetails.biography && (
                            <Box mb={3}>
                                <Typography variant="body1" sx={{whiteSpace: 'pre-wrap'}}>
                                    {userDetails.biography}
                                </Typography>
                            </Box>
                        )}

                        <Divider sx={{my: 3}}/>
                    </Box>
                )}
            </DialogContent>

            <DialogActions>
                <Button onClick={onClose}>Close</Button>
                {userDetails && (
                    <Button
                        variant="contained"
                        startIcon={<OpenInNew/>}
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
