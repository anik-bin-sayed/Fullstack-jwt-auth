"use client";

import React, { useState } from "react";
import Input from "./ui/Input";
import Link from "next/link";

interface LoginFormData {
  email: string;
  password: string;
  name: string;
}

const initialState = {
  email: "",
  password: "",
  name: "",
};
const RegisterForm = () => {
  const [formData, setFormData] = useState<LoginFormData>(initialState);

  const [errors, setErrors] = useState<Partial<LoginFormData>>({
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (errors[name as keyof LoginFormData]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<LoginFormData> = {};

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (validateForm()) {
      console.log("Form submitted:", formData);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl">
        <h1 className="text-3xl font-semibold mb-2 text-center text-black tracking-tighter">
          Welcome Back
        </h1>
        <p className="mb-8 text-center text-black tracking-tighter">
          Sign in to continue to your account
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Full Name"
            name="name"
            type="text"
            placeholder="your name"
            value={formData.name}
            onChange={handleChange}
            error={errors.email}
          />
          <Input
            label="Email"
            name="email"
            type="email"
            placeholder="you@example.com"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
          />
          <Input
            label="Password"
            name="password"
            type="password"
            placeholder="••••••••"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
          />

          <button
            type="submit"
            className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-xl transition-colors duration-200 cursor-pointer"
          >
            Sign Up
          </button>
          <p className="text-center text-sm">
            Already have an account?{" "}
            <Link
              href="/login"
              className="text-blue-600/80 hover:underline font-semibold"
            >
              Login here
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegisterForm;
