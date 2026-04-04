export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data: T;
}

export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details: Record<string, unknown>;
    field_errors: Record<string, string[]>;
  };
}

export interface PaginatedData<T> {
  items: T[];
  pagination: {
    page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
  };
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface UserSession {
  isAuthenticated: boolean;
  accessToken: string | null;
  refreshToken: string | null;
  companyId: string | null;
  companyName: string | null;
  companyCode: string | null;
  isPlatformAdmin: boolean;
  isCompanyAdmin: boolean;
  username: string | null;
  role: string | null;
  permissions: string[];
}
