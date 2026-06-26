"use client";

import { forwardRef } from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  containerClassName?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      icon,
      rightIcon,
      className = "",
      containerClassName = "",
      ...props
    },
    ref,
  ) => {
    return (
      <div className={`w-full ${containerClassName}`}>
        {label && (
          <label className="block text-sm font-medium text-black mb-1.5">
            {label}
          </label>
        )}

        <div className="relative group">
          {icon && (
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-purple-400 transition-colors">
              {icon}
            </div>
          )}

          <input
            ref={ref}
            className={`w-full bg-white/5 border border-black/10 rounded-xl px-5 py-3.5 text-black 
                       placeholder-gray-500 focus:outline-none focus:border-purple-500 
                       transition-all duration-200
                       ${icon ? "pl-11" : ""} 
                       ${rightIcon ? "pr-11" : ""} 
                       ${error ? "border-red-500 focus:border-red-500" : ""}
                       ${className}`}
            {...props}
          />

          {rightIcon && (
            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400">
              {rightIcon}
            </div>
          )}
        </div>

        {error && <p className="mt-1.5 text-sm text-red-400">{error}</p>}
      </div>
    );
  },
);

Input.displayName = "Input";

export default Input;
