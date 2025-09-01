import {createContext, useContext} from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import {Box} from '@mui/material';

import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import NotFollowingBack from './pages/NotFollowingBack';
import Analytics from './pages/Analytics';
import { CustomThemeProvider } from './context/ThemeContext';

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
    const handleOpenProfile = (username: string) => {
        if (!username.trim()) {
            console.warn('Cannot open profile: username is empty');
            return;
        }
        // Directly redirect to Instagram instead of opening modal
        window.open(`https://instagram.com/${username}`, '_blank', 'noopener,noreferrer');
    };

    const profileContextValue: ProfileContextType = {
        openProfile: handleOpenProfile,
    };

    return (
        <CustomThemeProvider>
            <CssBaseline/>
            <ProfileContext.Provider value={profileContextValue}>
                <Router>
                    <Box sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        minHeight: '100vh',
                        background: (theme) => theme.palette.mode === 'light'
                            ? 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)'
                            : 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
                    }}>
                        <Navbar/>
                        <Box component="main" sx={{
                            flexGrow: 1,
                            p: { xs: 2, md: 4 },
                            maxWidth: '1400px',
                            width: '100%',
                            mx: 'auto',
                        }}>
                            <Routes>
                                <Route path="/" element={<Dashboard/>}/>
                                <Route path="/reports" element={<Reports/>}/>
                                <Route path="/not-following-back" element={<NotFollowingBack/>}/>
                                <Route path="/analytics" element={<Analytics/>}/>
                            </Routes>
                        </Box>
                    </Box>
                </Router>
            </ProfileContext.Provider>
        </CustomThemeProvider>
    );
}

export default App;