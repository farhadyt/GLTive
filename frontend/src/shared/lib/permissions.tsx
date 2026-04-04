import { type ReactNode } from "react";
import { useAuth } from "./auth";

export function usePermission(permissionCode: string): boolean {
  const { session } = useAuth();
  if (!session.isAuthenticated) return false;
  if (session.isPlatformAdmin) return true;
  if (session.isCompanyAdmin) return true;
  return session.permissions.includes(permissionCode);
}

export function CanAccess({
  permission,
  children,
  fallback = null,
}: {
  permission: string;
  children: ReactNode;
  fallback?: ReactNode;
}) {
  const allowed = usePermission(permission);
  return <>{allowed ? children : fallback}</>;
}
