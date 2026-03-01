"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";
import { Industry, Location } from "@/lib/types";

interface CompanyFiltersProps {
  industries: Industry[];
  locations: Location[];
}

/**
 * Client Component that renders industry and location filter dropdowns.
 * Updates URL search params on change so the Server Component page re-fetches data.
 */
export default function CompanyFilters({
  industries,
  locations,
}: CompanyFiltersProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const currentIndustryId = searchParams.get("industry_id") ?? "";
  const currentLocationId = searchParams.get("location_id") ?? "";

  const updateParams = useCallback(
    (key: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString());

      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }

      // Reset to page 1 when filters change
      params.delete("page");

      router.push(`?${params.toString()}`);
    },
    [router, searchParams],
  );

  const handleIndustryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateParams("industry_id", e.target.value);
  };

  const handleLocationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateParams("location_id", e.target.value);
  };

  const handleClearFilters = () => {
    router.push("/");
  };

  const hasActiveFilters = currentIndustryId || currentLocationId;

  return (
    <div className="flex flex-wrap items-center gap-3">
      {/* Industry filter */}
      <div className="relative">
        <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
            />
          </svg>
        </span>
        <select
          value={currentIndustryId}
          onChange={handleIndustryChange}
          aria-label="Filtrar por industria"
          className="appearance-none rounded-lg border border-slate-700 bg-slate-800 py-2 pl-9 pr-8 text-sm text-slate-200 transition-colors hover:border-slate-600 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
        >
          <option value="">Todas las industrias</option>
          {industries.map((industry) => (
            <option key={industry.id} value={industry.id}>
              {industry.name}
            </option>
          ))}
        </select>
        <span className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 text-slate-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </span>
      </div>

      {/* Location filter */}
      <div className="relative">
        <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
        </span>
        <select
          value={currentLocationId}
          onChange={handleLocationChange}
          aria-label="Filtrar por ubicacion"
          className="appearance-none rounded-lg border border-slate-700 bg-slate-800 py-2 pl-9 pr-8 text-sm text-slate-200 transition-colors hover:border-slate-600 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
        >
          <option value="">Todas las ubicaciones</option>
          {locations.map((location) => (
            <option key={location.id} value={location.id}>
              {location.city}, {location.country}
            </option>
          ))}
        </select>
        <span className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 text-slate-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </span>
      </div>

      {/* Clear filters button */}
      {hasActiveFilters && (
        <button
          onClick={handleClearFilters}
          className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm text-slate-400 transition-colors hover:border-slate-600 hover:text-slate-200"
        >
          Limpiar filtros
        </button>
      )}
    </div>
  );
}
