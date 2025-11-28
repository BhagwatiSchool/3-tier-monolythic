// src/theme/ThemeProvider.tsx
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { api } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

type ThemeMode = 'light' | 'dark';
interface ThemeShape {
  mode?: ThemeMode;
  primaryColor?: string;
  [k: string]: any;
}

type ThemeContextValue = {
  theme: ThemeMode;
  setThemeMode: (m: ThemeMode) => void;
  toggle: () => void;
  remoteConfig: ThemeShape | null;
  saveTheme: (cfg?: Partial<ThemeShape>) => Promise<void>;
  loading: boolean;
};

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
}

// Helper to convert HEX to HSL
function hexToHSL(hex: string): string {
  hex = hex.replace('#', '');
  const r = parseInt(hex.substring(0, 2), 16) / 255;
  const g = parseInt(hex.substring(2, 4), 16) / 255;
  const b = parseInt(hex.substring(4, 6), 16) / 255;
  
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0, s = 0, l = (max + min) / 2;
  
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
      case g: h = ((b - r) / d + 2) / 6; break;
      case b: h = ((r - g) / d + 4) / 6; break;
    }
  }
  
  return `${Math.round(h * 360)} ${Math.round(s * 100)}% ${Math.round(l * 100)}%`;
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [theme, setTheme] = useState<ThemeMode>('light');
  const [remoteConfig, setRemoteConfig] = useState<ThemeShape | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  // Define saveTheme early so it's available for useEffects
  const saveTheme = async (cfg?: Partial<ThemeShape>) => {
    // merge with remote config - keep all user-specific settings
    const payload = { ...(remoteConfig || {}), ...(cfg || {}), mode: cfg?.mode || theme };
    try {
      await api.updateTheme(payload);
      setRemoteConfig(payload);
    } catch (err) {
      console.error('saveTheme failed', err);
      throw err;
    }
  };

  // set dark class for CSS (Tailwind/Shadcn standard)
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [theme]);

  // Save theme mode change to backend (per user) - only on theme change, NOT on remoteConfig change
  useEffect(() => {
    // Skip saving during initial load - wait until theme is loaded from server
    if (isInitialLoad || !user) return;
    
    const saveMode = async () => {
      try {
        await saveTheme({ mode: theme });
      } catch (err) {
        // Silently fail - theme is still applied locally
      }
    };
    saveMode();
  }, [theme, user]);

  // load remote config when user logs in (user-specific theme)
  useEffect(() => {
    let mounted = true;
    setIsInitialLoad(true);
    
    (async () => {
      try {
        // Only fetch theme if user is authenticated
        const token = localStorage.getItem('access_token');
        if (!token || !user) {
          // Reset to default when user logs out
          if (mounted) {
            setRemoteConfig(null);
            setTheme('light');
            setLoading(false);
            setIsInitialLoad(false);
          }
          return;
        }
        
        const cfg = await api.getTheme();
        if (!mounted) return;
        if (cfg && Object.keys(cfg).length > 0) {
          setRemoteConfig(cfg);
          
          // Use user's saved theme mode
          if ((cfg as any).mode) {
            setTheme((cfg as any).mode as ThemeMode);
          } else {
            setTheme('light'); // default
          }
          
          // Apply saved CSS variables if present
          if ((cfg as any).primaryColor) {
            const primaryHSL = hexToHSL((cfg as any).primaryColor);
            document.documentElement.style.setProperty('--primary', primaryHSL);
            document.documentElement.style.setProperty('--ring', primaryHSL);
          }
          if ((cfg as any).accentColor) {
            const accentHSL = hexToHSL((cfg as any).accentColor);
            document.documentElement.style.setProperty('--accent', accentHSL);
          }
        } else {
          // No saved theme - use defaults
          setRemoteConfig(null);
          setTheme('light');
        }
      } catch (err) {
        // backend may not have theme — use defaults
        if (mounted) {
          setRemoteConfig(null);
          setTheme('light');
        }
      } finally {
        if (mounted) {
          setLoading(false);
          setIsInitialLoad(false);
        }
      }
    })();
    return () => { mounted = false; };
  }, [user]);

  const setThemeMode = (m: ThemeMode) => setTheme(m);
  const toggle = () => setTheme((t) => (t === 'light' ? 'dark' : 'light'));

  const value: ThemeContextValue = {
    theme,
    setThemeMode,
    toggle,
    remoteConfig,
    saveTheme,
    loading,
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
