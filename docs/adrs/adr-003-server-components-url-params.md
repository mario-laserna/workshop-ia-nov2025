# 3. Server Components + URL Search Params para data fetching en frontend

Fecha: Febrero 17 de 2026

## Status

Aceptada.

## Contexto

Se necesita definir la estrategia de fetching de datos y gestion del estado de filtros en el frontend Next.js. El dashboard permite filtrar empresas por industria, ubicacion y pagina, y se requiere que el estado de los filtros sea persistente y compartible via URL.

## Decision

Usamos React Server Components para el fetching de datos, con los filtros reflejados como URL search params (`?industry_id=1&location_id=2&page=1`).

- La pagina principal es un Server Component que lee `searchParams` y hace fetch directo al backend.
- Los componentes de filtros son Client Components que actualizan los search params via `useRouter()` y `useSearchParams()`.

Alternativas evaluadas:
- **Client Components con SWR/React Query**: mas JavaScript en cliente, estado de filtros en memoria (no compartible via URL).
- **Server Actions**: orientado a mutaciones, no ideal para queries de lectura con filtros.
- **API Routes intermedias**: capa adicional innecesaria entre frontend y backend.

## Consecuencias

- Menos JavaScript enviado al cliente al usar Server Components.
- URLs compartibles que preservan el estado completo de filtros y paginacion.
- Cada cambio de filtro genera un re-render desde el servidor.
