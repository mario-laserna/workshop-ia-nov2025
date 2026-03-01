import { fetchCompanies, fetchIndustries, fetchLocations } from "@/lib/api";
import CompanyFilters from "@/components/CompanyFilters";
import CompanyTable from "@/components/CompanyTable";
import Pagination from "@/components/Pagination";

interface PageProps {
  searchParams: Promise<{
    industry_id?: string;
    location_id?: string;
    page?: string;
  }>;
}

/**
 * Server Component — Top SaaS Dashboard.
 * Reads URL search params to apply filters and pagination,
 * fetches data in parallel from the backend, and renders the dashboard.
 */
export default async function Home({ searchParams }: PageProps) {
  const params = await searchParams;

  const industryId = params.industry_id
    ? Number(params.industry_id)
    : undefined;
  const locationId = params.location_id
    ? Number(params.location_id)
    : undefined;
  const page = params.page ? Number(params.page) : 1;

  const [companiesResponse, industries, locations] = await Promise.all([
    fetchCompanies({ industry_id: industryId, location_id: locationId, page }),
    fetchIndustries(),
    fetchLocations(),
  ]);

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 to-slate-800">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        {/* Header */}
        <header className="mb-8">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-600/20">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5 text-cyan-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-white">
              Top SaaS Dashboard
            </h1>
          </div>
          <p className="mt-2 text-sm text-slate-400">
            Analiza y compara las principales empresas SaaS por industria,
            ubicacion, inversion y valoracion.
          </p>
        </header>

        {/* Filters */}
        <section className="mb-6" aria-label="Filtros">
          <CompanyFilters industries={industries} locations={locations} />
        </section>

        {/* Table */}
        <section aria-label="Tabla de empresas">
          <CompanyTable companies={companiesResponse.items} />
        </section>

        {/* Pagination */}
        {companiesResponse.total_pages > 0 && (
          <Pagination
            page={companiesResponse.page}
            totalPages={companiesResponse.total_pages}
            total={companiesResponse.total}
          />
        )}
      </div>
    </div>
  );
}
