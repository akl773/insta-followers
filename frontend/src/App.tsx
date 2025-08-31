import {useState, createContext, useContext} from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import {ThemeProvider, createTheme} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {Box} from '@mui/material';

import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import NotFollowingBack from './pages/NotFollowingBack';
import Analytics from './pages/Analytics';
import UserProfile from './components/UserProfile';

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
        background: {
            default: '#0a0a0a',
            paper: '#1a1a1a',
        },
    },
    typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    },
});

// Context for profile management
interface ProfileContextType {
    openProfile: (username: string) => void;
}

const ProfileContext = createContext<ProfileContextType | undefined>(undefined);

export const useProfile = () => {
    const context = useContext(ProfileContext);
    if (context === undefined) {
        throw new Error('useProfile must be used within a ProfileProvider');
    }
    return context;
};

function App() {
    const [profileOpen, setProfileOpen] = useState(false);
    const [selectedUsername, setSelectedUsername] = useState('');

    const handleOpenProfile = (username: string) => {
        if (!username.trim()) {
            console.warn('Cannot open profile: username is empty');
            return;
        }
        setSelectedUsername(username);
        setProfileOpen(true);
    };

    const handleCloseProfile = () => {
        setProfileOpen(false);
        // Clear username after a short delay to prevent flickering
        setTimeout(() => {
            if (!profileOpen) {
                setSelectedUsername('');
            }
        }, 300);
    };

    const profileContextValue: ProfileContextType = {
        openProfile: handleOpenProfile,
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline/>
            <ProfileContext.Provider value={profileContextValue}>
                <Router>
                    <Box sx={{display: 'flex', flexDirection: 'column', minHeight: '100vh'}}>
                        <Navbar/>
                        <Box component="main" sx={{flexGrow: 1, p: 3}}>
                            <Routes>
                                <Route path="/" element={<Dashboard/>}/>
                                <Route path="/reports" element={<Reports/>}/>
                                <Route path="/not-following-back" element={<NotFollowingBack/>}/>
                                <Route path="/analytics" element={<Analytics/>}/>
                            </Routes>
                        </Box>
                        {/* UserProfile dialog - only render when needed */}
                        {selectedUsername && (
                            <UserProfile
                                open={profileOpen}
                                onClose={handleCloseProfile}
                                username={selectedUsername}
                            />
                        )}
                    </Box>
                </Router>
            </ProfileContext.Provider>
        </ThemeProvider>
    );
}

export default App;