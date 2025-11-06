/**
 * Health check response from backend API
 */
export interface HealthResponse {
  status: "healthy" | "unhealthy";
  version: string;
  environment: string;
  timestamp: string;
}
