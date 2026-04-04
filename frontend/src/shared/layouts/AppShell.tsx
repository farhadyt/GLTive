import { Outlet } from "react-router";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

export function AppShell() {
  return (
    <div className="min-h-screen bg-[var(--surface)]">
      <Sidebar />
      <TopBar />
      <main className="pl-[240px] pt-[56px] min-h-screen">
        <div className="p-8 max-w-[1600px] mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
