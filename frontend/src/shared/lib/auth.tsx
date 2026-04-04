/**
 * Auth Foundation
 *
 * Session model:
 * - Tokens stored in-memory only (not localStorage) for security.
 * - Hard browser reload clears session — user must re-login. This is
 *   intentional for the current platform stage.
 * - 401 responses trigger a silent refresh attempt via the API client
 *   interceptor. If refresh fails, user is redirected to login.
 *
 * Permission model:
 * - Backend JWT currently includes: company_id, is_platform_admin, is_company_admin.
 * - Backend does NOT include role permissions in JWT claims.
 * - Therefore, fine-grained permission checks for non-admin users are NOT
 *   yet active. Only admin bypass (platform_admin / company_admin) works.
 * - When a /me or session endpoint is added to backend, permissions will
 *   be fetched from there and populated into session.permissions.
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
    // Backend does not currently include permissions in JWT.
    // This array will be populated when a /me endpoint or similar is available.
    permissions: [],
  };
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<UserSession>(EMPTY_SESSION);
  const [isLoading, setIsLoading] = useState(false);

  const clearSession = useCallback(() => {
    setAccessToken(null);
    setRefreshToken(null);
    setSession(EMPTY_SESSION);
  }, []);

  // Register logout callback so API client can force logout on refresh failure
  useEffect(() => {
    setLogoutCallback(clearSession);
    return () => setLogoutCallback(null);
  }, [clearSession]);

  const login = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await apiClient.post<{ success: boolean; data: AuthTokens }>(
        "/api/v1/auth/login/",
        { username, password }
      );
      const { access, refresh } = res.data.data;
      setAccessToken(access);
      setRefreshToken(refresh);
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
      // Logout is best-effort — always clear local state
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
