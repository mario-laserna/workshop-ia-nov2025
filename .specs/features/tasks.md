# Lista de Tareas del Proyecto — Top SaaS Dashboard

Este documento desglosa el trabajo definido en `planning.md` en tareas accionables, organizadas por fases. Incluye tareas de diseño (ADRs, diagramas C4, modelo ER), desarrollo backend/frontend, pruebas unitarias y documentación.

---

## Fase 0: Diseño y Arquitectura

### ADRs (Architectural Decision Records)

Generar los 3 ADRs más relevantes del proyecto utilizando el template [adr_template_es.md](../../.specs/templates/adr_template_es.md) y guardar en `docs/adrs/`.

- [x] **ADR-001: Supabase Python async client para acceso a datos**
    - [x] Documentar contexto: necesidad de acceso a PostgreSQL hospedado en Supabase desde FastAPI; la base de datos ya existe y está poblada en Supabase
    - [x] Documentar decisión: uso de la librería oficial `supabase-py` con cliente async (`supabase._async.create_client`) para acceder a datos vía PostgREST
    - [x] Documentar alternativas evaluadas: SQLAlchemy async + asyncpg (acceso SQL directo), postgrest-py (cliente PostgREST sin SDK completo), raw HTTP a PostgREST
    - [x] Documentar consecuencias: sin necesidad de modelos ORM, queries vía API REST (PostgREST), requiere `SUPABASE_URL` + `SUPABASE_KEY`, menor complejidad de configuración, dependencia del servicio Supabase
    - [x] Guardar en `docs/adrs/adr-001-supabase-python-client.md`

- [x] **ADR-002: Arquitectura por capas (Router → Service → Repository)**
    - [x] Documentar contexto: necesidad de separar responsabilidades para mantenibilidad y testabilidad
    - [x] Documentar decisión: patrón de capas con inyección de dependencias vía `Depends()` de FastAPI
    - [x] Documentar alternativas evaluadas: lógica directa en routers, patrón CQRS, hexagonal architecture
    - [x] Documentar consecuencias: más archivos/boilerplate, clara separación de responsabilidades, facilidad de testing con mocks, escalabilidad del código
    - [x] Guardar en `docs/adrs/adr-002-arquitectura-por-capas.md`

- [x] **ADR-003: Server Components + URL Search Params para data fetching en frontend**
    - [x] Documentar contexto: estrategia de fetching de datos y gestión de estado de filtros en Next.js
    - [x] Documentar decisión: uso de React Server Components con filtros reflejados en URL search params
    - [x] Documentar alternativas evaluadas: Client Components con SWR/React Query, Server Actions, API Routes intermedias
    - [x] Documentar consecuencias: menos JavaScript en cliente, URLs compartibles con estado, re-render desde servidor en cada cambio de filtro
    - [x] Guardar en `docs/adrs/adr-003-server-components-url-params.md`

### Diagramas de Arquitectura C4 (MermaidJS)

- [x] **Diseñar diagrama C4 de Contexto del sistema**
    - [x] Identificar actor externo: Inversionista/Analista (usuario)
    - [x] Representar el sistema "Top SaaS Dashboard" como caja central (incluye Frontend, Backend y Base de datos Supabase dentro del boundary del sistema)
    - [x] Mostrar relaciones: usuario → sistema (consulta dashboard para evaluar métricas de empresas SaaS)
    - [x] Generar diagrama en MermaidJS
    - [x] Guardar en `docs/architecture/c4-context.md`

- [x] **Diseñar diagrama C4 de Contenedores del sistema**
    - [x] Identificar contenedores: Frontend (Next.js 16), Backend API (FastAPI), Base de datos (PostgreSQL/Supabase)
    - [x] Mostrar tecnologías de cada contenedor
    - [x] Mostrar protocolos de comunicación: HTTP/REST (frontend → backend), HTTP/PostgREST (backend → Supabase)
    - [x] La base de datos hace parte del límite del sistema
    - [x] Generar diagrama en MermaidJS
    - [x] Guardar en `docs/architecture/c4-containers.md`

### Diseño de Base de Datos (Modelo Entidad-Relación)

- [x] **Revisar modelo de datos existente**
    - [x] Analizar script `scripts/database/01-top-saas-db-creation.sql` para validar tablas, columnas y tipos de datos
    - [x] Verificar relaciones: `company.industry_id` → `industry.id` (many-to-one), `company.location_id` → `location.id` (many-to-one), `company_investor` (many-to-many entre company e investor)
    - [x] Verificar tipos de datos: `BIGSERIAL`, `TEXT`, `VARCHAR(255)`, `INTEGER`, `BIGINT`, `REAL`, `TIMESTAMPTZ`
    - [x] Verificar índices existentes: `idx_company_industry`, `idx_company_location`, `idx_company_investor_company`, `idx_company_investor_investor`
    - [x] Verificar triggers de auditoría (`update_updated_at_column`) en todas las tablas
    - [x] Documentar hallazgos y confirmar que no se requieren migraciones

- [x] **Diseñar diagrama Entidad-Relación (ER) en MermaidJS**
    - [x] Modelar entidad `company` con todas sus columnas y tipos
    - [x] Modelar entidad `industry` con columnas y constraint UNIQUE en name
    - [x] Modelar entidad `location` con columnas
    - [x] Modelar entidad `investor` con columnas y constraint UNIQUE en name
    - [x] Modelar tabla de asociación `company_investor` con PK compuesta
    - [x] Representar relaciones: company ||--o{ industry, company ||--o{ location, company }o--o{ investor (vía company_investor)
    - [x] Incluir campos de auditoría (`created_at`, `created_by`, `updated_at`, `updated_by`)
    - [x] Guardar en `docs/database/er-diagram.md`

### Documentación de Diagramas

- [x] **Documentar diagrama C4 de Contexto**
    - [x] Agregar descripción textual del diagrama
    - [x] Explicar actor externo (Inversionista/Analista) y el sistema (Top SaaS Dashboard que incluye Frontend, Backend y DB)
    - [x] Incluir diagrama MermaidJS renderizable en el markdown

- [x] **Documentar diagrama C4 de Contenedores**
    - [x] Agregar descripción textual de cada contenedor (Frontend Next.js, Backend FastAPI, PostgreSQL Supabase)
    - [x] Documentar responsabilidades de cada contenedor
    - [x] Documentar protocolos: HTTP/REST (frontend → backend), HTTP/PostgREST (backend → Supabase)
    - [x] Incluir diagrama MermaidJS renderizable en el markdown

- [x] **Documentar diagrama ER de base de datos**
    - [x] Agregar descripción textual del modelo de datos
    - [x] Documentar cardinalidad de cada relación
    - [x] Documentar convenciones de tipos de datos (BIGSERIAL para PKs, BIGINT para monetarios, TIMESTAMPTZ para auditoría)
    - [x] Incluir diagrama MermaidJS renderizable en el markdown

---

## Fase 1: Infraestructura del Backend (Cliente Supabase y Schemas)

### Dependencias

- [x] Instalar dependencias de producción del backend:
    - [x] `uv add supabase` — cliente oficial de Supabase para Python (incluye PostgREST)
    - [x] Verificar compatibilidad con Python 3.12+

### Supabase — Configuración del Cliente

- [x] Crear módulo de configuración del cliente Supabase (`src/backend/core/supabase_client.py`):
    - [x] Crear instancia async del cliente con `create_client` de `supabase._async`
    - [x] Configurar con `SUPABASE_URL` y `SUPABASE_KEY` desde Settings
    - [x] Implementar dependency `get_supabase` para inyección en FastAPI vía `Depends()`
    - [x] Agregar `SUPABASE_URL: str` y `SUPABASE_KEY: str` a la clase `Settings` existente en `main.py`

> **Nota**: No se crean modelos ORM. El acceso a datos se realiza vía el cliente Supabase (PostgREST). Los schemas Pydantic se usan para validar y tipar las respuestas.

### Schemas Pydantic (Request/Response)

- [x] Crear schema `IndustryRead` (`src/backend/schemas/industry.py`):
    - [x] Campos: `id: int`, `name: str`

- [x] Crear schema `LocationRead` (`src/backend/schemas/location.py`):
    - [x] Campos: `id: int`, `city: str`, `state: str | None`, `country: str`

- [x] Crear schema de paginación genérico (`src/backend/schemas/pagination.py`):
    - [x] `PaginatedResponse[T]` con campos: `items: list[T]`, `total: int`, `page: int`, `size: int`, `total_pages: int`

- [x] Crear schemas de company (`src/backend/schemas/company.py`):
    - [x] `CompanyRead`: `id`, `name`, `industry` (str), `location` (str formateado "City, Country"), `products`, `founding_year`, `total_funding`, `arr`, `valuation`
    - [x] `CompanyListResponse`: tipo alias para `PaginatedResponse[CompanyRead]`

---

## Fase 2: Backend — Endpoints de Catálogos (Industries, Locations)

### Industrias

- [x] Crear repositorio de industrias (`src/backend/repositories/industry_repository.py`):
    - [x] Método async `get_all(client: AsyncClient) -> list[dict]`: query vía `client.table("industry").select("*").order("name")` 

- [x] Crear servicio de industrias (`src/backend/services/industry_service.py`):
    - [x] Método async `get_all_industries(client: AsyncClient) -> list[IndustryRead]`: delega al repositorio y convierte a schemas Pydantic

- [x] Crear router de industrias (`src/backend/api/industries.py`):
    - [x] `GET /api/v1/industries` → `response_model=list[IndustryRead]`, `status_code=200`
    - [x] Inyectar cliente Supabase vía `Depends(get_supabase)`
    - [x] Registrar router en `main.py` con `prefix="/api/v1"` y `tags=["industries"]`

### Ubicaciones

- [x] Crear repositorio de ubicaciones (`src/backend/repositories/location_repository.py`):
    - [x] Método async `get_all(client: AsyncClient) -> list[dict]`: query vía `client.table("location").select("*").order("city")`

- [x] Crear servicio de ubicaciones (`src/backend/services/location_service.py`):
    - [x] Método async `get_all_locations(client: AsyncClient) -> list[LocationRead]`: delega al repositorio y convierte a schemas Pydantic

- [x] Crear router de ubicaciones (`src/backend/api/locations.py`):
    - [x] `GET /api/v1/locations` → `response_model=list[LocationRead]`, `status_code=200`
    - [x] Inyectar cliente Supabase vía `Depends(get_supabase)`
    - [x] Registrar router en `main.py` con `prefix="/api/v1"` y `tags=["locations"]`

---

## Fase 3: Backend — Endpoint de Empresas con Filtros y Paginación

### Repositorio de Empresas

- [x] Crear repositorio de empresas (`src/backend/repositories/company_repository.py`):
    - [x] Método async `get_all(client, industry_id?, location_id?, page, size) -> list[dict]`:
        - [x] Construir query base con `client.table("company").select("*, industry(name), location(city, state, country)")`
        - [x] Aplicar filtro `.eq("industry_id", industry_id)` si se provee
        - [x] Aplicar filtro `.eq("location_id", location_id)` si se provee
        - [x] Aplicar paginación offset-based con `.range(start, end)` donde `start = (page - 1) * size` y `end = start + size - 1`
    - [x] Método async `count(client, industry_id?, location_id?) -> int`:
        - [x] Query con `.select("*", count="exact", head=True)` con mismos filtros opcionales
        - [x] Retornar `count` de la respuesta para metadata de paginación

> **Nota**: El cliente Supabase (PostgREST) soporta queries con relaciones embebidas. Usar `select("*, industry(name), location(city, state, country)")` para obtener datos de tablas relacionadas en una sola llamada, evitando N+1.

### Servicio de Empresas

- [x] Crear servicio de empresas (`src/backend/services/company_service.py`):
    - [x] Método async `get_companies(client, industry_id?, location_id?, page, size) -> CompanyListResponse`:
        - [x] Llamar a `company_repository.get_all(...)` para obtener empresas
        - [x] Llamar a `company_repository.count(...)` para obtener total
        - [x] Calcular `total_pages = ceil(total / size)`
        - [x] Transformar datos crudos (dict) a `CompanyRead` schemas (formatear industry/location como strings)
        - [x] Construir y retornar `CompanyListResponse` con items, total, page, size, total_pages

### Router de Empresas

- [x] Crear router de empresas (`src/backend/api/companies.py`):
    - [x] `GET /api/v1/companies` con query params:
        - [x] `industry_id: int | None = Query(default=None)` — filtro opcional por industria
        - [x] `location_id: int | None = Query(default=None)` — filtro opcional por ubicación
        - [x] `page: int = Query(default=1, ge=1)` — número de página
        - [x] `size: int = Query(default=20, ge=1, le=100)` — elementos por página
    - [x] `response_model=CompanyListResponse`, `status_code=200`
    - [x] Inyectar cliente Supabase vía `Depends(get_supabase)`
    - [x] Registrar router en `main.py` con `prefix="/api/v1"` y `tags=["companies"]`

---

## Fase 4: Tests del Backend

### Configuración de Infraestructura de Tests

- [x] Instalar dependencias de testing:
    - [x] `uv add --dev pytest pytest-asyncio httpx`
- [x] Crear `src/backend/tests/conftest.py`:
    - [x] Fixture de `TestClient` con `httpx.AsyncClient` o FastAPI `TestClient`
    - [x] Fixture de mock del cliente Supabase (`AsyncMock`)
    - [x] Configurar override de dependency `get_supabase` para usar mocks
    - [x] Crear datos de prueba (factories/fixtures) para Company, Industry, Location como dicts (formato PostgREST)

### Tests de Endpoint de Industrias

- [x] Crear `src/backend/tests/api/test_industries.py`:
    - [x] Happy path: `GET /api/v1/industries` retorna lista de industrias con status 200
    - [x] Caso límite: retorna lista vacía `[]` cuando no hay industrias
    - [x] Verificar formato de respuesta: cada item tiene `id` (int) y `name` (str)

### Tests de Endpoint de Ubicaciones

- [x] Crear `src/backend/tests/api/test_locations.py`:
    - [x] Happy path: `GET /api/v1/locations` retorna lista de ubicaciones con status 200
    - [x] Caso límite: retorna lista vacía `[]` cuando no hay ubicaciones
    - [x] Verificar formato de respuesta: cada item tiene `id`, `city`, `state`, `country`

### Tests de Endpoint de Empresas

- [x] Crear `src/backend/tests/api/test_companies.py`:
    - [x] Happy path: `GET /api/v1/companies` retorna lista paginada con status 200
    - [x] Filtro por industria: `?industry_id=1` retorna solo empresas de esa industria
    - [x] Filtro por ubicación: `?location_id=1` retorna solo empresas de esa ubicación
    - [x] Filtros combinados: `?industry_id=1&location_id=2` retorna intersección
    - [x] Paginación: `?page=2&size=10` retorna segundo lote de resultados
    - [x] Caso límite: filtro sin resultados retorna `items: []` con `total: 0`
    - [x] Error de validación: `?page=0` o `?size=200` retorna status 422

### Tests de Servicios (Unit Tests)

- [x] Crear `src/backend/tests/services/test_company_service.py`:
    - [x] Test de cálculo correcto de `total_pages` (ej. 100 items, size 20 → 5 pages)
    - [x] Test de delegación correcta al repositorio con parámetros
    - [x] Test con total = 0 retorna response válida con 0 pages

- [x] Crear `src/backend/tests/services/test_industry_service.py`:
    - [x] Test de delegación al repositorio
    - [x] Test con lista vacía

- [x] Crear `src/backend/tests/services/test_location_service.py`:
    - [x] Test de delegación al repositorio
    - [x] Test con lista vacía

### Tests de Repositorios (Unit Tests)

- [x] Crear `src/backend/tests/repositories/test_company_repository.py`:
    - [x] Test de query sin filtros llama a `client.table("company").select(...)` sin `.eq()`
    - [x] Test de query con filtro `industry_id` verifica que se llama `.eq("industry_id", ...)` en el mock
    - [x] Test de query con filtro `location_id` verifica que se llama `.eq("location_id", ...)` en el mock
    - [x] Test de paginación: verifica `.range(start, end)` con valores correctos
    - [x] Test de `count()` verifica uso de `count="exact"` y `head=True`

- [x] Crear `src/backend/tests/repositories/test_industry_repository.py`:
    - [x] Test de `get_all()` verifica que se llama `.order("name")` en el mock

- [x] Crear `src/backend/tests/repositories/test_location_repository.py`:
    - [x] Test de `get_all()` verifica que se llama `.order("city")` en el mock

---

## Fase 5: Frontend — Tipos y API Client

### Tipos TypeScript

- [x] Extender tipos TypeScript (`src/frontend/lib/types.ts`):
    - [x] Interface `Company`: `id`, `name`, `industry` (string), `location` (string), `products`, `founding_year`, `total_funding`, `arr`, `valuation`
    - [x] Interface `Industry`: `id`, `name`
    - [x] Interface `Location`: `id`, `city`, `state` (nullable), `country`
    - [x] Interface genérica `PaginatedResponse<T>`: `items: T[]`, `total`, `page`, `size`, `total_pages`
    - [x] Type alias `CompanyListResponse = PaginatedResponse<Company>`

### API Client

- [x] Extender API client (`src/frontend/lib/api.ts`):
    - [x] Función `fetchCompanies(params?: { industry_id?, location_id?, page?, size? }): Promise<CompanyListResponse>`:
        - [x] Construir query string con parámetros opcionales
        - [x] Fetch a `GET /api/v1/companies?...`
        - [x] Manejo de errores HTTP consistente
    - [x] Función `fetchIndustries(): Promise<Industry[]>`:
        - [x] Fetch a `GET /api/v1/industries`
    - [x] Función `fetchLocations(): Promise<Location[]>`:
        - [x] Fetch a `GET /api/v1/locations`

---

## Fase 6: Frontend — Componentes y Dashboard

### Componentes

- [ ] Crear componente `CompanyFilters` (`src/frontend/components/CompanyFilters.tsx`):
    - [ ] Client Component (`'use client'`)
    - [ ] Props: `industries: Industry[]`, `locations: Location[]`
    - [ ] Dropdown de industria con opciones dinámicas
    - [ ] Dropdown de ubicación con opciones dinámicas
    - [ ] Al cambiar selección, actualizar URL search params vía `useRouter()` + `useSearchParams()`
    - [ ] Botón "Limpiar filtros" que resetea search params
    - [ ] Estilo con Tailwind CSS, tema oscuro (slate-900/800)

- [ ] Crear componente `CompanyTable` (`src/frontend/components/CompanyTable.tsx`):
    - [ ] Server Component (recibe datos como props)
    - [ ] Props: `companies: Company[]`
    - [ ] Formato tabular HTML (`<table>`) — no cards
    - [ ] Columnas: nombre, industria, ubicación, productos, año fundación, total inversión, ingresos anuales, valoración
    - [ ] Formateo de moneda: `$X.XM` / `$X.XB` para funding, ARR, valuation
    - [ ] Empty state: mensaje cuando `companies.length === 0`
    - [ ] Responsivo: `overflow-x-auto` para scroll horizontal en mobile
    - [ ] Estilo con Tailwind CSS, tema oscuro

- [ ] Crear componente `Pagination` (`src/frontend/components/Pagination.tsx`):
    - [ ] Client Component (`'use client'`)
    - [ ] Props: `page: number`, `totalPages: number`, `total: number`
    - [ ] Botón "Anterior" (disabled si page = 1)
    - [ ] Botón "Siguiente" (disabled si page = totalPages)
    - [ ] Indicador "Página X de Y"
    - [ ] Indicador total de registros
    - [ ] Actualiza `page` en URL search params

### Estados de la Página

- [ ] Crear loading state (`src/frontend/app/loading.tsx`):
    - [ ] Skeleton de tabla con placeholders animados (`animate-pulse`)
    - [ ] Placeholder para filtros y paginación
    - [ ] Estilo consistente con tema oscuro

- [ ] Crear error boundary (`src/frontend/app/error.tsx`):
    - [ ] Client Component (`'use client'`)
    - [ ] Mensaje de error claro
    - [ ] Botón "Reintentar" que llama a `reset()`
    - [ ] Estilo consistente con tema oscuro

### Página Principal

- [ ] Refactorizar página principal (`src/frontend/app/page.tsx`):
    - [ ] Convertir a Server Component (remover `'use client'`)
    - [ ] Leer `searchParams` de la URL: `industry_id`, `location_id`, `page`
    - [ ] Fetch paralelo con `Promise.all`: empresas + industrias + ubicaciones desde el backend
    - [ ] Componer layout: `CompanyFilters` + `CompanyTable` + `Pagination`
    - [ ] Mantener header con título "Top SaaS Dashboard"
    - [ ] Estilo con Tailwind CSS, tema oscuro (slate-900/800)

---

## Fase 7: Tests del Frontend

> **Nota**: De acuerdo con los requerimientos del prompt, las pruebas unitarias se generan solo para el backend (Fase 4). Las tareas de esta fase quedan documentadas como referencia para implementación futura si se decide extender el coverage al frontend.

### Configuración (Referencia)

- [ ] Instalar dependencias de testing frontend:
    - [ ] `npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom`
    - [ ] Configurar `vitest.config.ts` con environment `jsdom`
    - [ ] Crear setup file para testing-library

### Tests de API Client (Referencia)

- [ ] Tests de `fetchCompanies` con y sin filtros
- [ ] Tests de `fetchIndustries` y `fetchLocations`
- [ ] Tests de manejo de errores HTTP

### Tests de Componentes (Referencia)

- [ ] Tests de `CompanyTable`: renderizado, empty state, formato de moneda
- [ ] Tests de `CompanyFilters`: renderizado de dropdowns, actualización de search params
- [ ] Tests de `Pagination`: renderizado de controles, navegación entre páginas

---

## Fase 8: Integración y Verificación Final

### Verificación End-to-End

- [ ] Iniciar backend: `cd src/backend && uv run fastapi dev`
- [ ] Iniciar frontend: `cd src/frontend && npm run dev`
- [ ] Verificar que el dashboard carga empresas desde la base de datos
- [ ] Probar filtro por industria y verificar que la tabla se actualiza
- [ ] Probar filtro por ubicación y verificar que la tabla se actualiza
- [ ] Probar filtros combinados (industria + ubicación)
- [ ] Probar paginación: navegar entre páginas
- [ ] Verificar que URLs con filtros son compartibles (copiar URL y abrir en nueva pestaña)
- [ ] Verificar empty state cuando filtros no retornan resultados
- [ ] Verificar loading state durante la carga de datos

### Checks de Calidad — Backend

- [ ] `uv run ruff check .` — sin errores de linting
- [ ] `uv run ruff format --check .` — código formateado correctamente
- [ ] `uv run mypy .` — sin errores de tipos
- [ ] `uv run pytest` — todos los tests pasan
- [ ] Verificar coverage ≥ 60%

### Checks de Calidad — Frontend

- [ ] `npm run lint` — sin errores ESLint
- [ ] `npm run build` — build exitoso sin errores de TypeScript
- [ ] Verificar que no hay warnings críticos en consola del navegador

---

## Resumen de Entregables por Fase

| Fase | Categoría | Entregables |
|------|-----------|-------------|
| 0 | Diseño | 3 ADRs, diagrama C4 contexto, diagrama C4 contenedores, diagrama ER, documentación |
| 1 | Backend | Dependencia `supabase`, `core/supabase_client.py`, schemas Pydantic (4) |
| 2 | Backend | Repositorios, servicios y routers de industrias y ubicaciones |
| 3 | Backend | Repositorio, servicio y router de empresas con filtros y paginación |
| 4 | Testing | Infraestructura de tests, tests de endpoints, servicios y repositorios (backend) |
| 5 | Frontend | Tipos TypeScript extendidos, API client con 3 funciones de fetch |
| 6 | Frontend | 3 componentes (Filters, Table, Pagination), loading/error states, refactor page.tsx |
| 7 | Frontend | (Referencia) Configuración de tests, tests de API client y componentes |
| 8 | Integración | Verificación E2E, checks de calidad backend y frontend |

---

## Orden de Ejecución Sugerido

```
Fase 0 (Diseño)
    ↓
Fase 1 (Supabase Setup) → Fase 5 (Types + API Client)  ← pueden ejecutarse en paralelo
    ↓                       ↓
Fase 2 (Catálogos)   Fase 6 (Dashboard UI)
    ↓                       ↓
Fase 3 (Companies)          ↓
    ↓                       ↓
Fase 4 (Tests Backend)      ↓
    ↓                       ↓
    └──────── Fase 8 (Integración) ──────────┘
```

> **Nota**: Las fases 1-4 (backend) y 5-6 (frontend) pueden paralelizarse si hay dos desarrolladores. La Fase 0 debe completarse antes de iniciar desarrollo. La Fase 8 requiere que backend y frontend estén completos.
