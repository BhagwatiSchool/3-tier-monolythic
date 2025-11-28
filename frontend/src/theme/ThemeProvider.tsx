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
  // 🔴 यह बदलना है: Added to prevent mode-only saves from overwriting full theme config during initial load
  const [hasLoadedTheme, setHasLoadedTheme] = useState(false);

  // Define saveTheme early so it's available for useEffects
  // 🔴 यह बदलना है: Fixed merge logic to preserve colors when saving theme mode
  const saveTheme = async (cfg?: Partial<ThemeShape>) => {
    // merge with remote config - keep all user-specific settings
    const payload = { ...(remoteConfig || {}), ...(cfg || {}) };
    // 🔴 यह बदलना है: Priority logic to ensure mode is set correctly
    if (cfg?.mode) {
      payload.mode = cfg.mode;
    } else if (remoteConfig?.mode) {
      payload.mode = remoteConfig.mode;
    } else {
      payload.mode = theme;
    }
    console.log(`💾 Saving theme:`, payload);
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
  // 🔴 यह बदलना है: Added hasLoadedTheme check to prevent overwrites during initialization
  useEffect(() => {
    // Skip saving during initial load - wait until theme is loaded from server
    // Only save mode if we've successfully loaded a theme from backend
    if (!hasLoadedTheme || !user || isInitialLoad) return;
    
    const saveMode = async () => {
      try {
        await saveTheme({ mode: theme });
      } catch (err) {
        // Silently fail - theme is still applied locally
      }
    };
    saveMode();
  }, [theme, user, hasLoadedTheme, isInitialLoad]);

  // Apply CSS variables when remoteConfig changes
  useEffect(() => {
    if (remoteConfig) {
      // Apply primary color
      if ((remoteConfig as any).primaryColor) {
        const primaryHSL = hexToHSL((remoteConfig as any).primaryColor);
        document.documentElement.style.setProperty('--primary', primaryHSL);
        document.documentElement.style.setProperty('--ring', primaryHSL);
        console.log(`✅ Applied primary color: ${(remoteConfig as any).primaryColor} -> ${primaryHSL}`);
      }
      // Apply accent color
      if ((remoteConfig as any).accentColor) {
        const accentHSL = hexToHSL((remoteConfig as any).accentColor);
        document.documentElement.style.setProperty('--accent', accentHSL);
        console.log(`✅ Applied accent color: ${(remoteConfig as any).accentColor} -> ${accentHSL}`);
      }
    }
  }, [remoteConfig]);

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
            // Reset CSS variables to defaults
            document.documentElement.style.removeProperty('--primary');
            document.documentElement.style.removeProperty('--accent');
            document.documentElement.style.removeProperty('--ring');
            setLoading(false);
            setIsInitialLoad(false);
          }
          return;
        }
        
        console.log(`🔄 Loading theme for user ${user.id}...`);
        const cfg = await api.getTheme();
        if (!mounted) return;
        
        if (cfg && Object.keys(cfg).length > 0) {
          console.log(`✅ Theme loaded:`, cfg);
          setRemoteConfig(cfg);
          
          // Use user's saved theme mode
          if ((cfg as any).mode) {
            setTheme((cfg as any).mode as ThemeMode);
            console.log(`✅ Set theme mode: ${(cfg as any).mode}`);
          } else {
            setTheme('light');
          }
          
          // 🔴 यह बदलना है: Mark theme as loaded to enable mode-only saves
          setHasLoadedTheme(true);
        } else {
          // No saved theme - use defaults
          console.log(`ℹ️ No theme found, using defaults`);
          setRemoteConfig(null);
          setTheme('light');
          // 🔴 यह बदलना है: Mark as loaded even with no saved theme
          setHasLoadedTheme(true);
        }
      } catch (err) {
        console.error('❌ Failed to load theme:', err);
        // backend may not have theme — use defaults
        if (mounted) {
          setRemoteConfig(null);
          setTheme('light');
          // 🔴 यह बदलना है: Mark as loaded even on error to allow normal operation
          setHasLoadedTheme(true);
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
