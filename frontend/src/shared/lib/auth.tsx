import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from "react";
import { apiClient, setAccessToken } from "./api-client";
import type { UserSession, AuthTokens } from "@/shared/types/api";
import { jwtDecode } from "./jwt-decode";

interface AuthContextValue {
  session: UserSession;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isLoading: boolean;
}

const EMPTY_SESSION: UserSession = {
  isAuthenticated: false,
  accessToken: null,
  refreshToken: null,
  companyId: null,
  isPlatformAdmin: false,
  isCompanyAdmin: false,
  username: null,
  permissions: [],
};

const AuthContext = createContext<AuthContextValue | null>(null);

function buildSession(access: string, refresh: string): UserSession {
  const claims = jwtDecode(access);
  return {
    isAuthenticated: true,
    accessToken: access,
    refreshToken: refresh,
    companyId: claims.company_id || null,
    isPlatformAdmin: claims.is_platform_admin || false,
    isCompanyAdmin: claims.is_company_admin || false,
    username: claims.username || claims.user_id || null,
    permissions: claims.permissions || [],
  };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<UserSession>(EMPTY_SESSION);
  const [isLoading, setIsLoading] = useState(false);

  const login = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await apiClient.post<{ success: boolean; data: AuthTokens }>(
        "/api/v1/auth/login/",
        { username, password }
      );
      const { access, refresh } = res.data.data;
      setAccessToken(access);
      const newSession = buildSession(access, refresh);
      setSession(newSession);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      if (session.refreshToken) {
        await apiClient.post("/api/v1/auth/logout/", {
          refresh: session.refreshToken,
        });
      }
    } catch {
      // Logout best-effort
    } finally {
      setAccessToken(null);
      setSession(EMPTY_SESSION);
    }
  }, [session.refreshToken]);

  // Clear tokens on unmount
  useEffect(() => {
    return () => setAccessToken(null);
  }, []);

  return (
    <AuthContext.Provider value={{ session, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
