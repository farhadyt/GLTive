interface JwtClaims {
  user_id?: string;
  username?: string;
  company_id?: string | null;
  is_platform_admin?: boolean;
  is_company_admin?: boolean;
  permissions?: string[];
  exp?: number;
  [key: string]: unknown;
}

export function jwtDecode(token: string): JwtClaims {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return {};
    const payload = parts[1];
    const decoded = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(decoded) as JwtClaims;
  } catch {
    return {};
  }
}
