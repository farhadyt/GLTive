import axios from "axios";
import type { ApiError } from "@/shared/types/api";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  headers: { "Content-Type": "application/json" },
});

let accessToken: string | null = null;
let refreshToken: string | null = null;
let logoutCallback: (() => void) | null = null;
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}> = [];

export function setAccessToken(token: string | null) {
  accessToken = token;
}

export function setRefreshToken(token: string | null) {
  refreshToken = token;
}

export function setLogoutCallback(cb: (() => void) | null) {
  logoutCallback = cb;
}

function processQueue(error: unknown, token: string | null) {
  failedQueue.forEach((p) => {
    if (token) p.resolve(token);
    else p.reject(error);
  });
  failedQueue = [];
}

apiClient.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // 401 handling with refresh attempt
    if (
      axios.isAxiosError(error) &&
      error.response?.status === 401 &&
      !originalRequest._retry &&
      refreshToken
    ) {
      if (isRefreshing) {
        // Queue requests while refreshing
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: (token: string) => {
              originalRequest.headers.Authorization = `Bearer ${token}`;
              resolve(apiClient(originalRequest));
            },
            reject,
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const res = await axios.post(
          `${apiClient.defaults.baseURL}/api/v1/auth/refresh/`,
          { refresh: refreshToken },
          { headers: { "Content-Type": "application/json" } }
        );
        const newAccess = res.data?.data?.access;
        if (newAccess) {
          setAccessToken(newAccess);
          processQueue(null, newAccess);
          originalRequest.headers.Authorization = `Bearer ${newAccess}`;
          return apiClient(originalRequest);
        }
      } catch {
        processQueue(error, null);
        // Refresh failed — force logout
        setAccessToken(null);
        setRefreshToken(null);
        if (logoutCallback) logoutCallback();
        return Promise.reject(error);
      } finally {
        isRefreshing = false;
      }
    }

    // Normalize error response
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
