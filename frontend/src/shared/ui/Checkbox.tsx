import { forwardRef, type InputHTMLAttributes } from "react";

interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, id, className = "", ...props }, ref) => {
    const checkId = id || label?.toLowerCase().replace(/\s+/g, "-");
    return (
      <label
        htmlFor={checkId}
        className={`inline-flex items-center gap-2 cursor-pointer select-none ${className}`}
      >
        <input
          ref={ref}
          type="checkbox"
          id={checkId}
          className="w-4 h-4 rounded border-[var(--border-default)] text-[var(--color-primary-600)] focus:ring-[var(--color-primary-500)] bg-[var(--surface-card)]"
          {...props}
        />
        {label && (
          <span className="text-sm text-[var(--text-primary)]">{label}</span>
        )}
      </label>
    );
  }
);

Checkbox.displayName = "Checkbox";
