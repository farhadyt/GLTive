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
const ReceivePage = lazy(() =>
  import("@/modules/stock/pages/ReceivePage").then((m) => ({
    default: m.ReceivePage,
  }))
);
const IssuePage = lazy(() =>
  import("@/modules/stock/pages/IssuePage").then((m) => ({
    default: m.IssuePage,
  }))
);
const TransferPage = lazy(() =>
  import("@/modules/stock/pages/TransferPage").then((m) => ({
    default: m.TransferPage,
  }))
);
const AdjustmentsPage = lazy(() =>
  import("@/modules/stock/pages/AdjustmentsPage").then((m) => ({
    default: m.AdjustmentsPage,
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
  {
    element: <AuthGuard />,
    children: [
      {
        element: <AppShell />,
        children: [
          { index: true, element: <Navigate to="/stock" replace /> },
          // Stock view routes
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
          // Stock operations — separate permissions
          {
            element: (
              <PermissionGuard permission={STOCK_PERMISSIONS.RECEIVE} />
            ),
            children: [
              {
                path: "/stock/receive",
                element: (
                  <SuspenseWrapper>
                    <ReceivePage />
                  </SuspenseWrapper>
                ),
              },
            ],
          },
          {
            element: (
              <PermissionGuard permission={STOCK_PERMISSIONS.ISSUE} />
            ),
            children: [
              {
                path: "/stock/issue",
                element: (
                  <SuspenseWrapper>
                    <IssuePage />
                  </SuspenseWrapper>
                ),
              },
            ],
          },
          {
            element: (
              <PermissionGuard permission={STOCK_PERMISSIONS.TRANSFER} />
            ),
            children: [
              {
                path: "/stock/transfer",
                element: (
                  <SuspenseWrapper>
                    <TransferPage />
                  </SuspenseWrapper>
                ),
              },
            ],
          },
          {
            element: (
              <PermissionGuard permission={STOCK_PERMISSIONS.ADJUST} />
            ),
            children: [
              {
                path: "/stock/adjustments",
                element: (
                  <SuspenseWrapper>
                    <AdjustmentsPage />
                  </SuspenseWrapper>
                ),
              },
            ],
          },
          // Movement history
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
          // Utility
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
