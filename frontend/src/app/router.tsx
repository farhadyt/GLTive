import { createBrowserRouter, Navigate } from "react-router";
import { lazy, Suspense } from "react";
import { AuthGuard, PublicGuard, PermissionGuard } from "./guards";
import { AppShell } from "@/shared/layouts/AppShell";
import { Spinner } from "@/shared/ui";
import { STOCK_PERMISSIONS } from "@/shared/config/permissions";

const LoginPage = lazy(() =>
  import("./LoginPage").then((m) => ({ default: m.LoginPage }))
);
const NotFoundPage = lazy(() =>
  import("./NotFoundPage").then((m) => ({ default: m.NotFoundPage }))
);
const AccessDeniedPage = lazy(() =>
  import("./AccessDeniedPage").then((m) => ({ default: m.AccessDeniedPage }))
);
const StockDashboardPage = lazy(() =>
  import("@/modules/stock/pages/StockDashboardPage").then((m) => ({
    default: m.StockDashboardPage,
  }))
);
const CategoriesPage = lazy(() =>
  import("@/modules/stock/pages/CategoriesPage").then((m) => ({
    default: m.CategoriesPage,
  }))
);
const StockItemsPage = lazy(() =>
  import("@/modules/stock/pages/StockItemsPage").then((m) => ({
    default: m.StockItemsPage,
  }))
);
const MovementsPage = lazy(() =>
  import("@/modules/stock/pages/MovementsPage").then((m) => ({
    default: m.MovementsPage,
  }))
);

function SuspenseWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[40vh]">
          <Spinner size="lg" />
        </div>
      }
    >
      {children}
    </Suspense>
  );
}

export const router = createBrowserRouter([
  // Public routes
  {
    element: <PublicGuard />,
    children: [
      {
        path: "/login",
        element: (
          <SuspenseWrapper>
            <LoginPage />
          </SuspenseWrapper>
        ),
      },
    ],
  },
  // Authenticated routes
  {
    element: <AuthGuard />,
    children: [
      {
        element: <AppShell />,
        children: [
          { index: true, element: <Navigate to="/stock" replace /> },
          // Stock module — permission-guarded
          {
            element: <PermissionGuard permission={STOCK_PERMISSIONS.VIEW} />,
            children: [
              {
                path: "/stock",
                element: (
                  <SuspenseWrapper>
                    <StockDashboardPage />
                  </SuspenseWrapper>
                ),
              },
              {
                path: "/stock/categories",
                element: (
                  <SuspenseWrapper>
                    <CategoriesPage />
                  </SuspenseWrapper>
                ),
              },
              {
                path: "/stock/items",
                element: (
                  <SuspenseWrapper>
                    <StockItemsPage />
                  </SuspenseWrapper>
                ),
              },
            ],
          },
          // Movement history — separate permission
          {
            element: (
              <PermissionGuard permission={STOCK_PERMISSIONS.HISTORY_VIEW} />
            ),
            children: [
              {
                path: "/stock/movements",
                element: (
                  <SuspenseWrapper>
                    <MovementsPage />
                  </SuspenseWrapper>
                ),
              },
            ],
          },
          // Utility routes
          {
            path: "/403",
            element: (
              <SuspenseWrapper>
                <AccessDeniedPage />
              </SuspenseWrapper>
            ),
          },
          {
            path: "*",
            element: (
              <SuspenseWrapper>
                <NotFoundPage />
              </SuspenseWrapper>
            ),
          },
        ],
      },
    ],
  },
]);
