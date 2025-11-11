# Descripción General

## Problema que Resuelve
Los inversionistas y analistas financieros necesitan evaluar rápidamente el panorama de empresas SaaS líderes en el mercado para identificar oportunidades de inversión, analizar tendencias de industria y comparar métricas de rendimiento entre competidores. Actualmente, esta información está dispersa en múltiples fuentes y no existe una herramienta centralizada que permita visualizar y filtrar datos de las top 100 empresas SaaS de manera eficiente.

## Solución Propuesta
Una aplicación web full-stack que proporciona un dashboard interactivo con visualización de métricas clave de las 100 principales empresas SaaS del mundo. La plataforma permite:
- Consultar información detallada de empresas (financiamiento, valoración, ingresos, productos)
- Filtrar empresas por industria y ubicación geográfica
- Visualizar relaciones entre empresas e inversores
- Acceder a métricas normalizadas y comparables

## Audiencia Objetivo
- **Inversionistas venture capital**: Buscan identificar patrones de inversión y oportunidades en el sector SaaS
- **Analistas financieros**: Necesitan comparar métricas de rendimiento entre empresas del mismo sector
- **Emprendedores SaaS**: Quieren entender el panorama competitivo y benchmarks de la industria
- **Investigadores de mercado**: Analizan tendencias geográficas y sectoriales en el ecosistema SaaS

## Valor Diferencial
- **Datos normalizados y estructurados**: Información de Kaggle procesada en una base de datos relacional optimizada
- **Acceso instantáneo**: Sin necesidad de procesar datasets o hacer consultas complejas
- **Filtrado inteligente**: Búsqueda por múltiples dimensiones (industria, ubicación) en tiempo real
- **Visión completa**: Relación empresas-inversores visible en una sola vista
- **Base técnica sólida**: Arquitectura escalable preparada para crecer con más datos y funcionalidades

## Stack Tecnológico
- **Frontend**: Next.js 16+ (App Router) con TypeScript y Tailwind CSS
- **Backend**: FastAPI con Python 3.12+, SQLAlchemy async
- **Base de datos**: PostgreSQL en Supabase (normalizada, con datos ya cargados)
- **Gestión de paquetes**: `uv` para Python, `npm` para Node.js

---

# Funcionalidades Principales

## 1. Listado de Empresas con Métricas Clave

### Qué hace
Presenta una vista tabular o de cards con todas las empresas SaaS del dataset, mostrando información completa de cada una:
- **Identificación**: Nombre de la empresa
- **Clasificación**: Industria/categoría
- **Geografía**: Ciudad y país (ubicación)
- **Oferta**: Productos y servicios
- **Historia**: Año de fundación
- **Métricas financieras**:
  - Total de financiamiento recibido
  - Ingresos anuales recurrentes (ARR)
  - Valoración actual de la empresa
- **Inversores**: Lista de inversores asociados (cargados mediante eager loading)

### Por qué es importante
- **Es el core de la aplicación**: Proporciona acceso directo a toda la información del dataset
- **Contexto completo**: Los inversionistas necesitan ver múltiples métricas simultáneamente para tomar decisiones
- **Comparación visual**: Permite identificar rápidamente empresas destacadas por su valoración, funding o crecimiento
- **Base para análisis**: Todos los demás features (filtros, búsquedas) operan sobre este listado

### Cómo funciona a alto nivel

**Backend**:
1. Endpoint `GET /api/v1/companies` que consulta la tabla `company` con joins a `industry`, `location` e `investor`
2. SQLAlchemy realiza eager loading usando `selectinload()` o `joinedload()` para traer inversores en la misma query
3. Pydantic schemas validan y estructuran la respuesta:
   - `CompanyRead`: schema principal con todos los campos
   - `IndustryRead`: schema anidado para industria
   - `LocationRead`: schema anidado para ubicación
   - `InvestorRead`: lista anidada de inversores
4. Retorna JSON con estructura:
   ```json
   {
     "data": [
       {
         "id": 1,
         "name": "Salesforce",
         "industry": { "id": 1, "name": "CRM" },
         "location": { "id": 1, "city": "San Francisco", "country": "USA" },
         "products": "Customer 360, Sales Cloud, Service Cloud",
         "founding_year": 1999,
         "total_funding": 150000000,
         "arr": 31000000000,
         "valuation": 200000000000,
         "investors": [
           { "id": 1, "name": "Sequoia Capital" },
           { "id": 2, "name": "Accel Partners" }
         ]
       }
     ],
     "total": 100
   }
   ```

**Frontend**:
1. Server Component o Client Component con `useSWR` hace fetch a `/api/v1/companies`
2. Recibe datos completos (empresas + inversores) en una sola llamada
3. Renderiza componente `CompanyList` que mapea cada empresa a un `CompanyCard`
4. `CompanyCard` muestra todos los campos con formateo client-side:
   - Números financieros formateados con `Intl.NumberFormat` (e.g., "$150M", "$31B")
   - Fechas formateadas
   - Lista de inversores como badges o tags
5. Implementa estado de loading skeleton mientras carga datos
6. Maneja errores con UI apropiada (error boundary)

**Decisiones técnicas aplicadas**:
- ✅ **Eager loading**: Inversores vienen anidados, evitando N+1 queries
- ✅ **Sin paginación**: Las 100 empresas se cargan completas (payload ~50-100KB)
- ✅ **Valores raw**: Backend envía números sin formatear, frontend aplica `formatCurrency()`

---

## 2. Filtro por Industria

### Qué hace
Permite filtrar el listado de empresas seleccionando una o múltiples industrias desde un dropdown o conjunto de checkboxes. Solo se muestran empresas que pertenecen a las industrias seleccionadas.

### Por qué es importante
- **Segmentación de mercado**: Los inversionistas suelen especializarse en sectores específicos (e.g., FinTech, HealthTech, Martech)
- **Comparación sectorial**: Facilita análisis de competidores directos dentro de la misma vertical
- **Reducción de ruido**: Permite enfocarse solo en las categorías relevantes para el análisis actual
- **Insights de tendencias**: Identificar qué industrias tienen más empresas unicornio o mayor valoración promedio

### Cómo funciona a alto nivel

**Backend**:

1. **Endpoint de catálogo**: `GET /api/v1/industries`
   - Consulta tabla `industry` para obtener todas las industrias únicas
   - Retorna lista simple:
     ```json
     {
       "data": [
         { "id": 1, "name": "CRM" },
         { "id": 2, "name": "Marketing Automation" },
         { "id": 3, "name": "Collaboration" }
       ]
     }
     ```

2. **Modificación de endpoint principal**: `GET /api/v1/companies?industry_id=1,2`
   - Acepta query param `industry_id` (uno o múltiples valores separados por coma)
   - SQLAlchemy agrega filtro condicional:
     ```python
     if industry_ids:
         query = query.filter(Company.industry_id.in_(industry_ids))
     ```
   - Retorna solo empresas que coincidan con los filtros

**Frontend**:

1. **Componente `IndustryFilter`**:
   - Hace fetch a `/api/v1/industries` al montar para obtener opciones
   - Renderiza dropdown multi-select (usando Headless UI o Radix)
   - Mantiene estado local de industrias seleccionadas

2. **Sincronización con query params**:
   - Al seleccionar industrias, actualiza URL: `?industry_id=1,2`
   - Usa `useSearchParams` (Next.js) para leer/escribir query params
   - El cambio en URL triggerea re-fetch de empresas con nuevos filtros

3. **Integración con listado**:
   - `CompanyList` lee `industry_id` desde query params
   - Pasa filtros a la llamada de API
   - SWR cachea resultados por combinación de filtros

**Flujo completo**:
```
Usuario selecciona "CRM" 
  → Estado actualiza: selectedIndustries = [1]
  → URL cambia: /?industry_id=1
  → useSWR detecta cambio de key
  → Fetch: GET /api/v1/companies?industry_id=1
  → Backend filtra empresas
  → Frontend renderiza solo empresas CRM
```

---

## 3. Filtro por Ubicación

### Qué hace
Permite filtrar el listado de empresas seleccionando ubicaciones geográficas (ciudad/país) desde un dropdown o campo de búsqueda. Solo se muestran empresas ubicadas en las locaciones seleccionadas.

### Por qué es importante
- **Análisis geográfico**: Identificar hubs de innovación SaaS (Silicon Valley, Tel Aviv, Londres)
- **Oportunidades regionales**: Inversionistas enfocados en mercados específicos (LATAM, Asia, Europa)
- **Ventajas regulatorias**: Algunas regiones ofrecen beneficios fiscales o marcos legales favorables
- **Diversificación de portfolio**: Balancear inversiones entre diferentes geografías

### Cómo funciona a alto nivel

**Backend**:

1. **Endpoint de catálogo**: `GET /api/v1/locations`
   - Consulta tabla `location` para obtener todas las ubicaciones únicas
   - Retorna lista con agrupación opcional por país:
     ```json
     {
       "data": [
         { "id": 1, "city": "San Francisco", "state": "CA", "country": "USA" },
         { "id": 2, "city": "New York", "state": "NY", "country": "USA" },
         { "id": 3, "city": "London", "state": null, "country": "UK" }
       ]
     }
     ```

2. **Modificación de endpoint principal**: `GET /api/v1/companies?location_id=1,2`
   - Acepta query param `location_id` (uno o múltiples valores)
   - SQLAlchemy agrega filtro condicional:
     ```python
     if location_ids:
         query = query.filter(Company.location_id.in_(location_ids))
     ```
   - Retorna solo empresas que coincidan con los filtros

**Frontend**:

1. **Componente `LocationFilter`**:
   - Hace fetch a `/api/v1/locations` al montar
   - Renderiza dropdown con agrupación por país (e.g., usando `optgroup` o acordeón)
   - Formato de display: "San Francisco, USA" o "London, UK"
   - Mantiene estado local de ubicaciones seleccionadas

2. **Sincronización con query params**:
   - Al seleccionar ubicaciones, actualiza URL: `?location_id=1,3`
   - Usa `useSearchParams` para gestionar query params
   - Cambio en URL triggerea re-fetch automático

3. **Combinación con otros filtros**:
   - Permite aplicar filtro de industria y ubicación simultáneamente
   - URL: `?industry_id=1,2&location_id=1,3`
   - Backend aplica ambos filtros con AND lógico

**Flujo completo**:
```
Usuario selecciona "San Francisco, USA" 
  → Estado actualiza: selectedLocations = [1]
  → URL cambia: /?location_id=1
  → useSWR detecta cambio de key
  → Fetch: GET /api/v1/companies?location_id=1
  → Backend filtra empresas
  → Frontend renderiza solo empresas de San Francisco
```

**Mejoras UX**:
- Búsqueda type-ahead para filtrar ubicaciones rápidamente
- Contador de empresas por ubicación (e.g., "San Francisco (25)")
- Icono de bandera por país para reconocimiento visual
- Botón "Clear filters" para resetear todas las selecciones

---

## 4. Combinación de Filtros (Funcionalidad Transversal)

### Qué hace
Permite aplicar múltiples filtros simultáneamente (industria + ubicación) para refinar la búsqueda. Los filtros funcionan con lógica AND: mostrar solo empresas que cumplan TODOS los criterios seleccionados.

### Por qué es importante
- **Búsquedas específicas**: Encontrar "empresas de CRM en San Francisco" o "FinTech en London"
- **Análisis de nicho**: Identificar competencia directa en segmentos muy específicos
- **Flexibilidad analítica**: Combinar dimensiones para explorar correlaciones (e.g., "¿Qué industrias dominan en cada región?")

### Cómo funciona a alto nivel

**Backend**:
- Endpoint `GET /api/v1/companies?industry_id=1,2&location_id=3`
- SQLAlchemy construye query dinámicamente aplicando todos los filtros presentes:
  ```python
  query = select(Company)
  if industry_ids:
      query = query.filter(Company.industry_id.in_(industry_ids))
  if location_ids:
      query = query.filter(Company.location_id.in_(location_ids))
  ```
- Retorna solo empresas que cumplan ambas condiciones

**Frontend**:
- Ambos filtros escriben en query params independientemente
- `useSWR` usa la URL completa como key, así cualquier cambio triggerea refetch
- UI muestra badges activos con los filtros aplicados
- Botón "Clear all" para resetear todos los filtros a la vez

---

## Resumen de Interacciones entre Funcionalidades

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (Inversionista)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────┐
         │   Frontend (Next.js + TypeScript)  │
         ├───────────────────────────────────┤
         │  • CompanyList (listado principal) │
         │  • IndustryFilter (dropdown)       │
         │  • LocationFilter (dropdown)       │
         │  • Formateo client-side (Intl)     │
         └───────────────┬───────────────────┘
                         │
                         │ HTTP Requests
                         │
                         ▼
         ┌───────────────────────────────────┐
         │    Backend (FastAPI + Python)      │
         ├───────────────────────────────────┤
         │  GET /api/v1/companies?filters     │
         │  GET /api/v1/industries            │
         │  GET /api/v1/locations             │
         │                                    │
         │  • Routers (endpoints)             │
         │  • Services (lógica de negocio)    │
         │  • Repositories (queries)          │
         │  • Schemas (Pydantic validation)   │
         └───────────────┬───────────────────┘
                         │
                         │ SQLAlchemy ORM
                         │
                         ▼
         ┌───────────────────────────────────┐
         │   PostgreSQL (Supabase)            │
         ├───────────────────────────────────┤
         │  • company (100 registros)         │
         │  • industry (normalizada)          │
         │  • location (normalizada)          │
         │  • investor (normalizada)          │
         │  • company_investor (M2M)          │
         └───────────────────────────────────┘
```

---

## Decisiones Arquitectónicas Clave Aplicadas

| Decisión | Implementación | Beneficio |
|----------|----------------|-----------|
| **Eager loading de inversores** | SQLAlchemy `selectinload(Company.investors)` | Una sola query para datos completos, frontend más simple |
| **Sin paginación (MVP)** | Endpoint retorna las 100 empresas completas | Desarrollo más rápido, filtros funcionan sobre dataset completo |
| **Valores raw + formateo client-side** | Backend envía números, frontend usa `Intl.NumberFormat` | Separación de responsabilidades, flexibilidad para i18n futuro |
| **Filtros vía query params** | URL como source of truth: `?industry_id=1&location_id=3` | Sharable URLs, deep linking, navegación back/forward funciona |
| **Arquitectura por capas** | Router → Service → Repository → Model | Testeable, mantenible, escalable |

---

# Experiencia de Usuario

## Perfiles de Usuario

### 1. **Inversionista Venture Capital (Perfil Principal)**
- **Nombre**: Laura Chen
- **Contexto**: Partner en un fondo VC enfocado en early-stage SaaS
- **Objetivos**:
  - Identificar empresas SaaS emergentes con alto potencial de crecimiento
  - Analizar patrones de inversión de otros VCs en el sector
  - Comparar métricas de valoración vs. financiamiento entre competidores
- **Necesidades**:
  - Filtrar por industrias específicas donde tiene expertise (e.g., FinTech, MarTech)
  - Ver qué otros inversores están activos en esas verticales
  - Exportar o compartir listas filtradas con su equipo
- **Nivel técnico**: Medio (usa herramientas analíticas regularmente)
- **Dispositivos**: Desktop/Laptop (principal), Tablet ocasional

### 2. **Analista Financiero**
- **Nombre**: Marcus Thompson
- **Contexto**: Analista en firma de research que publica reportes sectoriales
- **Objetivos**:
  - Generar benchmarks de ARR y valoración por industria
  - Identificar tendencias geográficas en el ecosistema SaaS
  - Crear reportes comparativos entre empresas del mismo sector
- **Necesidades**:
  - Acceso rápido a métricas financieras confiables
  - Capacidad de filtrar y segmentar datos por múltiples dimensiones
  - Datos estructurados para procesamiento posterior
- **Nivel técnico**: Alto (familiarizado con APIs, exports, análisis de datos)
- **Dispositivos**: Desktop/Laptop exclusivamente

### 3. **Emprendedor SaaS**
- **Nombre**: Sofia Martínez
- **Contexto**: Fundadora de startup SaaS en fase de crecimiento
- **Objetivos**:
  - Entender el panorama competitivo en su industria
  - Identificar benchmarks de funding y valuación para su ronda siguiente
  - Descubrir qué inversores están activos en su sector
- **Necesidades**:
  - Vista rápida de competidores directos (misma industria + geografía)
  - Comparación de métricas de empresas similares
  - Información de contacto o perfil de inversores relevantes
- **Nivel técnico**: Medio (no técnico pero familiarizado con dashboards SaaS)
- **Dispositivos**: Desktop/Laptop, Mobile ocasional

---

## Flujos Clave de Usuario

### **Flujo 1: Descubrimiento Inicial (Primera Visita)**

**Objetivo**: Usuario nuevo explora la plataforma para entender qué datos están disponibles

1. **Landing en home** (`/`)
   - Ve título "Top SaaS Companies Dashboard"
   - Descripción breve del contenido y valor
   - Visualiza inmediatamente el listado de empresas (carga automática)

2. **Explora el listado completo**
   - Loading skeleton durante fetch inicial
   - Cards o tabla con las 100 empresas
   - Scroll para explorar más empresas
   - Contador visible: "Showing 100 companies"

3. **Inspecciona filtros disponibles**
   - Nota dropdowns de "Industry" y "Location" en la parte superior
   - Ve que puede refinar la búsqueda

4. **Éxito**: Usuario entiende qué datos hay y cómo navegar la plataforma

---

### **Flujo 2: Búsqueda Específica por Industria**

**Objetivo**: Inversionista busca empresas de una vertical específica (e.g., "CRM")

1. **Abre filtro de industria**
   - Click en dropdown "Select Industry"
   - Ve lista de todas las industrias disponibles (alfabéticamente)

2. **Selecciona industria**
   - Click en "CRM"
   - URL actualiza: `/?industry_id=1`

3. **Ve resultados filtrados**
   - Listado se actualiza mostrando solo empresas CRM
   - Contador actualiza: "Showing 15 companies (filtered)"
   - Badge visible: "Industry: CRM ✕" (permite remover filtro)

4. **Explora y compara**
   - Revisa métricas de empresas CRM
   - Compara valuaciones y ARR entre competidores
   - Ve qué inversores están activos en CRM

5. **Comparte hallazgos** (opcional)
   - Copia URL de la página: `/?industry_id=1`
   - Envía link a colega → al abrir, ve exactamente los mismos filtros aplicados

6. **Éxito**: Usuario encontró y analizó empresas de su sector de interés

---

### **Flujo 3: Análisis Geográfico con Múltiples Filtros**

**Objetivo**: Analista busca empresas de FinTech en San Francisco

1. **Aplica primer filtro (Industria)**
   - Selecciona "FinTech" en dropdown de industria
   - Ve resultados filtrados (e.g., 20 empresas)
   - URL: `/?industry_id=5`

2. **Aplica segundo filtro (Ubicación)**
   - Click en dropdown "Select Location"
   - Ve lista organizada por país y ciudad
   - Selecciona "San Francisco, CA, USA"
   - URL actualiza: `/?industry_id=5&location_id=1`

3. **Ve resultados combinados**
   - Listado muestra solo empresas que cumplen AMBOS filtros
   - Contador: "Showing 8 companies (filtered)"
   - Badges activos: "Industry: FinTech ✕" | "Location: San Francisco, CA ✕"

4. **Analiza resultados específicos**
   - Revisa las 8 empresas FinTech de SF
   - Compara métricas, productos, inversores
   - Identifica patrones (e.g., "Sequoia invirtió en 5 de estas 8")

5. **Refina o resetea**
   - Opción A: Click en "✕" de un badge para remover ese filtro específico
   - Opción B: Click en "Clear all filters" para empezar de nuevo

6. **Éxito**: Usuario obtuvo insights específicos de un nicho muy particular

---

### **Flujo 4: Exploración de Inversores**

**Objetivo**: Usuario quiere entender qué inversores están activos en ciertas empresas

1. **Busca empresa conocida**
   - Scroll o búsqueda visual para encontrar "Salesforce"
   - Ve card de Salesforce con sus métricas

2. **Inspecciona inversores**
   - Ve sección "Investors" en el card
   - Lista de badges: "Sequoia Capital", "Accel Partners", "Greylock"

3. **Identifica patrón**
   - Nota que "Sequoia Capital" aparece en muchas empresas
   - Scroll para ver otras empresas con Sequoia

4. **Insight generado**
   - Comprende qué VCs son más activos en el ecosistema SaaS
   - Identifica posibles contactos para fundraising

5. **Éxito**: Usuario entendió relaciones entre empresas e inversores

---

## Consideraciones de UI/UX

### **Layout y Navegación**

**Header/Navbar**:
- Logo o título de la app (izquierda)
- Navegación simple: "Companies" (única página por ahora)
- Espacio para futuras secciones: "Industries", "Investors", "Analytics"

**Área de Filtros**:
- Ubicación: Top de la página, siempre visible
- Layout horizontal en desktop:
  ```
  [Industry Filter ▼]  [Location Filter ▼]  [Clear All]  |  Showing X companies
  ```
- Responsive: Stack vertical en mobile, filtros colapsables

**Área de Contenido Principal**:
- **Opción recomendada**: Grid de cards (3-4 columnas en desktop, 1 en mobile)
- Cada card muestra todos los campos de forma clara y legible
- Hover effects para feedback visual

**Footer**:
- Información sobre fuente de datos: "Data from Kaggle - Top 100 SaaS Companies"
- Link al dataset original

---

### **Diseño de Componentes**

#### **CompanyCard**

```
┌─────────────────────────────────────────────┐
│  Salesforce                          [CRM]  │
│  ────────────────────────────────────────── │
│                                             │
│  📍 San Francisco, CA, USA                  │
│  🏭 Customer 360, Sales Cloud, Service...   │
│  📅 Founded: 1999                           │
│                                             │
│  💰 Funding: $150M                          │
│  📈 ARR: $31.0B                             │
│  💎 Valuation: $200B                        │
│                                             │
│  🤝 Investors:                              │
│     [Sequoia] [Accel] [Greylock]           │
└─────────────────────────────────────────────┘
```

**Características**:
- Header con nombre destacado + badge de industria
- Iconos visuales para cada tipo de información
- Números financieros formateados con notación compacta ($150M, $31.0B)
- Inversores como badges
- Hover effect para feedback visual
- Sombra sutil, border radius moderno

---

### **Estados de UI**

#### **Loading State**
- Skeleton screens mientras carga datos
- Estructura del skeleton refleja el layout final
- Animación pulse sutil
- Duración esperada: < 1 segundo

#### **Empty State (Filtros sin resultados)**
```
┌─────────────────────────────────────────┐
│           🔍 No Results Found           │
│                                         │
│   No companies match your filters      │
│   Try adjusting or clearing filters    │
│                                         │
│   [Clear All Filters]                  │
└─────────────────────────────────────────┘
```

#### **Error State**
```
┌─────────────────────────────────────────┐
│           ⚠️ Error Loading Data         │
│                                         │
│   Could not fetch companies            │
│   Please try again later               │
│                                         │
│   [Retry]                              │
└─────────────────────────────────────────┘
```

---

### **Responsive Design**

- **Desktop (>1024px)**: 3-4 columnas de cards, filtros en fila horizontal
- **Tablet (768-1024px)**: 2 columnas, filtros en fila horizontal
- **Mobile (<768px)**: 1 columna, filtros stack vertical y colapsables

---

### **Accesibilidad (a11y)**

- **Keyboard Navigation**: Tab entre filtros y cards, Enter/Space para acciones
- **Screen Readers**: Labels apropiados, anuncio de cambios en filtros
- **Color Contrast**: WCAG AA compliance (4.5:1 para texto normal)
- **Focus Indicators**: Focus ring visible en todos los elementos interactivos

---

# Arquitectura

## Componentes del Sistema

### **Arquitectura General (3-Tier)**

```
┌──────────────────────────────────────────────────────────────┐
│                    CLIENT TIER (Browser)                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Next.js 16 (App Router) + TypeScript           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │   Pages/     │  │  Components  │  │    Hooks     │ │  │
│  │  │   Routes     │  │     (UI)     │  │  (Custom)    │ │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │  │
│  │         │                 │                  │         │  │
│  │         └─────────────────┴──────────────────┘         │  │
│  │                           │                            │  │
│  │                  ┌────────▼─────────┐                  │  │
│  │                  │   API Client     │                  │  │
│  │                  │  (lib/api.ts)    │                  │  │
│  │                  └────────┬─────────┘                  │  │
│  └───────────────────────────┼──────────────────────────────┘  │
└────────────────────────────────┼──────────────────────────────┘
                                │ HTTP/REST (JSON)
┌────────────────────────────────▼──────────────────────────────┐
│                   APPLICATION TIER (Server)                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           FastAPI (Python 3.12+) + Uvicorn             │  │
│  │                                                         │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │              API Layer (Routers)                  │  │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │  │  │
│  │  │  │ Company  │  │ Industry │  │ Location │       │  │  │
│  │  │  │ Router   │  │  Router  │  │  Router  │       │  │  │
│  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘       │  │  │
│  │  └───────┼─────────────┼─────────────┼─────────────┘  │  │
│  │          │             │             │                │  │
│  │  ┌───────▼─────────────▼─────────────▼─────────────┐  │  │
│  │  │         Service Layer (Business Logic)           │  │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │  │  │
│  │  │  │ Company  │  │ Industry │  │ Location │      │  │  │
│  │  │  │ Service  │  │  Service │  │  Service │      │  │  │
│  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘      │  │  │
│  │  └───────┼─────────────┼─────────────┼────────────┘  │  │
│  │          │             │             │               │  │
│  │  ┌───────▼─────────────▼─────────────▼────────────┐  │  │
│  │  │      Repository Layer (Data Access)              │  │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │  │  │
│  │  │  │ Company  │  │ Industry │  │ Location │     │  │  │
│  │  │  │   Repo   │  │   Repo   │  │   Repo   │     │  │  │
│  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘     │  │  │
│  │  └───────┼─────────────┼─────────────┼───────────┘  │  │
│  │          │             │             │              │  │
│  │  ┌───────▼─────────────▼─────────────▼───────────┐  │  │
│  │  │      SQLAlchemy ORM (Async Models)              │  │
│  │  └──────────────────────┬────────────────────────┘  │  │
│  │                         │                           │  │
│  │  ┌──────────────────────▼────────────────────────┐  │  │
│  │  │       Pydantic Schemas (Validation)            │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬──────────────────────────────┘
                                │ SQL (Async)
┌────────────────────────────────▼──────────────────────────────┐
│                      DATA TIER (Database)                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           PostgreSQL 15+ (Supabase Hosted)             │  │
│  │                                                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │
│  │  │ company  │  │ industry │  │ location │            │  │
│  │  │  (100)   │  │  (~20)   │  │  (~30)   │            │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │  │
│  │       │             │             │                   │  │
│  │       │   ┌─────────▼──────────┐  │                  │  │
│  │       │   │     investor        │  │                  │  │
│  │       │   │      (~50)          │  │                  │  │
│  │       │   └─────────┬───────────┘  │                  │  │
│  │       │             │              │                  │  │
│  │       │   ┌─────────▼──────────┐   │                  │  │
│  │       └───► company_investor   │◄──┘                  │  │
│  │           │   (M2M junction)   │                      │  │
│  │           └────────────────────┘                      │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Modelos de Datos

### **Esquema de Base de Datos**

#### **Tabla: `company`**
```sql
CREATE TABLE company (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    products TEXT,
    founding_year INTEGER,
    total_funding BIGINT,           -- En USD (valor raw)
    arr BIGINT,                      -- Annual Recurring Revenue en USD
    valuation BIGINT,                -- En USD
    employees INTEGER,
    g2_rating REAL,                  -- Rating de 0.0 a 5.0
    industry_id BIGINT REFERENCES industry(id),
    location_id BIGINT REFERENCES location(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Índices**:
- `idx_company_industry` en `industry_id`
- `idx_company_location` en `location_id`

**Relaciones**:
- `industry_id` → `industry.id` (Many-to-One)
- `location_id` → `location.id` (Many-to-One)
- `investors` → vía `company_investor` (Many-to-Many)

---

#### **Tabla: `industry`**
```sql
CREATE TABLE industry (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Ejemplos**: CRM, Marketing Automation, Collaboration, FinTech, HR Tech, ERP

---

#### **Tabla: `location`**
```sql
CREATE TABLE location (
    id BIGSERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    state TEXT,                      -- Puede ser NULL (fuera de USA)
    country TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Ejemplos**: San Francisco/CA/USA, New York/NY/USA, London/NULL/UK, Tel Aviv/NULL/Israel

---

#### **Tabla: `investor`**
```sql
CREATE TABLE investor (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Ejemplos**: Sequoia Capital, Accel Partners, Andreessen Horowitz, Y Combinator

---

#### **Tabla: `company_investor` (Junction Table)**
```sql
CREATE TABLE company_investor (
    company_id BIGINT REFERENCES company(id) ON DELETE CASCADE,
    investor_id BIGINT REFERENCES investor(id) ON DELETE CASCADE,
    PRIMARY KEY (company_id, investor_id)
);
```

**Índices**:
- `idx_company_investor_company` en `company_id`
- `idx_company_investor_investor` en `investor_id`

---

### **Modelos SQLAlchemy (Backend)**

**Archivo**: `src/backend/models/company.py`

```python
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Text, Float, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.core.database import Base

# Junction table para M2M
company_investor_table = Table(
    "company_investor",
    Base.metadata,
    Column("company_id", BigInteger, ForeignKey("company.id"), primary_key=True),
    Column("investor_id", BigInteger, ForeignKey("investor.id"), primary_key=True),
)

class Company(Base):
    __tablename__ = "company"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    products: Mapped[str | None] = mapped_column(Text)
    founding_year: Mapped[int | None] = mapped_column(Integer)
    total_funding: Mapped[int | None] = mapped_column(BigInteger)
    arr: Mapped[int | None] = mapped_column(BigInteger)
    valuation: Mapped[int | None] = mapped_column(BigInteger)
    employees: Mapped[int | None] = mapped_column(Integer)
    g2_rating: Mapped[float | None] = mapped_column(Float)
    
    # Foreign Keys
    industry_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("industry.id"))
    location_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("location.id"))
    
    # Relationships (eager loading configurado aquí)
    industry: Mapped["Industry"] = relationship(back_populates="companies")
    location: Mapped["Location"] = relationship(back_populates="companies")
    investors: Mapped[list["Investor"]] = relationship(
        secondary=company_investor_table,
        back_populates="companies"
    )

class Industry(Base):
    __tablename__ = "industry"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    companies: Mapped[list["Company"]] = relationship(back_populates="industry")

class Location(Base):
    __tablename__ = "location"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str | None] = mapped_column(Text)
    country: Mapped[str] = mapped_column(Text, nullable=False)
    
    companies: Mapped[list["Company"]] = relationship(back_populates="location")

class Investor(Base):
    __tablename__ = "investor"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    companies: Mapped[list["Company"]] = relationship(
        secondary=company_investor_table,
        back_populates="investors"
    )
```

---

### **Schemas Pydantic (Backend)**

**Archivo**: `src/backend/schemas/company.py`

```python
from pydantic import BaseModel, Field

# Schemas anidados
class IndustryRead(BaseModel):
    id: int
    name: str
    
    model_config = {"from_attributes": True}

class LocationRead(BaseModel):
    id: int
    city: str
    state: str | None
    country: str
    
    model_config = {"from_attributes": True}

class InvestorRead(BaseModel):
    id: int
    name: str
    
    model_config = {"from_attributes": True}

# Schema principal de lectura
class CompanyRead(BaseModel):
    id: int
    name: str
    products: str | None
    founding_year: int | None
    total_funding: int | None = Field(description="Total funding in USD")
    arr: int | None = Field(description="Annual Recurring Revenue in USD")
    valuation: int | None = Field(description="Company valuation in USD")
    employees: int | None
    g2_rating: float | None
    
    # Relaciones anidadas
    industry: IndustryRead | None
    location: LocationRead | None
    investors: list[InvestorRead] = Field(default_factory=list)
    
    model_config = {"from_attributes": True}

# Schema de respuesta de listado
class CompanyListResponse(BaseModel):
    data: list[CompanyRead]
    total: int
    filters_applied: dict[str, list[int]] = Field(default_factory=dict)
```

---

### **Tipos TypeScript (Frontend)**

**Archivo**: `src/frontend/lib/types.ts`

```typescript
export interface Industry {
  id: number;
  name: string;
}

export interface Location {
  id: number;
  city: string;
  state: string | null;
  country: string;
}

export interface Investor {
  id: number;
  name: string;
}

export interface Company {
  id: number;
  name: string;
  products: string | null;
  founding_year: number | null;
  total_funding: number | null;  // Raw value in USD
  arr: number | null;             // Raw value in USD
  valuation: number | null;       // Raw value in USD
  employees: number | null;
  g2_rating: number | null;
  
  // Nested relations
  industry: Industry | null;
  location: Location | null;
  investors: Investor[];
}

export interface CompanyListResponse {
  data: Company[];
  total: number;
  filters_applied?: {
    industry_id?: number[];
    location_id?: number[];
  };
}
```

---

## APIs e Integraciones

### **Backend API Endpoints**

**Base URL**: `http://localhost:8000/api/v1`

#### **1. List Companies (con filtros)**
```
GET /companies?industry_id=1,2&location_id=3
```

**Query Parameters**:
- `industry_id` (optional): Comma-separated list of industry IDs
- `location_id` (optional): Comma-separated list of location IDs

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": 1,
      "name": "Salesforce",
      "products": "Customer 360, Sales Cloud",
      "founding_year": 1999,
      "total_funding": 150000000,
      "arr": 31000000000,
      "valuation": 200000000000,
      "employees": 73000,
      "g2_rating": 4.3,
      "industry": {"id": 1, "name": "CRM"},
      "location": {"id": 1, "city": "San Francisco", "state": "CA", "country": "USA"},
      "investors": [
        {"id": 1, "name": "Sequoia Capital"},
        {"id": 2, "name": "Accel Partners"}
      ]
    }
  ],
  "total": 100,
  "filters_applied": {
    "industry_id": [1, 2],
    "location_id": [3]
  }
}
```

**Implementación**:
- Router: `CompanyRouter.get_companies()`
- Service: `CompanyService.get_filtered_companies()`
- Repository: `CompanyRepository.find_all_with_filters()`
- Query con eager loading:
  ```python
  query = select(Company).options(
      selectinload(Company.industry),
      selectinload(Company.location),
      selectinload(Company.investors)
  )
  if industry_ids:
      query = query.filter(Company.industry_id.in_(industry_ids))
  if location_ids:
      query = query.filter(Company.location_id.in_(location_ids))
  ```

---

#### **2. List Industries**
```
GET /industries
```

**Response** (200 OK):
```json
{
  "data": [
    {"id": 1, "name": "CRM"},
    {"id": 2, "name": "Marketing Automation"},
    {"id": 3, "name": "Collaboration"}
  ]
}
```

---

#### **3. List Locations**
```
GET /locations
```

**Response** (200 OK):
```json
{
  "data": [
    {"id": 1, "city": "San Francisco", "state": "CA", "country": "USA"},
    {"id": 2, "city": "New York", "state": "NY", "country": "USA"},
    {"id": 3, "city": "London", "state": null, "country": "UK"}
  ]
}
```

---

### **Frontend API Client**

**Archivo**: `src/frontend/lib/api.ts`

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Fetch companies con filtros opcionales
export async function fetchCompanies(filters?: {
  industry_id?: number[];
  location_id?: number[];
}): Promise<CompanyListResponse> {
  const params = new URLSearchParams();
  
  if (filters?.industry_id?.length) {
    params.set('industry_id', filters.industry_id.join(','));
  }
  if (filters?.location_id?.length) {
    params.set('location_id', filters.location_id.join(','));
  }
  
  const url = `${API_BASE_URL}/companies${params.toString() ? `?${params}` : ''}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch companies: ${response.statusText}`);
  }
  
  return response.json();
}

// Fetch industries
export async function fetchIndustries(): Promise<IndustryListResponse> {
  const response = await fetch(`${API_BASE_URL}/industries`);
  if (!response.ok) throw new Error('Failed to fetch industries');
  return response.json();
}

// Fetch locations
export async function fetchLocations(): Promise<LocationListResponse> {
  const response = await fetch(`${API_BASE_URL}/locations`);
  if (!response.ok) throw new Error('Failed to fetch locations');
  return response.json();
}
```

---

## Requisitos de Infraestructura

### **Entorno de Desarrollo**

#### **Backend**
- **Python**: 3.12+
- **Gestor de paquetes**: `uv`
- **Servidor**: Uvicorn
- **Base de datos**: PostgreSQL 15+ (Supabase)
- **Variables de entorno** (`.env`):
  ```env
  DATABASE_URL=postgresql+asyncpg://user:pass@db.supabase.co:5432/postgres
  CORS_ORIGINS=http://localhost:3000
  ENVIRONMENT=development
  ```

**Comandos**:
```bash
cd src/backend
uv sync                    # Instalar dependencias
uv run fastapi dev         # Servidor en http://localhost:8000
```

---

#### **Frontend**
- **Node.js**: 20+ LTS
- **Gestor de paquetes**: npm
- **Framework**: Next.js 16+
- **Variables de entorno** (`.env.local`):
  ```env
  NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
  ```

**Comandos**:
```bash
cd src/frontend
npm install                # Instalar dependencias
npm run dev                # Servidor en http://localhost:3000
```

---

#### **Base de Datos**
- **Provider**: Supabase (PostgreSQL managed)
- **Conexión**: Async con `asyncpg` driver
- **Estado actual**: Schema creado, datos cargados

---

### **Estructura de Directorios**

#### **Backend** (`src/backend/`)
```
backend/
├── main.py                      # Punto de entrada FastAPI
├── pyproject.toml               # Configuración uv
├── api/
│   ├── __init__.py
│   ├── health.py                # Health check endpoint
│   └── v1/
│       ├── __init__.py
│       ├── companies.py         # CompanyRouter
│       ├── industries.py        # IndustryRouter
│       └── locations.py         # LocationRouter
├── core/
│   ├── __init__.py
│   ├── config.py                # Settings con pydantic-settings
│   └── database.py              # DB session, engine, Base
├── models/
│   ├── __init__.py
│   ├── company.py               # SQLAlchemy models
│   ├── industry.py
│   ├── location.py
│   └── investor.py
├── schemas/
│   ├── __init__.py
│   ├── company.py               # Pydantic schemas
│   ├── industry.py
│   └── location.py
├── services/
│   ├── __init__.py
│   ├── company_service.py       # Business logic
│   ├── industry_service.py
│   └── location_service.py
└── repositories/
    ├── __init__.py
    ├── company_repository.py    # Data access layer
    ├── industry_repository.py
    └── location_repository.py
```

---

#### **Frontend** (`src/frontend/`)
```
frontend/
├── app/
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page (listado principal)
│   └── globals.css              # Tailwind globals
├── components/
│   ├── CompanyList.tsx          # Listado de empresas
│   ├── CompanyCard.tsx          # Card individual
│   ├── IndustryFilter.tsx       # Dropdown de industrias
│   ├── LocationFilter.tsx       # Dropdown de ubicaciones
│   └── ui/                      # Componentes base (Button, Badge, etc.)
├── lib/
│   ├── api.ts                   # API client functions
│   ├── types.ts                 # TypeScript interfaces
│   └── utils/
│       └── format.ts            # Formateo de números, fechas
├── hooks/
│   └── useCompanies.ts          # Custom hook con SWR
└── public/
    └── ...                      # Assets estáticos
```

---

### **Seguridad y Configuración**

#### **CORS (Backend)**
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

#### **Variables de Entorno**
- Desarrollo: `.env` files (nunca commiteados, listados en `.gitignore`)
- Producción: Variables en plataforma de hosting (Vercel, Railway, etc.)

---

### **Dependencias Principales**

#### **Backend** (`pyproject.toml`)
```toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.29.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
```

#### **Frontend** (`package.json`)
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "swr": "^2.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^3.4.0",
    "eslint": "^8.0.0"
  }
}
```

---

# Hoja de Ruta de Desarrollo

## Fase 1: MVP (Minimum Viable Product)

### Objetivo
Crear una aplicación funcional que permita visualizar y filtrar las 100 empresas SaaS con las funcionalidades core descritas en este documento.

### Alcance Detallado

#### **1.1 Configuración de Infraestructura Base**

**Backend**:
- [ ] Configurar proyecto FastAPI con estructura de directorios por capas
- [ ] Configurar `pyproject.toml` con `uv` como gestor de dependencias
- [ ] Instalar dependencias core: FastAPI, Uvicorn, SQLAlchemy, asyncpg, Pydantic
- [ ] Configurar `ruff.toml` para linting y formateo
- [ ] Configurar `mypy` para type checking
- [ ] Crear archivo `.env.example` con variables de entorno requeridas
- [ ] Configurar CORS middleware para aceptar requests desde frontend

**Frontend**:
- [ ] Inicializar proyecto Next.js 16+ con App Router
- [ ] Configurar TypeScript con `tsconfig.json` estricto
- [ ] Instalar y configurar Tailwind CSS
- [ ] Configurar ESLint y Prettier
- [ ] Crear archivo `.env.local.example` con variables de entorno
- [ ] Configurar SWR para data fetching

**Base de Datos**:
- [ ] Verificar conexión a Supabase PostgreSQL
- [ ] Confirmar que el schema está creado (ya ejecutado)
- [ ] Confirmar que los datos están cargados (scripts 02-06)
- [ ] Crear archivo de configuración de conexión async

**Entregables**:
- Repositorio con estructura base funcional
- Scripts de desarrollo: `./scripts/dev/run-backend.sh` y `./scripts/dev/run-frontend.sh`
- README con instrucciones de setup
- Ambos servidores corriendo: Backend (8000) y Frontend (3000)

---

#### **1.2 Capa de Datos (Backend)**

**Modelos SQLAlchemy**:
- [ ] Crear `backend/core/database.py` con engine async y session factory
- [ ] Crear `backend/models/industry.py` con modelo Industry
- [ ] Crear `backend/models/location.py` con modelo Location
- [ ] Crear `backend/models/investor.py` con modelo Investor
- [ ] Crear `backend/models/company.py` con modelo Company y relaciones M2M
- [ ] Configurar `company_investor_table` para junction table
- [ ] Configurar relationships con `selectinload` para eager loading

**Schemas Pydantic**:
- [ ] Crear `backend/schemas/industry.py` con `IndustryRead`
- [ ] Crear `backend/schemas/location.py` con `LocationRead`
- [ ] Crear `backend/schemas/investor.py` con `InvestorRead`
- [ ] Crear `backend/schemas/company.py` con:
  - `CompanyRead` (schema principal con relaciones anidadas)
  - `CompanyListResponse` (wrapper con metadata)
- [ ] Validar que `from_attributes = True` esté configurado en todos los schemas

**Repositories**:
- [ ] Crear `backend/repositories/base_repository.py` con clase base abstracta
- [ ] Crear `backend/repositories/industry_repository.py`:
  - `find_all()` → retorna todas las industrias ordenadas por nombre
- [ ] Crear `backend/repositories/location_repository.py`:
  - `find_all()` → retorna todas las ubicaciones ordenadas por país/ciudad
- [ ] Crear `backend/repositories/company_repository.py`:
  - `find_all_with_filters(industry_ids, location_ids)` → query con filtros opcionales y eager loading
  - `count_with_filters(industry_ids, location_ids)` → contador para metadata

**Entregables**:
- Modelos completos con relaciones configuradas
- Schemas Pydantic validados
- Repositories con queries async funcionales
- Tests unitarios para repositories (al menos 1 test por método)

---

#### **1.3 Capa de Negocio (Backend)**

**Services**:
- [ ] Crear `backend/services/industry_service.py`:
  - `get_all()` → llama a repository y retorna lista de industrias
- [ ] Crear `backend/services/location_service.py`:
  - `get_all()` → llama a repository y retorna lista de ubicaciones
- [ ] Crear `backend/services/company_service.py`:
  - `get_filtered_companies(industry_ids, location_ids)` → lógica de filtrado
  - Construir `filters_applied` dict para respuesta
  - Retornar `CompanyListResponse` con data + metadata

**Dependency Injection**:
- [ ] Crear `backend/core/dependencies.py`:
  - `get_db_session()` → dependency para DB session
  - `get_company_service()` → dependency para CompanyService
  - `get_industry_service()` → dependency para IndustryService
  - `get_location_service()` → dependency para LocationService

**Entregables**:
- Services con lógica de negocio encapsulada
- Dependency injection configurada
- Tests unitarios para services (mocking repositories)

---

#### **1.4 API REST (Backend)**

**Routers**:
- [ ] Crear `backend/api/__init__.py` con función `include_routers(app)`
- [ ] Crear `backend/api/v1/companies.py`:
  - `GET /api/v1/companies` con query params `industry_id`, `location_id`
  - Validar query params (convertir strings a listas de ints)
  - Inyectar `CompanyService` vía `Depends()`
  - Retornar `CompanyListResponse` con status 200
  - Manejar errores con `HTTPException`
- [ ] Crear `backend/api/v1/industries.py`:
  - `GET /api/v1/industries`
  - Retornar lista de industrias con status 200
- [ ] Crear `backend/api/v1/locations.py`:
  - `GET /api/v1/locations`
  - Retornar lista de ubicaciones con status 200

**Main App**:
- [ ] Actualizar `backend/main.py`:
  - Incluir routers con prefijo `/api/v1`
  - Configurar OpenAPI docs en `/docs`
  - Agregar tags para organización en Swagger

**Testing de API**:
- [ ] Tests de integración con `TestClient` de FastAPI:
  - Test GET `/api/v1/companies` sin filtros (debe retornar 100)
  - Test GET `/api/v1/companies?industry_id=1` (debe filtrar correctamente)
  - Test GET `/api/v1/companies?industry_id=1&location_id=2` (filtros combinados)
  - Test GET `/api/v1/industries` (debe retornar lista completa)
  - Test GET `/api/v1/locations` (debe retornar lista completa)

**Entregables**:
- API REST funcional con 3 endpoints
- Documentación OpenAPI automática en `/docs`
- Tests de integración con coverage >60%
- Backend completamente funcional y testeable

---

#### **1.5 API Client y Tipos (Frontend)**

**Tipos TypeScript**:
- [ ] Crear `src/frontend/lib/types.ts`:
  - Interface `Industry`
  - Interface `Location`
  - Interface `Investor`
  - Interface `Company` (con relaciones anidadas)
  - Interface `CompanyListResponse`
  - Interface `IndustryListResponse`
  - Interface `LocationListResponse`

**API Client**:
- [ ] Crear `src/frontend/lib/api.ts`:
  - Función `fetchCompanies(filters?)` → GET /api/v1/companies
  - Función `fetchIndustries()` → GET /api/v1/industries
  - Función `fetchLocations()` → GET /api/v1/locations
  - Helper `buildQueryString()` para construir query params
  - Manejo de errores con throw

**Utilities**:
- [ ] Crear `src/frontend/lib/utils/format.ts`:
  - Función `formatCurrency(value: number)` → usa `Intl.NumberFormat` con notation compact
  - Función `formatNumber(value: number)` → formatea números con separadores
  - Función `formatYear(year: number)` → retorna año como string
  - Función `formatLocation(location: Location)` → "City, State, Country" o "City, Country"

**Entregables**:
- Tipos TypeScript completos y type-safe
- API client funcional con manejo de errores
- Utilities de formateo testeables
- Tests unitarios para formateo

---

#### **1.6 Componentes UI Core (Frontend)**

**Componentes Base**:
- [ ] Crear `src/frontend/components/ui/Badge.tsx`:
  - Componente reutilizable para industrias, ubicaciones, inversores
  - Props: `label`, `variant`, `onRemove` (opcional)
  - Variantes: default, primary, secondary
- [ ] Crear `src/frontend/components/ui/Button.tsx`:
  - Props: `children`, `onClick`, `variant`, `disabled`
  - Variantes: primary, secondary, ghost
- [ ] Crear `src/frontend/components/ui/Select.tsx`:
  - Dropdown genérico (o usar Headless UI)
  - Props: `options`, `value`, `onChange`, `placeholder`

**Componentes de Negocio**:
- [ ] Crear `src/frontend/components/CompanyCard.tsx`:
  - Props: `company: Company`
  - Renderizar todos los campos con iconos visuales
  - Formatear números con utilities
  - Mostrar inversores como badges
  - Hover effect con elevación
- [ ] Crear `src/frontend/components/CompanyList.tsx`:
  - Props: `companies: Company[]`, `isLoading`, `error`
  - Grid responsive (3-4 cols desktop, 1 col mobile)
  - Mapear cada empresa a `CompanyCard`
  - Skeleton loading state
  - Empty state cuando no hay resultados
  - Error state con retry button

**Entregables**:
- Componentes UI base reutilizables
- CompanyCard con diseño completo según especificación
- CompanyList con todos los estados (loading, empty, error, success)
- Storybook (opcional) para documentar componentes

---

#### **1.7 Filtros y Estado (Frontend)**

**Componentes de Filtro**:
- [ ] Crear `src/frontend/components/IndustryFilter.tsx`:
  - Fetch de industrias con SWR al montar
  - Dropdown multi-select (o single-select para MVP)
  - Sincronizar selección con URL query params
  - Mostrar loading state mientras carga opciones
- [ ] Crear `src/frontend/components/LocationFilter.tsx`:
  - Fetch de ubicaciones con SWR al montar
  - Dropdown con opciones formateadas ("City, Country")
  - Sincronizar con URL query params
  - Opcional: agrupar por país
- [ ] Crear `src/frontend/components/FilterBar.tsx`:
  - Contenedor para ambos filtros
  - Contador de resultados: "Showing X companies"
  - Badges de filtros activos con botón de remover
  - Botón "Clear all filters"
  - Layout responsive (horizontal desktop, vertical mobile)

**Gestión de Estado**:
- [ ] Crear `src/frontend/hooks/useCompanies.ts`:
  - Custom hook que encapsula SWR
  - Lee filtros desde URL query params (`useSearchParams`)
  - Construye key dinámica para SWR basada en filtros
  - Llama a `fetchCompanies()` con filtros
  - Retorna: `{ data, error, isLoading, mutate }`
- [ ] Crear `src/frontend/hooks/useFilters.ts`:
  - Custom hook para gestionar filtros
  - Lee/escribe query params con Next.js router
  - Funciones: `setIndustryFilter()`, `setLocationFilter()`, `clearFilters()`
  - Sincronización bidireccional URL ↔ Estado

**Entregables**:
- Filtros funcionales con UI completa
- Sincronización URL ↔ Filtros ↔ Datos
- URLs compartibles que mantienen filtros aplicados
- Tests de integración para flujo completo de filtrado

---

#### **1.8 Página Principal (Frontend)**

**Layout**:
- [ ] Actualizar `src/frontend/app/layout.tsx`:
  - Header con título de la app
  - Footer con créditos y link al dataset
  - Metadata para SEO (title, description)
  - Importar `globals.css` con Tailwind

**Home Page**:
- [ ] Actualizar `src/frontend/app/page.tsx`:
  - Usar hook `useCompanies()` para fetch de datos
  - Usar hook `useFilters()` para gestión de filtros
  - Renderizar `FilterBar` en top
  - Renderizar `CompanyList` con datos filtrados
  - Manejar estados: loading (skeleton), error (retry), success
  - Configurar SWR con `refreshInterval` opcional

**Estilos**:
- [ ] Configurar `src/frontend/app/globals.css`:
  - Imports de Tailwind
  - Custom CSS variables para colores (opcional)
  - Utility classes personalizadas si es necesario

**Entregables**:
- Home page funcional con todos los componentes integrados
- Flujo completo: filtros → fetch → visualización
- Responsive en desktop, tablet y mobile
- Todas las funcionalidades del MVP operativas

---

#### **1.9 Testing y Calidad**

**Backend**:
- [ ] Ejecutar `uv run ruff check` y corregir issues
- [ ] Ejecutar `uv run ruff format` para formateo consistente
- [ ] Ejecutar `uv run mypy .` y resolver type errors
- [ ] Ejecutar `uv run pytest --cov` y verificar coverage >60%
- [ ] Revisar y actualizar docstrings en funciones públicas

**Frontend**:
- [ ] Ejecutar `npm run lint` y corregir issues
- [ ] Ejecutar `npm run type-check` (tsc --noEmit)
- [ ] Ejecutar `npm test` si hay tests configurados
- [ ] Verificar que `npm run build` sea exitoso
- [ ] Probar manualmente en Chrome, Firefox, Safari

**Testing Manual**:
- [ ] Flujo 1: Primera visita → ver listado completo
- [ ] Flujo 2: Filtrar por industria → ver resultados correctos
- [ ] Flujo 3: Filtrar por ubicación → ver resultados correctos
- [ ] Flujo 4: Combinar filtros → ver intersección correcta
- [ ] Flujo 5: Copiar URL con filtros → abrir en nueva pestaña → filtros persisten
- [ ] Flujo 6: Clear all filters → volver a listado completo
- [ ] Flujo 7: Mobile responsive → verificar en viewport 375px

**Entregables**:
- Código con linting/formateo/type checking limpio
- Tests con coverage adecuado
- Aplicación funcional end-to-end
- Flujos de usuario validados

---

#### **1.10 Documentación y Deploy**

**Documentación**:
- [ ] Actualizar `README.md` con:
  - Descripción del proyecto
  - Stack tecnológico
  - Instrucciones de instalación (backend + frontend)
  - Comandos de desarrollo
  - Variables de entorno requeridas
  - Estructura de directorios
  - Contribución y contacto
- [ ] Documentar endpoints en `docs/api.md` (opcional, ya hay OpenAPI)
- [ ] Crear `CONTRIBUTING.md` con guías de contribución

**Preparación para Deploy (Opcional en MVP)**:
- [ ] Configurar variables de entorno para producción
- [ ] Crear `Dockerfile` para backend (opcional)
- [ ] Configurar build de Next.js para producción
- [ ] Documentar proceso de deploy en README

**Entregables**:
- Documentación completa y actualizada
- MVP listo para demo/presentación
- (Opcional) Deploy en staging environment

---

### Criterios de Aceptación del MVP

**Funcional**:
- ✅ Usuario puede ver listado de 100 empresas con todas las métricas
- ✅ Usuario puede filtrar por industria
- ✅ Usuario puede filtrar por ubicación
- ✅ Usuario puede combinar múltiples filtros
- ✅ URLs son compartibles y mantienen filtros
- ✅ Inversores se muestran anidados en cada empresa
- ✅ Números financieros están formateados correctamente

**Técnico**:
- ✅ Backend pasa linting, type checking y tests (coverage >60%)
- ✅ Frontend pasa linting, type checking y build exitoso
- ✅ Eager loading funciona (sin N+1 queries)
- ✅ API retorna respuestas en <500ms para 100 empresas
- ✅ Frontend carga inicial en <2 segundos

**UX**:
- ✅ Loading states visibles durante fetch
- ✅ Empty state cuando filtros no tienen resultados
- ✅ Error state con retry cuando falla fetch
- ✅ Responsive en desktop, tablet, mobile
- ✅ Accesibilidad básica (keyboard navigation, contrast)

---

## Fase 2: Mejoras y Expansión (Post-MVP)

### Objetivo
Agregar funcionalidades adicionales basadas en feedback del MVP y preparar para escalabilidad.

### Alcance Propuesto

#### **2.1 Búsqueda por Nombre**
- [ ] Agregar input de búsqueda en FilterBar
- [ ] Endpoint backend: `GET /api/v1/companies?search=salesforce`
- [ ] Query con `ILIKE` en nombre de empresa
- [ ] Autocompletado con debounce (opcional)

#### **2.2 Filtro por Inversor**
- [ ] Endpoint: `GET /api/v1/investors`
- [ ] Componente `InvestorFilter`
- [ ] Query param: `?investor_id=1,2`
- [ ] Modificar query para filtrar por inversores asociados

#### **2.3 Ordenamiento de Resultados**
- [ ] Dropdown "Sort by": Valuation, Funding, ARR, Founded Year
- [ ] Query param: `?sort_by=valuation&order=desc`
- [ ] Backend aplica `order_by()` dinámicamente

#### **2.4 Paginación**
- [ ] Implementar offset/limit pagination
- [ ] Query params: `?page=1&page_size=20`
- [ ] Componente de paginación en frontend
- [ ] Metadata en respuesta: `{ total, page, page_size, total_pages }`

#### **2.5 Vista de Detalle de Empresa**
- [ ] Ruta: `/companies/[id]`
- [ ] Endpoint: `GET /api/v1/companies/{id}`
- [ ] Página con información expandida
- [ ] Gráficos de métricas (Chart.js o Recharts)

#### **2.6 Exportación de Datos**
- [ ] Botón "Export to CSV"
- [ ] Endpoint: `GET /api/v1/companies/export?format=csv`
- [ ] Generar CSV con datos filtrados
- [ ] Download automático en frontend

#### **2.7 Analytics Dashboard**
- [ ] Ruta: `/analytics`
- [ ] Gráficos agregados:
  - Distribución por industria (pie chart)
  - Distribución geográfica (bar chart)
  - Top 10 empresas por valoración
  - Promedio ARR por industria

#### **2.8 Performance Optimization**
- [ ] Implementar caché con Redis
- [ ] CDN para assets estáticos
- [ ] Image optimization (logos de empresas)
- [ ] Database indexes optimization
- [ ] Query optimization con EXPLAIN ANALYZE

#### **2.9 Autenticación (Opcional)**
- [ ] NextAuth.js en frontend
- [ ] OAuth2 con JWT en backend
- [ ] Perfiles de usuario
- [ ] Listas favoritas / Watchlists

---

## Fase 3: Datos Dinámicos y Administración

### Objetivo
Permitir actualización de datos y gestión administrativa.

### Alcance Propuesto

#### **3.1 CRUD de Empresas**
- [ ] Endpoints POST, PUT, DELETE para /api/v1/companies
- [ ] Validación completa con Pydantic
- [ ] Permisos de admin requeridos
- [ ] UI de administración en frontend

#### **3.2 Importación de Datos**
- [ ] Endpoint para upload de CSV
- [ ] Parser y validación de dataset
- [ ] Bulk insert en base de datos
- [ ] Reporte de errores/warnings

#### **3.3 Auditoría y Versionado**
- [ ] Triggers de auditoría en PostgreSQL
- [ ] Tabla de changelog
- [ ] UI para ver historial de cambios

#### **3.4 API Pública**
- [ ] Rate limiting
- [ ] API keys para autenticación
- [ ] Documentación pública detallada
- [ ] SDKs para Python/JavaScript

---

# Riesgos y Mitigaciones

## Riesgos Técnicos

### **Riesgo 1: Performance con Eager Loading**

**Descripción**: Cargar inversores anidados para 100 empresas podría generar queries lentas o problemas N+1.

**Probabilidad**: Media  
**Impacto**: Alto (afecta UX y tiempo de respuesta)

**Mitigación**:
- ✅ **Ya implementado**: Usar `selectinload()` de SQLAlchemy para eager loading eficiente
- ✅ **Monitoreo**: Ejecutar `EXPLAIN ANALYZE` en queries para verificar plan de ejecución
- ✅ **Fallback**: Si el performance es inaceptable, implementar endpoint separado `/companies/{id}/investors` y cargar bajo demanda
- ✅ **Índices**: Asegurar que existen índices en foreign keys (`industry_id`, `location_id`) y junction table
- ✅ **Benchmark**: Medir tiempo de respuesta, objetivo <500ms para 100 empresas

**Plan B**: Si eager loading no funciona bien, implementar lazy loading con endpoints separados en Fase 2.

---

### **Riesgo 2: Conexión a Supabase Inestable**

**Descripción**: Dependencia en servicio externo (Supabase) podría causar timeouts o errores de conexión.

**Probabilidad**: Baja  
**Impacto**: Alto (aplicación no funciona sin DB)

**Mitigación**:
- ✅ **Connection pooling**: Configurar pool de conexiones con límites apropiados
- ✅ **Retry logic**: Implementar reintentos automáticos con backoff exponencial
- ✅ **Timeout configuration**: Configurar timeouts razonables (5-10 segundos)
- ✅ **Health checks**: Endpoint `/health` que verifica conectividad con DB
- ✅ **Monitoreo**: Alertas si health check falla >2 veces consecutivas
- ✅ **Fallback**: Mensaje de error amigable en frontend con botón de retry

**Plan B**: Considerar migración a PostgreSQL self-hosted si Supabase muestra problemas recurrentes.

---

### **Riesgo 3: Incompatibilidad de Versiones (Python/Node)**

**Descripción**: Diferentes versiones de Python o Node.js entre desarrolladores podrían causar bugs inconsistentes.

**Probabilidad**: Media  
**Impacto**: Medio (frustración en desarrollo, bugs difíciles de reproducir)

**Mitigación**:
- ✅ **Documentación clara**: README especifica Python 3.12+ y Node.js 20+ LTS
- ✅ **Version managers**: Recomendar uso de `pyenv` para Python y `nvm` para Node.js
- ✅ **CI/CD validation**: Pipeline de CI ejecuta en versiones específicas
- ✅ **Lock files**: `uv.lock` para Python, `package-lock.json` para Node.js
- ✅ **Docker (opcional)**: Proveer Dockerfile con versiones exactas

**Plan B**: Si hay problemas persistentes, crear devcontainer con versiones controladas.

---

### **Riesgo 4: Datos Inconsistentes en Dataset**

**Descripción**: Dataset de Kaggle podría tener campos NULL, formatos inconsistentes, o datos faltantes.

**Probabilidad**: Media  
**Impacto**: Medio (afecta visualización y queries)

**Mitigación**:
- ✅ **Schema con NULLables**: Todos los campos opcionales marcados como `| None` en modelos
- ✅ **Validación en Pydantic**: Schemas validan tipos y permiten NULL
- ✅ **Formateo defensivo**: Frontend valida existencia antes de renderizar
- ✅ **Placeholders**: UI muestra "N/A" o "-" para campos faltantes
- ✅ **Data cleaning**: Scripts de limpieza antes de cargar a DB (ya ejecutados)

**Plan B**: Crear script de validación de datos que reporte problemas antes de deploy.

---

### **Riesgo 5: CORS Issues en Desarrollo/Producción**

**Descripción**: Configuración incorrecta de CORS podría bloquear requests entre frontend y backend.

**Probabilidad**: Media  
**Impacado**: Alto (aplicación no funciona)

**Mitigación**:
- ✅ **Configuración explícita**: CORSMiddleware con origins específicos
- ✅ **Variables de entorno**: `CORS_ORIGINS` configurable por ambiente
- ✅ **Testing temprano**: Probar integración frontend-backend en setup inicial
- ✅ **Documentación**: README incluye configuración de CORS
- ✅ **Wildcard en dev**: Permitir `http://localhost:3000` en desarrollo

**Plan B**: Usar proxy de Next.js (`rewrites` en `next.config.ts`) como alternativa.

---

## Riesgos de Alcance y Recursos

### **Riesgo 6: Scope Creep (Expansión de Alcance)**

**Descripción**: Agregar funcionalidades no planificadas durante desarrollo del MVP retrasa entrega.

**Probabilidad**: Alta  
**Impacto**: Medio (retraso en timeline)

**Mitigación**:
- ✅ **Definición clara de MVP**: Este documento especifica alcance mínimo viable
- ✅ **Priorización**: Fase 1 es MVP, Fase 2+ son mejoras post-lanzamiento
- ✅ **Registro de ideas**: Documentar features adicionales como backlog para Fase 2
- ✅ **Revisión regular**: Checkpoints semanales para validar progreso vs. plan
- ✅ **Criterios de aceptación**: MVP tiene criterios claros y medibles

**Plan B**: Si el tiempo es limitado, reducir alcance removiendo características no-core (e.g., búsqueda por nombre pasa a Fase 2).

---

### **Riesgo 7: Curva de Aprendizaje de Tecnologías**

**Descripción**: Equipo podría no estar familiarizado con FastAPI, Next.js App Router, o SQLAlchemy async.

**Probabilidad**: Media  
**Impacto**: Medio (desarrollo más lento inicialmente)

**Mitigación**:
- ✅ **Documentación oficial**: Links a docs de FastAPI, Next.js, SQLAlchemy en README
- ✅ **Ejemplos de código**: Este plan incluye snippets de código de referencia
- ✅ **Pair programming**: Sesiones de pair programming para compartir conocimiento
- ✅ **Spikes técnicos**: Dedicar tiempo inicial a prototipos de aprendizaje
- ✅ **Recursos externos**: Tutoriales, videos, cursos si es necesario

**Plan B**: Si la curva de aprendizaje es muy alta, considerar tecnologías más conocidas por el equipo (e.g., Django REST en lugar de FastAPI).

---

### **Riesgo 8: Testing Insuficiente**

**Descripción**: Falta de tests adecuados podría resultar en bugs en producción o refactoring riesgoso.

**Probabilidad**: Alta  
**Impacto**: Alto (calidad del código, mantenibilidad)

**Mitigación**:
- ✅ **Coverage mínimo**: Objetivo 60% definido en este plan
- ✅ **Tests como parte de Definition of Done**: No considerar tarea completa sin tests
- ✅ **CI/CD**: Pipeline ejecuta tests automáticamente en cada commit
- ✅ **Test-first approach**: Escribir tests antes de implementación cuando sea posible
- ✅ **Tipos de tests**: Unit tests (repositories, services), Integration tests (API endpoints), E2E tests (flujos completos)

**Plan B**: Si coverage es bajo, dedicar sprint específico a mejorar tests antes de producción.

---

## Riesgos de Datos y Seguridad

### **Riesgo 9: Exposición de Credenciales en Repositorio**

**Descripción**: Commit accidental de archivo `.env` con credenciales de Supabase.

**Probabilidad**: Media  
**Impacto**: Crítico (acceso no autorizado a DB)

**Mitigación**:
- ✅ **Gitignore**: `.env` y `.env.local` en `.gitignore` desde inicio
- ✅ **Ejemplos**: Proveer `.env.example` sin valores reales
- ✅ **Pre-commit hooks**: Hook que rechaza commits con patrones de credenciales
- ✅ **Git secrets**: Tool que escanea commits por secretos
- ✅ **Educación**: Recordatorio en README sobre no commitear secretos

**Plan B**: Si ocurre exposición, rotar credenciales de Supabase inmediatamente y revisar logs de acceso.

---

### **Riesgo 10: SQL Injection**

**Descripción**: Queries mal construidas podrían permitir SQL injection.

**Probabilidad**: Baja  
**Impacto**: Crítico (pérdida de datos, acceso no autorizado)

**Mitigación**:
- ✅ **ORM obligatorio**: Usar SQLAlchemy exclusivamente, nunca raw SQL sin parametrización
- ✅ **Validación Pydantic**: Todos los inputs validados por schemas Pydantic
- ✅ **Query params seguros**: FastAPI valida y parsea query params
- ✅ **Code review**: Revisar todo código que toque DB
- ✅ **Security scan**: Herramientas como Bandit para escanear código Python

**Plan B**: Realizar penetration testing antes de deploy a producción.

---

## Riesgos de UX y Producto

### **Riesgo 11: Performance Percibido en Frontend**

**Descripción**: Aunque la API sea rápida, el frontend podría sentirse lento sin feedback visual.

**Probabilidad**: Media  
**Impacto**: Medio (mala UX, usuarios frustrados)

**Mitigación**:
- ✅ **Loading states**: Skeleton screens mientras carga datos
- ✅ **Optimistic updates**: UI se actualiza inmediatamente al cambiar filtros
- ✅ **SWR cache**: Resultados cacheados para navegación back/forward
- ✅ **Debouncing**: En búsquedas futuras, evitar requests excesivos
- ✅ **Progressive enhancement**: App funciona sin JS (SSR)

**Plan B**: Implementar service worker para caché offline y mejorar perceived performance.

---

### **Riesgo 12: Usuarios No Encuentran Valor**

**Descripción**: Después de lanzar MVP, usuarios no ven utilidad o no se comprometen con la plataforma.

**Probabilidad**: Media  
**Impacto**: Alto (falta de adopción)

**Mitigación**:
- ✅ **Validación temprana**: Demo con usuarios target (inversionistas, analistas) antes de MVP final
- ✅ **Feedback loop**: Formulario de feedback en footer
- ✅ **Analytics**: Trackear métricas de uso (páginas vistas, filtros usados, tiempo en app)
- ✅ **Iteración rápida**: Ciclos cortos de feedback → mejora
- ✅ **Documentación clara**: Explicar casos de uso en landing page

**Plan B**: Si adopción es baja, pivotar hacia audiencia diferente o agregar features específicas de Fase 2 que agreguen más valor.

---

## Definición de Versión Inicial Viable

### Criterios Mínimos para Lanzar MVP

**Funcionalidad**:
- [x] Listado de 100 empresas con todas las métricas visible
- [x] Filtro por industria funcional
- [x] Filtro por ubicación funcional
- [x] Combinación de filtros funcional
- [x] URLs compartibles

**Calidad Técnica**:
- [x] Backend pasa linting, type checking, tests (>60% coverage)
- [x] Frontend pasa linting, type checking, build
- [x] No hay errores críticos en consola del navegador
- [x] API responde en <500ms para queries normales

**UX Básica**:
- [x] Loading states visibles
- [x] Error handling funcional
- [x] Responsive en mobile/desktop
- [x] Accesibilidad básica (keyboard nav, contraste)

### Qué NO es Necesario para MVP

- ❌ Búsqueda por nombre (Fase 2)
- ❌ Paginación (dataset es pequeño, Fase 2)
- ❌ Ordenamiento customizable (Fase 2)
- ❌ Filtro por inversor (Fase 2)
- ❌ Vista de detalle de empresa (Fase 2)
- ❌ Exportación de datos (Fase 2)
- ❌ Autenticación (Fase 3)
- ❌ CRUD de empresas (Fase 3)
- ❌ Gráficos/visualizaciones (Fase 2)
- ❌ Perfil de usuario (Fase 3)

**Principio**: Si la funcionalidad no es crítica para validar la propuesta de valor core (visualizar y filtrar empresas SaaS), se pospone para post-MVP.

---

# Apéndice

## A. Decisiones Arquitectónicas Registradas

### ADR-001: Uso de Eager Loading para Relaciones

**Contexto**: Las empresas tienen relaciones con industrias, ubicaciones e inversores. Necesitamos decidir cómo cargar estos datos relacionados.

**Decisión**: Usar eager loading con `selectinload()` de SQLAlchemy para cargar todas las relaciones en una o pocas queries.

**Consecuencias**:
- ✅ Una sola llamada API retorna datos completos
- ✅ Frontend más simple, sin múltiples requests
- ✅ Mejor performance para dataset pequeño (100 empresas)
- ⚠️ Queries más complejas en backend
- ⚠️ Payload de respuesta más grande

**Alternativas Consideradas**:
- Lazy loading con endpoints separados → rechazado por complejidad en frontend
- GraphQL → rechazado por over-engineering para MVP

---

### ADR-002: Sin Paginación en MVP

**Contexto**: El dataset tiene 100 empresas. Necesitamos decidir si implementar paginación desde el inicio.

**Decisión**: No implementar paginación en MVP. Retornar las 100 empresas completas.

**Consecuencias**:
- ✅ Desarrollo más rápido
- ✅ Filtros funcionan sobre dataset completo sin complejidad
- ✅ UX más simple (scroll infinito o ver todo)
- ⚠️ No escalable si dataset crece significativamente
- ✅ Preparado para agregar paginación en Fase 2 sin breaking changes (response ya tiene campo `total`)

**Alternativas Consideradas**:
- Paginación offset/limit desde inicio → rechazado por premature optimization
- Cursor-based pagination → rechazado por complejidad innecesaria

---

### ADR-003: Formateo de Números en Cliente (Frontend)

**Contexto**: Los datos financieros (funding, ARR, valuation) necesitan ser presentados de forma legible.

**Decisión**: Backend envía valores raw (números enteros), frontend aplica formateo con `Intl.NumberFormat`.

**Consecuencias**:
- ✅ Separación clara de responsabilidades (backend = datos, frontend = presentación)
- ✅ Flexibilidad para cambiar formato sin tocar backend
- ✅ Preparado para internacionalización (i18n)
- ✅ APIs más reutilizables (otros clientes pueden formatear a su gusto)
- ⚠️ Frontend debe implementar lógica de formateo

**Alternativas Consideradas**:
- Backend formatea y retorna strings → rechazado por falta de flexibilidad
- Ambos (raw + formatted) → rechazado por duplicación innecesaria

---

### ADR-004: Filtros vía Query Parameters en URL

**Contexto**: Los usuarios necesitan filtrar empresas por industria y ubicación.

**Decisión**: Implementar filtros como query parameters en la URL (`?industry_id=1&location_id=2`).

**Consecuencias**:
- ✅ URLs compartibles que mantienen estado de filtros
- ✅ Navegación back/forward funciona correctamente
- ✅ Deep linking posible
- ✅ SWR cachea resultados por combinación de filtros
- ✅ Estándar REST para filtrado
- ⚠️ URLs pueden volverse largas con muchos filtros

**Alternativas Consideradas**:
- Estado solo en frontend (React state) → rechazado por falta de shareability
- POST con body → rechazado por no ser RESTful para lectura

---

### ADR-005: Arquitectura por Capas en Backend

**Contexto**: Necesitamos organizar el código del backend de forma mantenible y testeable.

**Decisión**: Implementar arquitectura por capas: Router → Service → Repository → Model.

**Consecuencias**:
- ✅ Separación clara de responsabilidades
- ✅ Fácil de testear (unit tests por capa)
- ✅ Cambios en una capa no afectan otras
- ✅ Preparado para crecer (nuevos features en nuevos services)
- ⚠️ Más boilerplate inicial
- ⚠️ Curva de aprendizaje para arquitectura

**Alternativas Consideradas**:
- Código flat (routers llaman directamente a DB) → rechazado por pobre mantenibilidad
- Clean Architecture completa → rechazado por over-engineering en MVP

---

### ADR-006: Next.js App Router sobre Pages Router

**Contexto**: Next.js ofrece dos sistemas de routing: Pages Router (legacy) y App Router (moderno).

**Decisión**: Usar App Router con React Server Components.

**Consecuencias**:
- ✅ Aprovecha lo último de Next.js y React
- ✅ Mejor performance con Server Components por defecto
- ✅ Streaming y Suspense nativos
- ✅ Layouts compartidos más fáciles
- ⚠️ Curva de aprendizaje si el equipo conoce solo Pages Router
- ⚠️ Menos recursos/tutoriales comparado con Pages Router (aún)

**Alternativas Consideradas**:
- Pages Router → rechazado por ser legacy
- Remix o otros frameworks → rechazado por mayor adopción de Next.js

---

## B. Hallazgos de Investigación

### Dataset: Top 100 SaaS Companies (Kaggle)

**Fuente**: https://www.kaggle.com/datasets/shreyasdasari7/top-100-saas-companiesstartups

**Características**:
- 100 registros de empresas SaaS líderes
- Campos disponibles: Company Name, Industry, Location, Products/Services, Founded Year, Total Funding, Annual Revenue, Valuation, Investors
- Formato: CSV
- Última actualización: Verificar en Kaggle
- Limitaciones conocidas:
  - Algunos campos pueden tener valores NULL
  - Inversores pueden estar en formato texto separado por comas (requiere normalización)
  - Valoraciones pueden estar desactualizadas (dataset estático)

**Procesamiento Realizado**:
- Scripts SQL en `scripts/database/` para normalizar datos
- Tablas creadas: `company`, `industry`, `location`, `investor`, `company_investor`
- Datos cargados vía INSERT statements

---

### Tecnologías Evaluadas

#### **Backend Frameworks Considerados**

| Framework | Pros | Contras | Decisión |
|-----------|------|---------|----------|
| **FastAPI** | Async nativo, type hints, docs automáticos, moderno | Comunidad más pequeña que Django | ✅ **Seleccionado** |
| Django REST | Maduro, gran ecosistema, admin UI | Sync por defecto, más pesado | ❌ Rechazado (overkill) |
| Flask | Ligero, flexible | Menos features out-of-the-box | ❌ Rechazado (requiere más setup) |

#### **Frontend Frameworks Considerados**

| Framework | Pros | Contras | Decisión |
|-----------|------|---------|----------|
| **Next.js** | SSR/SSG, App Router, gran ecosistema, Vercel deploy | Curva de aprendizaje | ✅ **Seleccionado** |
| Create React App | Simple, conocido | No SSR, menos features | ❌ Rechazado (menos potente) |
| Vite + React | Rápido, moderno | Requiere más configuración | ❌ Rechazado (preferencia Next.js) |

#### **ORMs Considerados**

| ORM | Pros | Contras | Decisión |
|-----|------|---------|----------|
| **SQLAlchemy** | Maduro, async support, flexible | Más complejo que otros | ✅ **Seleccionado** |
| Tortoise ORM | Async-first, más simple | Comunidad pequeña | ❌ Rechazado (menos maduro) |
| Prisma (JS) | Excelente DX | Solo para JavaScript | ❌ No aplica (backend en Python) |

---

## C. Especificaciones Técnicas Detalladas

### Query de Eager Loading en SQLAlchemy

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def find_all_with_filters(
    db: AsyncSession,
    industry_ids: list[int] | None = None,
    location_ids: list[int] | None = None
) -> list[Company]:
    """
    Query optimizada con eager loading para evitar N+1 queries.
    
    Ejemplo de SQL generado:
    1. SELECT company.* FROM company WHERE industry_id IN (1, 2)
    2. SELECT industry.* FROM industry WHERE id IN (...)
    3. SELECT location.* FROM location WHERE id IN (...)
    4. SELECT investor.* FROM investor 
       JOIN company_investor ON investor.id = company_investor.investor_id
       WHERE company_investor.company_id IN (...)
    
    Total: 4 queries eficientes en lugar de 1 + N*3 (lazy loading)
    """
    query = select(Company).options(
        selectinload(Company.industry),
        selectinload(Company.location),
        selectinload(Company.investors)
    )
    
    if industry_ids:
        query = query.filter(Company.industry_id.in_(industry_ids))
    
    if location_ids:
        query = query.filter(Company.location_id.in_(location_ids))
    
    result = await db.execute(query)
    return result.scalars().all()
```

---

### Ejemplo de Respuesta API Completa

```json
{
  "data": [
    {
      "id": 1,
      "name": "Salesforce",
      "products": "Customer 360, Sales Cloud, Service Cloud, Marketing Cloud",
      "founding_year": 1999,
      "total_funding": 150000000,
      "arr": 31000000000,
      "valuation": 200000000000,
      "employees": 73000,
      "g2_rating": 4.3,
      "industry": {
        "id": 1,
        "name": "CRM"
      },
      "location": {
        "id": 1,
        "city": "San Francisco",
        "state": "CA",
        "country": "USA"
      },
      "investors": [
        {
          "id": 1,
          "name": "Sequoia Capital"
        },
        {
          "id": 2,
          "name": "Accel Partners"
        }
      ]
    },
    {
      "id": 2,
      "name": "Slack",
      "products": "Team Collaboration, Messaging, Workflow Automation",
      "founding_year": 2013,
      "total_funding": 1400000000,
      "arr": 900000000,
      "valuation": 27700000000,
      "employees": 2500,
      "g2_rating": 4.5,
      "industry": {
        "id": 3,
        "name": "Collaboration"
      },
      "location": {
        "id": 1,
        "city": "San Francisco",
        "state": "CA",
        "country": "USA"
      },
      "investors": [
        {
          "id": 2,
          "name": "Accel Partners"
        },
        {
          "id": 5,
          "name": "Andreessen Horowitz"
        }
      ]
    }
  ],
  "total": 100,
  "filters_applied": {}
}
```

---

### Configuración de SWR en Frontend

```typescript
// src/frontend/app/layout.tsx
import { SWRConfig } from 'swr';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <SWRConfig 
          value={{
            fetcher: (url: string) => fetch(url).then(r => r.json()),
            revalidateOnFocus: false,
            revalidateOnReconnect: true,
            dedupingInterval: 2000,
            errorRetryCount: 3,
          }}
        >
          {children}
        </SWRConfig>
      </body>
    </html>
  );
}
```

---

### Variables de Entorno Requeridas

#### **Backend** (`.env`)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# App
APP_NAME=Top SaaS Backend
APP_VERSION=1.0.0
ENVIRONMENT=development

# Optional
LOG_LEVEL=INFO
```

#### **Frontend** (`.env.local`)

```env
# API URL (public, expuesta al browser)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Optional
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
```

---

## D. Glosario de Términos

| Término | Definición |
|---------|-----------|
| **ARR** | Annual Recurring Revenue - Ingresos anuales recurrentes de la empresa |
| **Eager Loading** | Técnica de cargar relaciones en la misma query para evitar N+1 problem |
| **Lazy Loading** | Técnica de cargar relaciones bajo demanda, solo cuando se accede |
| **N+1 Problem** | Antipatrón donde se ejecuta 1 query inicial + N queries adicionales en loop |
| **Junction Table** | Tabla intermedia en relación muchos-a-muchos (e.g., `company_investor`) |
| **Schema** | En Pydantic: modelo de validación de datos. En DB: estructura de tablas |
| **Repository Pattern** | Patrón que abstrae acceso a datos, encapsula queries |
| **Service Layer** | Capa de lógica de negocio entre API y acceso a datos |
| **SWR** | Stale-While-Revalidate - Librería de data fetching para React |
| **SSR** | Server-Side Rendering - Renderizado en servidor |
| **CSR** | Client-Side Rendering - Renderizado en cliente |
| **Query Params** | Parámetros en URL después de `?` (e.g., `?industry_id=1`) |
| **Skeleton Screen** | Loading state que muestra estructura de contenido antes de cargar |

---

## E. Referencias y Recursos

### Documentación Oficial

- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **SWR**: https://swr.vercel.app/
- **Supabase**: https://supabase.com/docs

### Tutoriales y Guías

- FastAPI Best Practices: https://github.com/zhanymkanov/fastapi-best-practices
- Next.js App Router Tutorial: https://nextjs.org/learn
- SQLAlchemy Async Tutorial: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Repository Pattern in Python: https://www.cosmicpython.com/book/chapter_02_repository.html

### Herramientas de Desarrollo

- **uv**: https://github.com/astral-sh/uv (gestor de paquetes Python)
- **Ruff**: https://github.com/astral-sh/ruff (linter/formatter Python)
- **mypy**: https://mypy.readthedocs.io/ (type checker Python)
- **pytest**: https://docs.pytest.org/ (testing framework Python)
- **ESLint**: https://eslint.org/ (linter JavaScript/TypeScript)

---

## F. Contacto y Contribución

### Mantenedores del Proyecto

- **Nombre del equipo/proyecto**: Top SaaS Workshop
- **Repositorio**: https://github.com/mario-laserna/workshop-ia-nov2025

### Cómo Contribuir

1. Fork el repositorio
2. Crear branch de feature: `git checkout -b feature/nueva-funcionalidad`
3. Hacer commits con mensajes descriptivos (seguir Conventional Commits)
4. Ejecutar linting, type checking y tests antes de commit
5. Abrir Pull Request con descripción detallada
6. Esperar code review y aprobación

### Reporte de Bugs

Usar Issues de GitHub con template:
- **Descripción**: Qué está fallando
- **Pasos para reproducir**: Cómo reproducir el bug
- **Comportamiento esperado**: Qué debería pasar
- **Comportamiento actual**: Qué está pasando
- **Screenshots**: Si aplica
- **Ambiente**: Browser/OS, versiones de Python/Node

---

**Fin del Documento de Planeación**

*Última actualización: 11 de noviembre de 2025*  
*Versión: 1.0*
