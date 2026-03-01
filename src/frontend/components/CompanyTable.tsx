import { Company } from "@/lib/types";

interface CompanyTableProps {
  companies: Company[];
}

/** Map of industry names to Tailwind badge color classes */
const INDUSTRY_COLORS: Record<string, string> = {
  Fintech: "bg-teal-600 text-teal-100",
  HealthTech: "bg-emerald-600 text-emerald-100",
  EdTech: "bg-green-600 text-green-100",
  CyberSecurity: "bg-cyan-600 text-cyan-100",
  "AI / ML": "bg-blue-600 text-blue-100",
  DevTools: "bg-indigo-600 text-indigo-100",
  MarTech: "bg-violet-600 text-violet-100",
  HRTech: "bg-orange-600 text-orange-100",
  CloudInfra: "bg-sky-600 text-sky-100",
  DataAnalytics: "bg-purple-600 text-purple-100",
};

const DEFAULT_BADGE_COLOR = "bg-slate-600 text-slate-100";

/**
 * Format a numeric value as a currency string ($X.XM or $X.XB).
 * Returns "—" for null/undefined values.
 */
function formatCurrency(value: number | null): string {
  if (value == null) return "—";

  const absValue = Math.abs(value);

  if (absValue >= 1_000_000_000) {
    const billions = value / 1_000_000_000;
    return `$${billions % 1 === 0 ? billions.toFixed(0) : billions.toFixed(1)}B`;
  }

  if (absValue >= 1_000_000) {
    const millions = value / 1_000_000;
    return `$${millions % 1 === 0 ? millions.toFixed(0) : millions.toFixed(1)}M`;
  }

  if (absValue >= 1_000) {
    const thousands = value / 1_000;
    return `$${thousands % 1 === 0 ? thousands.toFixed(0) : thousands.toFixed(1)}K`;
  }

  return `$${value}`;
}

/**
 * Server Component that renders a table of SaaS companies.
 * Displays company data with formatted currency and industry badges.
 */
export default function CompanyTable({ companies }: CompanyTableProps) {
  if (companies.length === 0) {
    return (
      <div className="rounded-lg border border-slate-700 bg-slate-800/50 px-6 py-16 text-center">
        <p className="text-lg text-slate-400">
          No se encontraron empresas con los filtros seleccionados.
        </p>
        <p className="mt-2 text-sm text-slate-500">
          Intenta cambiar o limpiar los filtros para ver resultados.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-700">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-slate-700 bg-slate-800/60">
            <th className="px-4 py-3 font-medium text-slate-400">Nombre</th>
            <th className="px-4 py-3 font-medium text-slate-400">Industria</th>
            <th className="px-4 py-3 font-medium text-slate-400">Ubicacion</th>
            <th className="px-4 py-3 font-medium text-slate-400">Productos</th>
            <th className="px-4 py-3 font-medium text-slate-400">Fundacion</th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Inversion Total
            </th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Ingresos Anuales
            </th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Valoracion
            </th>
          </tr>
        </thead>
        <tbody>
          {companies.map((company) => (
            <tr
              key={company.id}
              className="border-b border-slate-700/50 transition-colors hover:bg-slate-800/40"
            >
              <td className="px-4 py-3 font-medium text-white">
                {company.name}
              </td>
              <td className="px-4 py-3">
                <IndustryBadge name={company.industry} />
              </td>
              <td className="px-4 py-3 text-slate-300">{company.location}</td>
              <td className="px-4 py-3 text-slate-300">{company.products}</td>
              <td className="px-4 py-3 text-center text-slate-300">
                {company.founding_year ?? "—"}
              </td>
              <td className="px-4 py-3 text-right text-slate-200">
                {formatCurrency(company.total_funding)}
              </td>
              <td className="px-4 py-3 text-right font-medium text-emerald-400">
                {formatCurrency(company.arr)}
              </td>
              <td className="px-4 py-3 text-right text-slate-200">
                {formatCurrency(company.valuation)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** Renders a colored badge for an industry name */
function IndustryBadge({ name }: { name: string }) {
  const colorClasses = INDUSTRY_COLORS[name] ?? DEFAULT_BADGE_COLOR;

  return (
    <span
      className={`inline-block rounded px-2.5 py-0.5 text-xs font-medium ${colorClasses}`}
    >
      {name}
    </span>
  );
}
