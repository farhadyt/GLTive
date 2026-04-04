import { forwardRef, type TextareaHTMLAttributes } from "react";

interface TextAreaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  ({ label, error, id, className = "", ...props }, ref) => {
    const textareaId = id || label?.toLowerCase().replace(/\s+/g, "-");
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label
            htmlFor={textareaId}
            className="text-sm font-medium text-[var(--text-primary)]"
          >
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          rows={3}
          className={`w-full px-3 py-2 text-sm rounded-[var(--radius-md)] border bg-[var(--surface-card)] text-[var(--text-primary)] placeholder:text-[var(--text-muted)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] focus:border-transparent resize-y ${
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

TextArea.displayName = "TextArea";
