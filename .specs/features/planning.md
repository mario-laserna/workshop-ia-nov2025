# Descripción General

## Top SaaS Dashboard — Análisis de Empresas SaaS

Aplicación full-stack para análisis de las 100 empresas SaaS más importantes del mundo, dirigida a inversionistas que desean evaluar métricas clave como valoración, ingresos anuales, inversión total e industria.

### Problema que resuelve
Los inversionistas necesitan una forma rápida y visual de comparar métricas de empresas SaaS, filtrando por industria y ubicación geográfica para identificar oportunidades de inversión.

### Para quién es
- Inversionistas y analistas financieros interesados en el sector SaaS
- Equipos de venture capital evaluando portafolio de empresas tecnológicas
- Analistas de mercado que necesitan datos comparativos del ecosistema SaaS

### Por qué es valioso
- Centraliza datos de 100 empresas SaaS en una interfaz unificada
- Permite filtrado interactivo por industria y ubicación
- Presenta métricas financieras clave en un formato fácil de consumir
- Datos normalizados y estructurados a partir del dataset de Kaggle

### Componentes del sistema
| Componente | Tecnología | Ubicación |
|------------|-----------|-----------|
| Frontend | Next.js 16+, TypeScript, Tailwind CSS | `src/frontend/` |
| Backend | FastAPI, Python 3.12+, SQLAlchemy Async | `src/backend/` |
| Base de datos | PostgreSQL (Supabase) | Remota (Supabase) |

### Fuente de datos
- **Dataset**: [Top 100 SaaS Companies/Startups (Kaggle)](https://www.kaggle.com/datasets/shreyasdasari7/top-100-saas-companiesstartups)
- **Estado**: Base de datos creada y poblada (scripts en `scripts/database/`)

---

# Funcionalidades Principales

## F1: API REST de Empresas con Filtros

**Qué hace:** Endpoint que retorna el listado de empresas SaaS con soporte para filtros opcionales por industria y ubicación, con paginación offset-based.

**Por qué es importante:** Es el core de la aplicación; provee los datos que el frontend consume para mostrar el dashboard.

**Cómo funciona a alto nivel:**
1. El cliente envía una petición `GET /api/v1/companies` con query params opcionales (`industry_id`, `location_id`, `page`, `size`)
2. El router delega al servicio de empresas
3. El servicio aplica filtros y paginación vía el repositorio
4. El repositorio ejecuta queries async contra PostgreSQL usando SQLAlchemy
5. Se retorna una respuesta paginada con metadata (total, page, size, total_pages)

**Endpoint:** `GET /api/v1/companies`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `industry_id` | `int` | No | — | Filtrar por ID de industria |
| `location_id` | `int` | No | — | Filtrar por ID de ubicación |
| `page` | `int` | No | `1` | Número de página |
| `size` | `int` | No | `20` | Elementos por página (max: 100) |

**Response Schema (`CompanyListResponse`):**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Salesforce",
      "industry": "CRM",
      "location": "San Francisco, CA, USA",
      "products": "Sales Cloud, Service Cloud...",
      "founding_year": 1999,
      "total_funding": 65000000,
      "arr": 26490000000,
      "valuation": 200000000000
    }
  ],
  "total": 100,
  "page": 1,
  "size": 20,
  "total_pages": 5
}
```

## F2: API REST de Industrias

**Qué hace:** Endpoint que retorna el listado completo de industrias para poblar el filtro del frontend.

**Por qué es importante:** Necesario para que el dropdown de filtro por industria tenga las opciones disponibles.

**Cómo funciona a alto nivel:**
1. `GET /api/v1/industries` retorna todas las industrias ordenadas por nombre
2. Sin paginación (volumen bajo de registros)

**Endpoint:** `GET /api/v1/industries`

**Response Schema:**
```json
[
  { "id": 1, "name": "CRM" },
  { "id": 2, "name": "Cloud Computing" }
]
```

## F3: API REST de Ubicaciones

**Qué hace:** Endpoint que retorna el listado completo de ubicaciones para poblar el filtro del frontend.

**Por qué es importante:** Necesario para que el dropdown de filtro por ubicación tenga las opciones disponibles.

**Cómo funciona a alto nivel:**
1. `GET /api/v1/locations` retorna todas las ubicaciones ordenadas por ciudad
2. Sin paginación (volumen bajo de registros)

**Endpoint:** `GET /api/v1/locations`

**Response Schema:**
```json
[
  { "id": 1, "city": "San Francisco", "state": "CA", "country": "USA" }
]
```

## F4: Dashboard de Empresas SaaS (Frontend)

**Qué hace:** Página principal con tabla/listado de empresas SaaS mostrando métricas clave, con filtros por industria y ubicación.

**Por qué es importante:** Es la interfaz principal que los inversionistas usarán para explorar y comparar empresas.

**Cómo funciona a alto nivel:**
1. La página es un **Server Component** que lee search params de la URL
2. Realiza fetch directo al backend con los filtros aplicados
3. Renderiza una tabla con columnas: nombre, industria, ubicación, productos, año fundación, inversión total, ingresos anuales, valoración
4. Los filtros (dropdowns de industria y ubicación) son un **Client Component** que actualiza los URL search params
5. El cambio de URL params trigerea re-render del Server Component con nuevos datos
6. Incluye controles de paginación (anterior/siguiente, indicador de página)

**Campos visibles en el listado:**
| Campo | Fuente (DB) | Formato |
|-------|-------------|---------|
| Nombre empresa | `company.name` | Texto |
| Industria | `industry.name` | Texto |
| Ubicación | `location.city, location.country` | "City, Country" |
| Productos | `company.products` | Texto (puede truncarse) |
| Fecha de creación | `company.founding_year` | Año (número) |
| Total inversión | `company.total_funding` | Moneda formateada ($X.XB) |
| Ingresos anuales | `company.arr` | Moneda formateada ($X.XB) |
| Valoración | `company.valuation` | Moneda formateada ($X.XB) |

---

# Experiencia de Usuario

## Perfil de usuario
**Inversionista/Analista**: Profesional financiero que busca evaluar rápidamente métricas de empresas SaaS para tomar decisiones de inversión.

## Flujo principal de usuario

```
1. Usuario accede al dashboard (/)
     ↓
2. Ve el listado completo de empresas con métricas (página 1)
     ↓
3. Opcionalmente selecciona filtros:
   - Dropdown "Industria" → filtra por industria seleccionada
   - Dropdown "Ubicación" → filtra por ubicación seleccionada
     ↓
4. La tabla se actualiza mostrando solo empresas que cumplen filtros
     ↓
5. Navega entre páginas con controles de paginación
     ↓
6. Puede compartir URL con filtros aplicados (filtros en search params)
```

## Consideraciones UI/UX
- **Diseño oscuro** consistente con el tema actual (slate-900/800) — clase profesional para analistas
- **Tabla responsiva**: formato tabular exclusivamente, con scroll horizontal en mobile
- **Loading states**: skeleton loaders mientras se cargan datos del servidor
- **Empty states**: mensaje claro cuando no hay resultados para los filtros aplicados
- **Formato de moneda**: valores formateados (ej. "$26.5B" en lugar de "26490000000")
- **URLs compartibles**: filtros reflejados en URL search params para shareability
- **Filtros reseteables**: botón para limpiar filtros y volver al listado completo

---

# Arquitectura

## Arquitectura del Sistema

```
┌─────────────────────────────┐
│    Frontend (Next.js 16)    │
│    http://localhost:3000    │
│                             │
│  Server Components (fetch)  │
│  Client Components (filtros)│
└──────────┬──────────────────┘
           │ HTTP (fetch)
           ▼
┌─────────────────────────────┐
│    Backend (FastAPI)        │
│    http://localhost:8000    │
│                             │
│  Routers → Services →      │
│  Repositories → Models     │
└──────────┬──────────────────┘
           │ asyncpg (async)
           ▼
┌─────────────────────────────┐
│  PostgreSQL (Supabase)      │
│  Tablas: company, industry, │
│  location, investor,        │
│  company_investor           │
└─────────────────────────────┘
```

## Backend: Arquitectura por Capas

```
src/backend/
├── main.py                      # App FastAPI, settings, lifespan, CORS
├── api/                         # Capa de Routers
│   ├── health.py                # (existente) Health check
│   ├── companies.py             # Router de empresas
│   ├── industries.py            # Router de industrias
│   └── locations.py             # Router de ubicaciones
├── services/                    # Capa de Lógica de Negocio
│   ├── company_service.py       # Lógica de empresas (filtros, paginación)
│   ├── industry_service.py      # Lógica de industrias
│   └── location_service.py      # Lógica de ubicaciones
├── repositories/                # Capa de Acceso a Datos
│   ├── company_repository.py    # Queries de empresas (SQLAlchemy)
│   ├── industry_repository.py   # Queries de industrias
│   └── location_repository.py   # Queries de ubicaciones
├── models/                      # Modelos SQLAlchemy (ORM)
│   ├── base.py                  # Base declarativa, metadata
│   ├── company.py               # Modelo Company
│   ├── industry.py              # Modelo Industry
│   ├── location.py              # Modelo Location
│   ├── investor.py              # Modelo Investor
│   └── company_investor.py      # Tabla de asociación
├── schemas/                     # Schemas Pydantic (Request/Response)
│   ├── company.py               # CompanyRead, CompanyListResponse
│   ├── industry.py              # IndustryRead
│   ├── location.py              # LocationRead
│   └── pagination.py            # PaginatedResponse genérico
└── core/                        # Configuración central
    └── database.py              # Engine, SessionLocal, get_db dependency
```

**Flujo de una petición:**
```
GET /api/v1/companies?industry_id=1&page=1&size=20
    ↓
companies.py (Router) → valida query params con Pydantic
    ↓
company_service.py (Service) → aplica lógica de negocio
    ↓
company_repository.py (Repository) → construye query SQLAlchemy con filtros + paginación
    ↓
SQLAlchemy Async Session → ejecuta query contra PostgreSQL via asyncpg
    ↓
Response: CompanyListResponse (Pydantic schema)
```

## Frontend: Arquitectura por Capas

```
src/frontend/
├── app/
│   ├── layout.tsx               # Layout principal (metadata, fonts, navbar)
│   ├── page.tsx                 # Dashboard principal (Server Component)
│   ├── loading.tsx              # Loading state (skeleton)
│   └── error.tsx                # Error boundary
├── components/
│   ├── CompanyTable.tsx         # Tabla de empresas (Server Component)
│   ├── CompanyFilters.tsx       # Filtros industria/ubicación (Client Component)
│   ├── Pagination.tsx           # Controles de paginación (Client Component)
│   └── ui/                      # Componentes UI reutilizables
│       ├── Select.tsx           # Dropdown genérico
│       └── Badge.tsx            # Badge para tags
├── lib/
│   ├── api.ts                   # (existente + nuevas funciones) API client
│   └── types.ts                 # (existente + nuevos tipos) TypeScript interfaces
└── hooks/                       # (reservado para futuro uso)
```

**Flujo de renderizado:**
```
page.tsx (Server Component)
  → Lee searchParams: industry_id, location_id, page
  → Fetch directo al backend: GET /api/v1/companies?...
  → Fetch paralelo: GET /api/v1/industries, GET /api/v1/locations
  → Renderiza:
      ├── CompanyFilters (Client Component) ← industrias + ubicaciones
      ├── CompanyTable (Server Component) ← empresas
      └── Pagination (Client Component) ← metadata paginación
```

## Modelos de Datos (SQLAlchemy)

### Company
```python
class Company(Base):
    __tablename__ = "company"
    id: Mapped[int]                    # BIGSERIAL PK
    name: Mapped[str]                  # TEXT NOT NULL
    products: Mapped[str | None]       # TEXT
    founding_year: Mapped[int | None]  # INTEGER
    total_funding: Mapped[int | None]  # BIGINT
    arr: Mapped[int | None]            # BIGINT (Annual Recurring Revenue)
    valuation: Mapped[int | None]      # BIGINT
    employees: Mapped[int | None]      # INTEGER
    g2_rating: Mapped[float | None]    # REAL
    industry_id: Mapped[int | None]    # FK → industry.id
    location_id: Mapped[int | None]    # FK → location.id
    # Relationships
    industry: Mapped["Industry"]       # many-to-one
    location: Mapped["Location"]       # many-to-one
    investors: Mapped[list["Investor"]]# many-to-many via company_investor
```

### Industry
```python
class Industry(Base):
    __tablename__ = "industry"
    id: Mapped[int]            # BIGSERIAL PK
    name: Mapped[str]          # VARCHAR(255) UNIQUE
```

### Location
```python
class Location(Base):
    __tablename__ = "location"
    id: Mapped[int]                # BIGSERIAL PK
    city: Mapped[str]              # TEXT NOT NULL
    state: Mapped[str | None]      # TEXT
    country: Mapped[str]           # TEXT NOT NULL
```

### Investor
```python
class Investor(Base):
    __tablename__ = "investor"
    id: Mapped[int]            # BIGSERIAL PK
    name: Mapped[str]          # VARCHAR(255) UNIQUE
```

## Decisiones Arquitectónicas

### DA-1: SQLAlchemy Async + asyncpg para acceso a datos
- **Decisión**: Usar SQLAlchemy en modo async con driver `asyncpg`
- **Justificación**: Aprovecha el modelo async nativo de FastAPI, mejor throughput bajo concurrencia
- **Trade-offs**: Mayor complejidad en configuración vs rendimiento óptimo
- **Alternativa descartada**: SQLAlchemy sync + psycopg2 — bloquearía el event loop de FastAPI

### DA-2: Server Components + URL Search Params para data fetching
- **Decisión**: Usar Server Components de Next.js con filtros via URL search params
- **Justificación**: Menos JavaScript en el cliente, URLs compartibles con estado de filtros, mejor performance inicial
- **Trade-offs**: Cada cambio de filtro re-renderiza desde el servidor vs interactividad más limitada
- **Alternativa descartada**: Client Components con SWR — más interactivo pero más JS en cliente y sin URLs compartibles nativamente

### DA-3: Paginación offset-based (page/size)
- **Decisión**: Implementar paginación con `page` y `size` como query params
- **Justificación**: Simple, intuitivo, suficiente para 100 registros, fácil de integrar con UI de páginas numeradas
- **Trade-offs**: Menos eficiente en datasets muy grandes vs simplicidad
- **Alternativa descartada**: Cursor-based — overkill para el volumen actual del dataset

### DA-4: Arquitectura por capas (Router → Service → Repository)
- **Decisión**: Separar en capas claras con inyección de dependencias
- **Justificación**: Mantenibilidad, testabilidad, separación de responsabilidades (requerimiento del repo)
- **Trade-offs**: Más archivos y boilerplate vs claridad y facilidad de testing
- **Alternativa descartada**: Lógica directa en routers — más rápido inicialmente pero imposible de mantener/escalar

### DA-5: Configuración de conexión a Supabase via variables de entorno
- **Decisión**: URL de conexión a DB en variable de entorno `DATABASE_URL` gestionada con `pydantic-settings`
- **Justificación**: Seguridad (no commitear credenciales), consistente con la configuración existente en `main.py`
- **Alternativa descartada**: Hardcodear connection string — inseguro y difícil de gestionar entre entornos

---

# Hoja de Ruta de Desarrollo

## Fase 1: Infraestructura del Backend (Capa de Datos)

**Alcance**: Configurar la conexión a base de datos y crear los modelos ORM.

### Tareas:
1. **Instalar dependencias del backend**
   - Agregar `sqlalchemy[asyncio]`, `asyncpg` al proyecto con `uv add`
   - Verificar compatibilidad con Python 3.12+

2. **Crear módulo de configuración de base de datos** (`core/database.py`)
   - Configurar `AsyncEngine` con `create_async_engine`
   - Crear `async_sessionmaker` para sesiones async
   - Implementar dependency `get_db` para inyección en FastAPI
   - Agregar `DATABASE_URL` a la clase `Settings` existente en `main.py`

3. **Crear modelos SQLAlchemy** (`models/`)
   - `base.py`: `DeclarativeBase` con campos de auditoría comunes (`created_at`, `updated_at`)
   - `industry.py`: Modelo `Industry`
   - `location.py`: Modelo `Location`
   - `investor.py`: Modelo `Investor`
   - `company.py`: Modelo `Company` con relaciones (industry, location, investors)
   - `company_investor.py`: Tabla de asociación many-to-many

4. **Crear schemas Pydantic** (`schemas/`)
   - `industry.py`: `IndustryRead`
   - `location.py`: `LocationRead`
   - `company.py`: `CompanyRead`, `CompanyListResponse`
   - `pagination.py`: `PaginatedResponse` genérico con campos `total`, `page`, `size`, `total_pages`

## Fase 2: Backend — Endpoints de Catálogos (Industries, Locations)

**Alcance**: Implementar endpoints simples de lectura para alimentar los filtros del frontend.

### Tareas:
5. **Crear repositorio de industrias** (`repositories/industry_repository.py`)
   - Método `get_all()`: retorna todas las industrias ordenadas por nombre

6. **Crear servicio de industrias** (`services/industry_service.py`)
   - Método `get_all_industries()`: delega al repositorio

7. **Crear router de industrias** (`api/industries.py`)
   - `GET /api/v1/industries` → retorna lista de `IndustryRead`
   - Registrar router en `main.py`

8. **Crear repositorio de ubicaciones** (`repositories/location_repository.py`)
   - Método `get_all()`: retorna todas las ubicaciones ordenadas por ciudad

9. **Crear servicio de ubicaciones** (`services/location_service.py`)
   - Método `get_all_locations()`: delega al repositorio

10. **Crear router de ubicaciones** (`api/locations.py`)
    - `GET /api/v1/locations` → retorna lista de `LocationRead`
    - Registrar router en `main.py`

## Fase 3: Backend — Endpoint de Empresas con Filtros y Paginación

**Alcance**: Implementar el endpoint principal de empresas con filtrado y paginación.

### Tareas:
11. **Crear repositorio de empresas** (`repositories/company_repository.py`)
    - Método `get_all(industry_id?, location_id?, page, size)`: query con filtros opcionales, joins para industry/location, paginación offset-based
    - Método `count(industry_id?, location_id?)`: contar total de resultados para metadata de paginación
    - Usar `selectinload` para relaciones (evitar N+1)

12. **Crear servicio de empresas** (`services/company_service.py`)
    - Método `get_companies(industry_id?, location_id?, page, size)`: orquesta repositorio, calcula `total_pages`, retorna `CompanyListResponse`

13. **Crear router de empresas** (`api/companies.py`)
    - `GET /api/v1/companies` con query params: `industry_id`, `location_id`, `page`, `size`
    - Validación de params con Pydantic (`Query`)
    - Response model: `CompanyListResponse`
    - Registrar router en `main.py`

## Fase 4: Tests del Backend

**Alcance**: Crear tests unitarios y de integración para los endpoints.

### Tareas:
14. **Configurar infraestructura de tests**
    - Instalar `pytest`, `pytest-asyncio`, `httpx` como dependencias de dev
    - Crear `conftest.py` con fixture de `TestClient` y mock de DB session
    - Configurar test database (SQLite async in-memory o mocks)

15. **Tests de endpoints de industrias**
    - Happy path: retorna lista de industrias
    - Caso límite: lista vacía
    - Verificar formato de respuesta

16. **Tests de endpoints de ubicaciones**
    - Happy path: retorna lista de ubicaciones
    - Caso límite: lista vacía
    - Verificar formato de respuesta

17. **Tests de endpoint de empresas**
    - Happy path: retorna lista paginada de empresas
    - Filtro por industria: retorna solo empresas de esa industria
    - Filtro por ubicación: retorna solo empresas de esa ubicación
    - Filtros combinados: industria + ubicación
    - Paginación: page=2 retorna segundo lote
    - Caso límite: filtro sin resultados retorna lista vacía con total=0
    - Error: page/size inválidos retorna 422

## Fase 5: Frontend — Tipos y API Client

**Alcance**: Crear los tipos TypeScript y funciones de fetch para consumir la API.

### Tareas:
18. **Extender tipos TypeScript** (`lib/types.ts`)
    - `Company`: interface con todos los campos del listado
    - `Industry`: interface con id y name
    - `Location`: interface con id, city, state, country
    - `PaginatedResponse<T>`: genérico con items, total, page, size, total_pages
    - `CompanyListResponse`: `PaginatedResponse<Company>`

19. **Extender API client** (`lib/api.ts`)
    - `fetchCompanies(params)`: fetch con query params (industria, ubicación, paginación)
    - `fetchIndustries()`: fetch de todas las industrias
    - `fetchLocations()`: fetch de todas las ubicaciones
    - Manejo de errores consistente

## Fase 6: Frontend — Componentes y Dashboard

**Alcance**: Implementar la UI del dashboard con tabla, filtros y paginación.

### Tareas:
20. **Crear componente `CompanyFilters`** (`components/CompanyFilters.tsx`)
    - Client Component (`'use client'`)
    - Dos dropdowns: industria y ubicación
    - Recibe industrias y ubicaciones como props
    - Al cambiar selección, actualiza URL search params via `useRouter` + `useSearchParams`
    - Botón "Limpiar filtros"

21. **Crear componente `CompanyTable`** (`components/CompanyTable.tsx`)
    - Server Component (recibe datos como props)
    - Formato tabular exclusivamente (tabla HTML `<table>`) — no usar cards ni otros layouts
    - Columnas: nombre, industria, ubicación, productos, año, funding, ARR, valoración
    - Formateo de moneda ($X.XM / $X.XB)
    - Empty state cuando no hay resultados
    - Diseño responsivo: scroll horizontal (`overflow-x-auto`) en pantallas pequeñas

22. **Crear componente `Pagination`** (`components/Pagination.tsx`)
    - Client Component
    - Botones anterior/siguiente
    - Indicador "Página X de Y"
    - Indicador total de registros
    - Actualiza `page` en URL search params

23. **Crear loading state** (`app/loading.tsx`)
    - Skeleton de la tabla con placeholders animados

24. **Crear error boundary** (`app/error.tsx`)
    - Client Component con mensaje de error y botón de reintentar

25. **Refactorizar página principal** (`app/page.tsx`)
    - Convertir a Server Component (remover `'use client'`)
    - Leer `searchParams` de la URL (industria, ubicación, página)
    - Fetch paralelo: empresas + industrias + ubicaciones desde el backend
    - Componer: `CompanyFilters` + `CompanyTable` + `Pagination`
    - Mantener header con título del dashboard

## Fase 7: Tests del Frontend

**Alcance**: Crear tests unitarios para componentes y funciones.

### Tareas:
26. **Configurar infraestructura de tests frontend**
    - Instalar Vitest + React Testing Library + jsdom
    - Configurar `vitest.config.ts`
    - Crear setup file para testing-library

27. **Tests de API client** (`lib/api.ts`)
    - Mock de fetch global
    - Test de `fetchCompanies` con y sin filtros
    - Test de `fetchIndustries` y `fetchLocations`
    - Test de manejo de errores HTTP

28. **Tests de componentes**
    - `CompanyTable`: renderiza datos, muestra empty state, formato de moneda
    - `CompanyFilters`: renderiza dropdowns, selección actualiza search params
    - `Pagination`: renderiza controles, navegación entre páginas

## Fase 8: Integración y Verificación Final

**Alcance**: Verificar que todo funciona end-to-end y que los checks de calidad pasan.

### Tareas:
29. **Verificación end-to-end**
    - Iniciar backend (`uv run fastapi dev`) y frontend (`npm run dev`)
    - Verificar que el dashboard carga empresas
    - Probar filtros y paginación
    - Verificar URLs compartibles

30. **Checks de calidad — Backend**
    - `uv run ruff check .` — sin errores de linting
    - `uv run ruff format --check .` — código formateado
    - `uv run mypy .` — sin errores de tipos
    - `uv run pytest` — todos los tests pasan

31. **Checks de calidad — Frontend**
    - `npm run lint` — sin errores ESLint
    - `npm run build` — build exitoso sin errores de TypeScript
    - `npm test` — todos los tests pasan

---

# Riesgos y Mitigaciones

## R1: Conexión a Supabase desde desarrollo local
- **Riesgo**: La URL de conexión requiere SSL y puede tener restricciones de IP
- **Mitigación**: Usar connection string de Supabase con `?sslmode=require` en `DATABASE_URL`. Verificar que no haya restricciones de IP en el panel de Supabase. Documentar configuración en README.

## R2: Performance de queries con JOINs
- **Riesgo**: Queries con JOINs a industry, location e investors podrían ser lentas
- **Mitigación**: Ya existen índices en `company.industry_id` y `company.location_id`. Usar `selectinload` para relaciones. Con 100 registros el impacto es mínimo.

## R3: Variables de entorno no configuradas
- **Riesgo**: El backend falla al iniciar si `DATABASE_URL` no está configurada
- **Mitigación**: Implementar validación con `pydantic-settings` que falle rápido con mensaje claro. Documentar `.env.example` con las variables requeridas.

## R4: Compatibilidad de tipos entre Python y TypeScript
- **Riesgo**: Valores `BIGINT` de PostgreSQL podrían exceder `Number.MAX_SAFE_INTEGER` en JavaScript
- **Mitigación**: Los valores del dataset (valuaciones en miles de millones) están dentro del rango seguro de JavaScript. Monitorear y considerar serialización como string si es necesario.

## R5: Cambios en el esquema de base de datos
- **Riesgo**: El esquema de la DB ya está creado y poblado; los modelos SQLAlchemy deben reflejar exactamente las tablas existentes
- **Mitigación**: Crear modelos ORM basados estrictamente en `01-top-saas-db-creation.sql`. No usar migraciones automáticas de SQLAlchemy (Alembic) en esta fase. Verificar con queries manuales.

## Versión inicial (MVP)
La versión 1.0 incluye:
- ✅ API REST con 3 endpoints (companies, industries, locations)
- ✅ Paginación offset-based en listado de empresas
- ✅ Filtros por industria y ubicación
- ✅ Dashboard frontend con tabla, filtros y paginación
- ✅ Tests unitarios para backend y frontend (≥60% coverage)
- ✅ Documentación OpenAPI automática

**No incluye (futuro):**
- ❌ Autenticación/autorización de usuarios
- ❌ Detalle individual de empresa (página dedicada)
- ❌ Gráficos/visualizaciones (charts, treemaps)
- ❌ Exportación de datos (CSV, PDF)
- ❌ Búsqueda por texto libre
- ❌ Ordenamiento dinámico de columnas

---

# Apéndice

## A1: Esquema de Base de Datos Existente

Referencia: `scripts/database/01-top-saas-db-creation.sql`

**Tablas:**
| Tabla | Descripción | Registros estimados |
|-------|-------------|-------------------|
| `company` | Empresas SaaS principales | ~100 |
| `industry` | Industrias/categorías normalizadas | ~20-30 |
| `location` | Ubicaciones (city, state, country) | ~50-60 |
| `investor` | Inversores normalizados | ~100-200 |
| `company_investor` | Relación many-to-many empresa↔inversor | ~300-500 |

**Campos de auditoría en todas las tablas**: `created_at`, `created_by`, `updated_at`, `updated_by`

**Triggers**: `update_updated_at_column()` actualiza automáticamente `updated_at` en todas las tablas.

## A2: Dependencias a Instalar

### Backend (Python)
```bash
# Producción
uv add sqlalchemy[asyncio] asyncpg

# Desarrollo
uv add --dev pytest pytest-asyncio httpx
```

### Frontend (TypeScript)
```bash
# Desarrollo (testing)
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

## A3: Variables de Entorno Requeridas

### Backend (`.env`)
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname?sslmode=require
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## A4: Orden de Implementación Sugerido

```
Fase 1 → Fase 2 → Fase 3 → Fase 4 → Fase 5 → Fase 6 → Fase 7 → Fase 8
  DB       APIs     Empresas  Tests    Types    UI       Tests    Verif.
 Setup    Catálogo  +Filtros  Backend  +Client  Dash     Frontend  E2E
```

Las fases 1-4 (backend) y 5-7 (frontend) pueden paralelizarse si hay dos desarrolladores. La fase 8 requiere que ambos estén completos.

## A5: Preguntas Resueltas

| # | Pregunta | Decisión | Justificación |
|---|----------|----------|---------------|
| 1 | Estrategia de conexión a DB | SQLAlchemy Async + asyncpg | Aprovecha async nativo de FastAPI |
| 2 | Estrategia de fetching frontend | Server Components + URL params | Menos JS, URLs compartibles, mejor performance inicial |
| 3 | Tipo de paginación | Offset-based (page/size) | Simple, intuitivo, suficiente para 100 registros |
