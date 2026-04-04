import { forwardRef, type InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, id, className = "", ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, "-");
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-[var(--text-primary)]"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`w-full px-3 py-2 text-sm rounded-[var(--radius-md)] border bg-[var(--surface-card)] text-[var(--text-primary)] placeholder:text-[var(--text-muted)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] focus:border-transparent ${
            error
              ? "border-[var(--color-danger-500)]"
              : "border-[var(--border-default)]"
          } ${className}`}
          {...props}
        />
        {error && (
          <p className="text-xs text-[var(--color-danger-500)]">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";
