import { Navigate, Outlet } from "react-router";
import { useAuth } from "@/shared/lib/auth";
import { usePermission } from "@/shared/lib/permissions";
import { Spinner } from "@/shared/ui";

export function AuthGuard() {
  const { session, isLoading } = useAuth();
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Spinner size="lg" />
      </div>
    );
  }
  if (!session.isAuthenticated) return <Navigate to="/login" replace />;
  return <Outlet />;
}

export function PublicGuard() {
  const { session } = useAuth();
  if (session.isAuthenticated) return <Navigate to="/" replace />;
  return <Outlet />;
}

export function PermissionGuard({ permission }: { permission: string }) {
  const hasPermission = usePermission(permission);
  if (!hasPermission) return <Navigate to="/403" replace />;
  return <Outlet />;
}
