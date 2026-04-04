/**
 * Permission-Aware Rendering
 *
 * Current state:
 * - Backend JWT does NOT include role permission codes.
 * - Only is_platform_admin and is_company_admin are available from JWT.
 * - Therefore, usePermission() currently grants access to admin users only.
 * - Non-admin role-based users will see permission-gated content only after
 *   a backend /me endpoint or JWT permission claim extension is implemented.
 *
 * The hooks and components are structurally ready for fine-grained permissions.
 * Once session.permissions is populated from a real source, everything works.
 */
import { type ReactNode } from "react";
import { useAuth } from "./auth";

export function usePermission(permissionCode: string): boolean {
  const { session } = useAuth();
  if (!session.isAuthenticated) return false;
  // Admin bypass — grounded in real backend JWT claims
  if (session.isPlatformAdmin) return true;
  if (session.isCompanyAdmin) return true;
  // Fine-grained check — will activate when permissions are populated
  if (permissionCode && session.permissions.length > 0) {
    return session.permissions.includes(permissionCode);
  }
  // No permissions available and not admin — deny
  return false;
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
