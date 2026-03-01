"use client";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

/**
 * Error boundary for the dashboard page.
 * Displays a user-friendly error message with a retry button.
 */
export default function Error({ error, reset }: ErrorProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-linear-to-br from-slate-900 to-slate-800 px-4">
      <div className="max-w-md text-center">
        {/* Error icon */}
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-red-500/20">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8 text-red-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
        </div>

        <h2 className="mb-2 text-2xl font-bold text-white">
          Algo salio mal
        </h2>
        <p className="mb-6 text-slate-400">
          {error.message ||
            "Ocurrio un error inesperado al cargar el dashboard."}
        </p>

        <button
          onClick={reset}
          className="rounded-lg bg-cyan-600 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-slate-900"
        >
          Reintentar
        </button>
      </div>
    </div>
  );
}
