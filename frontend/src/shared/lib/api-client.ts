import axios from "axios";
import type { ApiError } from "@/shared/types/api";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  headers: { "Content-Type": "application/json" },
});

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

export function getAccessToken(): string | null {
  return accessToken;
}

apiClient.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response) {
      const data = error.response.data as ApiError;
      const message =
        data?.error?.message || error.response.statusText || "Request failed";
      return Promise.reject({
        status: error.response.status,
        code: data?.error?.code || "unknown_error",
        message,
        details: data?.error?.details || {},
        fieldErrors: data?.error?.field_errors || {},
      });
    }
    return Promise.reject({
      status: 0,
      code: "network_error",
      message: "Network error — please check your connection",
      details: {},
      fieldErrors: {},
    });
  }
);

export { apiClient };

export interface NormalizedError {
  status: number;
  code: string;
  message: string;
  details: Record<string, unknown>;
  fieldErrors: Record<string, string[]>;
}
