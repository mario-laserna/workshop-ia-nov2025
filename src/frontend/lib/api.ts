import {
  CompanyListResponse,
  HealthResponse,
  Industry,
  Location,
} from "./types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Perform a GET request to the backend API with consistent error handling.
 * @param path - API path (e.g. "/api/v1/health")
 * @returns Parsed JSON response
 * @throws Error if request fails or response is not ok
 */
async function apiGet<T>(path: string): Promise<T> {
  const url = `${API_URL}${path}`;

  const response = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

/**
 * Fetch health status from backend API
 * @returns Promise with health response
 * @throws Error if request fails or response is invalid
 */
export async function fetchHealth(): Promise<HealthResponse> {
  try {
    return await apiGet<HealthResponse>("/api/v1/health");
  } catch (error) {
    throw new Error(
      `Failed to fetch health status: ${error instanceof Error ? error.message : "Unknown error"}`,
    );
  }
}

/** Optional filter/pagination params for fetching companies */
interface FetchCompaniesParams {
  industry_id?: number;
  location_id?: number;
  page?: number;
  size?: number;
}

/**
 * Fetch paginated list of companies with optional filters.
 * @param params - Optional industry_id, location_id, page, size
 * @returns Paginated company list response
 * @throws Error if request fails
 */
export async function fetchCompanies(
  params?: FetchCompaniesParams,
): Promise<CompanyListResponse> {
  const searchParams = new URLSearchParams();

  if (params?.industry_id != null) {
    searchParams.set("industry_id", String(params.industry_id));
  }
  if (params?.location_id != null) {
    searchParams.set("location_id", String(params.location_id));
  }
  if (params?.page != null) {
    searchParams.set("page", String(params.page));
  }
  if (params?.size != null) {
    searchParams.set("size", String(params.size));
  }

  const query = searchParams.toString();
  const path = `/api/v1/companies${query ? `?${query}` : ""}`;

  try {
    return await apiGet<CompanyListResponse>(path);
  } catch (error) {
    throw new Error(
      `Failed to fetch companies: ${error instanceof Error ? error.message : "Unknown error"}`,
    );
  }
}

/**
 * Fetch all industries.
 * @returns List of industries
 * @throws Error if request fails
 */
export async function fetchIndustries(): Promise<Industry[]> {
  try {
    return await apiGet<Industry[]>("/api/v1/industries");
  } catch (error) {
    throw new Error(
      `Failed to fetch industries: ${error instanceof Error ? error.message : "Unknown error"}`,
    );
  }
}

/**
 * Fetch all locations.
 * @returns List of locations
 * @throws Error if request fails
 */
export async function fetchLocations(): Promise<Location[]> {
  try {
    return await apiGet<Location[]>("/api/v1/locations");
  } catch (error) {
    throw new Error(
      `Failed to fetch locations: ${error instanceof Error ? error.message : "Unknown error"}`,
    );
  }
}
