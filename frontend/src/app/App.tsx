import { RouterProvider } from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import { AuthProvider } from "@/shared/lib/auth";
import { router } from "./router";
import "@/i18n";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
        <Toaster
          position="bottom-right"
          containerStyle={{
            bottom: 24,
            right: 24,
          }}
          toastOptions={{
            duration: 4000,
            style: {
              background: "var(--surface-container-highest, #2d3449)",
              color: "var(--color-on-surface, #dae2fd)",
              border: "1px solid rgba(255,255,255,0.05)",
              borderRadius: "12px",
              boxShadow: "0 12px 32px rgba(0,0,0,0.25)",
              fontSize: "0.875rem",
              padding: "12px 16px",
              maxWidth: "380px",
            },
            success: {
              iconTheme: {
                primary: "#5de6ff",
                secondary: "#0b1326",
              },
            },
            error: {
              iconTheme: {
                primary: "#ffb4ab",
                secondary: "#0b1326",
              },
            },
          }}
        />
      </AuthProvider>
    </QueryClientProvider>
  );
}
