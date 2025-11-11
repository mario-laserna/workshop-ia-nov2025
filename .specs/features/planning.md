# Descripción General
Esta aplicación es una herramienta de análisis de empresas SaaS para inversionistas. Proporciona un dashboard interactivo para visualizar y filtrar métricas clave de las 100 compañías más importantes del sector, utilizando un stack tecnológico moderno con FastAPI en el backend y Next.js en el frontend.

# Funcionalidades Principales
- **Listado de Empresas**: Visualización de las métricas más importantes de las empresas SaaS en un formato tabular.
- **Filtros dinámicos**: Búsqueda y filtrado combinado (tipo AND) de empresas por industria y ubicación.
- **API RESTful**: Backend que expone los datos de empresas, industrias y ubicaciones.

# Experiencia de Usuario
- **Perfil de usuario**: Inversionistas y analistas de mercado.
- **Flujo clave**: El usuario accede al dashboard, visualiza la lista completa de empresas en una **tabla**, y utiliza los filtros para acotar la búsqueda según sus criterios de interés (industria o ubicación). La interfaz debe ser rápida, intuitiva y mostrar los datos de forma clara.

# Arquitectura

## Componentes del sistema
- **Frontend**: Next.js (App Router) con TypeScript y Tailwind CSS.
- **Backend**: FastAPI con Python, **supabase-py** y Pydantic.
- **Base de datos**: PostgreSQL en Supabase.

## Patrón de arquitectura (Backend)
```
FastAPI (Routers)
    ↓
Services (lógica de negocio)
    ↓
Repositories (acceso a datos con supabase-py)
    ↓
PostgreSQL (Supabase)
```

## APIs e integraciones
- **API interna**: El frontend consume una API RESTful proporcionada por el backend de FastAPI.
  - `GET /api/v1/companies`: Devuelve la lista de empresas. Acepta filtros combinados (AND) por `industry_id` y `location_id`. Devuelve los inversores anidados.
  - `GET /api/v1/industries`: Devuelve la lista de industrias para los filtros.
  - `GET /api/v1/locations`: Devuelve la lista de ubicaciones para los filtros.
- **Ejemplos de URLs con Query Params**:
  - **Listado completo (sin filtros):** `GET /api/v1/companies`
  - **Filtrado por industria:** `GET /api/v1/companies?industry_id=5`
  - **Filtrado por ubicación:** `GET /api/v1/companies?location_id=10`
  - **Filtro combinado (AND):** `GET /api/v1/companies?industry_id=5&location_id=10`

# Hoja de Ruta de Desarrollo

## Fase 1: Backend (API Core)
1.  **Configuración del entorno Backend**:
    -   Configurar `pyproject.toml` con dependencias: `fastapi`, `uvicorn`, `supabase-py`, `pydantic-settings`.
    -   Crear estructura de directorios: `api/`, `core/`, `repositories/`, `schemas/`, `services/`.
2.  **Conexión a Supabase**:
    -   Implementar `core/config.py` para gestionar variables de entorno (`SUPABASE_URL`, `SUPABASE_KEY`) con Pydantic-Settings.
    -   Crear `core/supabase.py` para inicializar y exponer el cliente de Supabase.
3.  **Schemas Pydantic**:
    -   Definir los schemas en `schemas/` para las respuestas de la API (ej. `CompanyRead`, `IndustryRead`). Incluir el schema para la lista de inversores anidada.
4.  **Capa de Acceso a Datos (Repositories)**:
    -   Implementar `repositories/company_repository.py` con métodos que usen el cliente de `supabase-py` para obtener empresas, aplicando filtros y seleccionando datos relacionados (`select('*, industry(*), ...')`).
    -   Implementar `repositories/industry_repository.py` y `location_repository.py`.
5.  **Capa de Lógica de Negocio (Services)**:
    -   Crear `services/company_service.py` que utilice los repositorios.
6.  **Capa de API (Routers)**:
    -   Implementar los endpoints en `api/` para `companies`, `industries`, `locations` y `health`.
7.  **Pruebas (con Mocks)**:
    -   Añadir pruebas para servicios y endpoints, usando `unittest.mock` para simular las respuestas del cliente de Supabase.

## Fase 2: Frontend (UI y Conexión)
1.  **Configuración del entorno Frontend**:
    -   Verificar `package.json` y estructura de directorios.
2.  **Tipos y Cliente de API**:
    -   Definir interfaces en `types/` y crear `lib/api.ts` para hacer fetch a los endpoints.
3.  **Componentes de UI**:
    -   `components/CompanyTable.tsx`: Componente para renderizar la tabla de datos.
    -   `components/Filters.tsx`: Componente cliente para los filtros.
4.  **Página Principal (Dashboard)**:
    -   Modificar `app/page.tsx` para leer `searchParams`, hacer fetch de los datos y renderizar los componentes.
5.  **Estilos**:
    -   Aplicar estilos con Tailwind CSS.

# Riesgos y Mitigaciones
-   **Riesgo**: Rendimiento en la consulta de datos anidados con `supabase-py`.
    -   **Mitigación**: Utilizar la sintaxis de `select` de Supabase para construir una única consulta eficiente que obtenga todos los datos relacionados, evitando el problema N+1.
-   **Riesgo**: Sincronización del estado de los filtros en el frontend.
    -   **Mitigación**: Adoptar el patrón de estado en la URL (query params), alineado con las mejores prácticas de Next.js App Router.
-   **Riesgo**: Desacople entre los schemas del backend y los tipos del frontend.
    -   **Mitigación**: Mantener una comunicación fluida o considerar un monorepo con tipos compartidos.

# Apéndice
-   **Dataset**: [Top 100 SaaS Companies on Kaggle](https://www.kaggle.com/datasets/shreyasdasari7/top-100-saas-companiesstartups)
-   **Esquema DB**: Ver `scripts/database/01-top-saas-db-creation.sql`.
