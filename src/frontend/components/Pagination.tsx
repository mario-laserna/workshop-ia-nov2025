"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";

interface PaginationProps {
  page: number;
  totalPages: number;
  total: number;
}

/**
 * Client Component that renders pagination controls.
 * Shows total records on the left and page navigation on the right.
 * Updates the `page` URL search param on navigation.
 */
export default function Pagination({
  page,
  totalPages,
  total,
}: PaginationProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const goToPage = useCallback(
    (newPage: number) => {
      const params = new URLSearchParams(searchParams.toString());

      if (newPage <= 1) {
        params.delete("page");
      } else {
        params.set("page", String(newPage));
      }

      router.push(`?${params.toString()}`);
    },
    [router, searchParams],
  );

  const isFirstPage = page <= 1;
  const isLastPage = page >= totalPages;

  return (
    <div className="flex items-center justify-between px-1 py-4">
      {/* Total records */}
      <p className="text-sm text-slate-400">
        <span className="font-medium text-slate-300">{total}</span> registros
        encontrados
      </p>

      {/* Page navigation */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => goToPage(page - 1)}
          disabled={isFirstPage}
          aria-label="Pagina anterior"
          className="rounded-md border border-slate-700 bg-slate-800 p-2 text-slate-400 transition-colors hover:border-slate-600 hover:text-slate-200 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:border-slate-700 disabled:hover:text-slate-400"
        >
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
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>

        <span className="text-sm text-slate-400">
          Pagina{" "}
          <span className="font-medium text-white">{page}</span> de{" "}
          <span className="font-medium text-white">{totalPages}</span>
        </span>

        <button
          onClick={() => goToPage(page + 1)}
          disabled={isLastPage}
          aria-label="Pagina siguiente"
          className="rounded-md border border-slate-700 bg-slate-800 p-2 text-slate-400 transition-colors hover:border-slate-600 hover:text-slate-200 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:border-slate-700 disabled:hover:text-slate-400"
        >
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
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}
