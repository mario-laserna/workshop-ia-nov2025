/**
 * Loading skeleton displayed while the dashboard page data is being fetched.
 * Matches the dark theme layout with animated pulse placeholders.
 */
export default function Loading() {
  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 to-slate-800">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        {/* Header skeleton */}
        <div className="mb-8">
          <div className="mb-2 h-8 w-64 animate-pulse rounded bg-slate-700" />
          <div className="h-4 w-96 animate-pulse rounded bg-slate-700/60" />
        </div>

        {/* Filters skeleton */}
        <div className="mb-6 flex gap-3">
          <div className="h-10 w-52 animate-pulse rounded-lg bg-slate-800" />
          <div className="h-10 w-52 animate-pulse rounded-lg bg-slate-800" />
        </div>

        {/* Table skeleton */}
        <div className="overflow-hidden rounded-lg border border-slate-700">
          {/* Header row */}
          <div className="flex gap-4 border-b border-slate-700 bg-slate-800/60 px-4 py-3">
            {Array.from({ length: 8 }).map((_, i) => (
              <div
                key={i}
                className="h-4 flex-1 animate-pulse rounded bg-slate-700/60"
              />
            ))}
          </div>

          {/* Data rows */}
          {Array.from({ length: 8 }).map((_, rowIdx) => (
            <div
              key={rowIdx}
              className="flex gap-4 border-b border-slate-700/50 px-4 py-4"
            >
              {Array.from({ length: 8 }).map((_, colIdx) => (
                <div
                  key={colIdx}
                  className="h-4 flex-1 animate-pulse rounded bg-slate-700/40"
                  style={{ animationDelay: `${(rowIdx * 8 + colIdx) * 30}ms` }}
                />
              ))}
            </div>
          ))}
        </div>

        {/* Pagination skeleton */}
        <div className="mt-4 flex items-center justify-between px-1">
          <div className="h-4 w-40 animate-pulse rounded bg-slate-700/40" />
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 animate-pulse rounded-md bg-slate-800" />
            <div className="h-4 w-28 animate-pulse rounded bg-slate-700/40" />
            <div className="h-8 w-8 animate-pulse rounded-md bg-slate-800" />
          </div>
        </div>
      </div>
    </div>
  );
}
