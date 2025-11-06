import { HealthResponse } from "./types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Fetch health status from backend API
 * @returns Promise with health response
 * @throws Error if request fails or response is invalid
 */
export async function fetchHealth(): Promise<HealthResponse> {
  const url = `${API_URL}/api/v1/health`;

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(
        `HTTP error! status: ${response.status}`,
      );
    }

    const data: HealthResponse = await response.json();
    return data;
  } catch (error) {
    throw new Error(
      `Failed to fetch health status: ${error instanceof Error ? error.message : "Unknown error"}`,
    );
  }
}
