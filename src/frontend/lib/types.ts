/**
 * Health check response from backend API
 */
export interface HealthResponse {
  status: "healthy" | "unhealthy";
  version: string;
  environment: string;
  timestamp: string;
}

/**
 * Industry record from the backend API
 */
export interface Industry {
  id: number;
  name: string;
}

/**
 * Location record from the backend API
 */
export interface Location {
  id: number;
  city: string;
  state: string | null;
  country: string;
}

/**
 * Company record from the backend API
 */
export interface Company {
  id: number;
  name: string;
  industry: string;
  location: string;
  products: string;
  founding_year: number | null;
  total_funding: number | null;
  arr: number | null;
  valuation: number | null;
}

/**
 * Generic paginated response wrapper
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
}

/**
 * Paginated response of companies
 */
export type CompanyListResponse = PaginatedResponse<Company>;
