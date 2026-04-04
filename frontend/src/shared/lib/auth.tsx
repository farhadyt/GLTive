/**
 * Auth Foundation
 *
 * Session model:
 * - Tokens stored in-memory only (not localStorage) for security.
 * - Hard browser reload clears session — user must re-login.
 * - 401 responses trigger a silent refresh attempt via the API client.
 *
 * Permission model:
 * - After login, /me endpoint is called to fetch real user permissions.
 * - session.permissions is populated from backend role.permissions.
 * - Admin bypass (platform_admin / company_admin) still works independently.
 */
import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from "react";
import {
  apiClient,
  setAccessToken,
  setRefreshToken,
  setLogoutCallback,
} from "./api-client";
import type { UserSession, AuthTokens } from "@/shared/types/api";

interface MeResponse {
  id: string;
  username: string;
  email: string;
  is_platform_admin: boolean;
  is_company_admin: boolean;
  company: { id: string; name: string; code: string } | null;
  role: string | null;
  permissions: string[];
}

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
  companyName: null,
  companyCode: null,
  isPlatformAdmin: false,
  isCompanyAdmin: false,
  username: null,
  role: null,
  permissions: [],
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<UserSession>(EMPTY_SESSION);
  const [isLoading, setIsLoading] = useState(false);

  const clearSession = useCallback(() => {
    setAccessToken(null);
    setRefreshToken(null);
    setSession(EMPTY_SESSION);
  }, []);

  useEffect(() => {
    setLogoutCallback(clearSession);
    return () => setLogoutCallback(null);
  }, [clearSession]);

  const login = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    try {
      // 1. Get tokens
      const res = await apiClient.post<{ success: boolean; data: AuthTokens }>(
        "/api/v1/auth/login/",
        { username, password }
      );
      const { access, refresh } = res.data.data;
      setAccessToken(access);
      setRefreshToken(refresh);

      // 2. Fetch real user info + permissions from /me
      const meRes = await apiClient.get<{ success: boolean; data: MeResponse }>(
        "/api/v1/auth/me/"
      );
      const me = meRes.data.data;

      setSession({
        isAuthenticated: true,
        accessToken: access,
        refreshToken: refresh,
        companyId: me.company?.id || null,
        companyName: me.company?.name || null,
        companyCode: me.company?.code || null,
        isPlatformAdmin: me.is_platform_admin,
        isCompanyAdmin: me.is_company_admin,
        username: me.username,
        role: me.role,
        permissions: me.permissions,
      });
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
      // best-effort
    } finally {
      clearSession();
    }
  }, [session.refreshToken, clearSession]);

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
