interface SkeletonProps {
  variant?: "line" | "rect" | "circle";
  width?: string;
  height?: string;
  className?: string;
}

export function Skeleton({
  variant = "line",
  width,
  height,
  className = "",
}: SkeletonProps) {
  const base = "animate-pulse bg-[var(--color-neutral-200)] dark:bg-[var(--color-neutral-700)]";
  const variants = {
    line: `${base} h-4 rounded`,
    rect: `${base} rounded-[var(--radius-md)]`,
    circle: `${base} rounded-full`,
  };

  return (
    <div
      className={`${variants[variant]} ${className}`}
      style={{ width, height }}
    />
  );
}
