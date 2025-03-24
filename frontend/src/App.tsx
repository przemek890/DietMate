import React, { useState, MouseEvent, useEffect  } from 'react';
import { createTheme, ThemeProvider, Fab } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Menu, MenuItem } from "@mui/material";
import { BrowserRouter as Router, Routes} from 'react-router-dom';
import Flag from 'react-world-flags';
import { useTranslation } from 'react-i18next';
import LanguageIcon from '@mui/icons-material/Language';
import GPT from "./Components/GPT/GPT";
import './i18n';

const App = () => {
    const [darkMode, setDarkMode] = useState<boolean>(false);
    const [anchorElLanguage, setAnchorElLanguage] = useState<null | HTMLElement>(null);
    const { i18n, t } = useTranslation();


    const handleThemeChange = (isDark: boolean): void => {
        setDarkMode(isDark);
    };

    const handleLanguageChange = (lang: string): void => {
        i18n.changeLanguage(lang);
    };

    // Notice:
    // Using localStorage would be incorrect as different browser tabs would share the same data because the token is issued per browser, not per session
    const [sessionToken, setSessionToken] = useState<string | null>(null);

      useEffect(() => {
        const initializeSession = async () => {
          try {
             // @ts-ignore
             const domain = window.REACT_APP_DOMAIN;
             const response = await fetch(`${domain}:5000/api/session`, {
              method: 'GET',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
              }
            });
      
            if (!response.ok) {
              throw new Error('Failed to initialize session');
            }
      
            const data = await response.json();
            setSessionToken(data.token);
            console.log('Session initialized successfully');
          } catch (err) {
            console.error('Session initialization error:', err);
          }
        };
      
        initializeSession();

      }, []);

    const theme = createTheme({
        palette: {
            primary: {
                main: darkMode ? '#ffffff' : '#000000',
            },
            mode: darkMode ? 'dark' : 'light',
            background: {
                default: darkMode ? '#1f1f23' : '#eaeaea',
            },
        },
    });

    const handleDarkModeToggle = (): void => {
        setDarkMode(!darkMode);
    };

    const handleLanguageClick = (event: MouseEvent<HTMLElement>): void => {
        setAnchorElLanguage(event.currentTarget);
    };

    const handleLanguageClose = (lang?: string): void => {
        if (lang) {
            i18n.changeLanguage(lang);
        }
        setAnchorElLanguage(null);
    };

    return (
        <Router>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <AppBar position="static">
                </AppBar>
                <Fab
                    color="primary"
                    aria-label="language"
                    style={{
                        position: 'fixed',
                        bottom: '20px',
                        right: '20px',
                        zIndex: 1000,
                    }}
                    onClick={handleLanguageClick}
                >
                    <LanguageIcon />
                </Fab>
                <Menu
                    id="language-menu"
                    anchorEl={anchorElLanguage}
                    keepMounted
                    open={Boolean(anchorElLanguage)}
                    onClose={() => handleLanguageClose()}
                >
                    <MenuItem onClick={() => handleLanguageClose('en')}>
                        <Flag code="US" height="16" width="24" style={{ marginRight: 8 }} />
                        {t('English')}
                    </MenuItem>
                    <MenuItem onClick={() => handleLanguageClose('pl')}>
                        <Flag code="PL" height="16" width="24" style={{ marginRight: 8 }} />
                        {t('Polish')}
                    </MenuItem>
                </Menu>

                <Routes>
                </Routes>
                <GPT
                    sessionToken={sessionToken}
                    setSessionToken={setSessionToken}
                />
            </ThemeProvider>
        </Router>
    );
};

export default App;