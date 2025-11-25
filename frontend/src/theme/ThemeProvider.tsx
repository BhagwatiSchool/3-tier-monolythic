// src/theme/ThemeProvider.tsx
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { api } from '@/lib/api';

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

const KEY = 'lovable_theme';
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
  const [theme, setTheme] = useState<ThemeMode>(() => {
    try {
      const s = localStorage.getItem(KEY);
      if (s) {
        const parsed = JSON.parse(s);
        return (parsed.mode as ThemeMode) || 'light';
      }
    } catch {}
    return 'light';
  });

  const [remoteConfig, setRemoteConfig] = useState<ThemeShape | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // set dark class for CSS (Tailwind/Shadcn standard)
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    // persist minimal shape
    try {
      localStorage.setItem(KEY, JSON.stringify({ mode: theme }));
    } catch {}
  }, [theme]);

  // load remote config on mount (if backend endpoint present)
  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const cfg = await api.getTheme();
        if (!mounted) return;
        if (cfg) {
          setRemoteConfig(cfg);
          // Only adopt remote mode if user has explicitly saved a preference
          // Otherwise keep local/default (light mode)
          const localPreference = localStorage.getItem(KEY);
          if (localPreference && (cfg as any).mode) {
            setTheme((cfg as any).mode as ThemeMode);
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
        }
      } catch (err) {
        // backend may not implement /api/theme — ignore silently
        // console.warn('getTheme failed', err);
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  const setThemeMode = (m: ThemeMode) => setTheme(m);
  const toggle = () => setTheme((t) => (t === 'light' ? 'dark' : 'light'));

  const saveTheme = async (cfg?: Partial<ThemeShape>) => {
    // merge with remote config
    const payload = { ...(remoteConfig || {}), ...(cfg || {}), mode: cfg?.mode || theme };
    try {
      await api.updateTheme(payload);
      setRemoteConfig(payload);
      // persist locally as well
      try { localStorage.setItem(KEY, JSON.stringify(payload)); } catch {}
    } catch (err) {
      // bubble up if needed or swallow
      console.error('saveTheme failed', err);
      throw err;
    }
  };

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
