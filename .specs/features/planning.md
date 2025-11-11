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
- **Backend**: FastAPI con Python, SQLAlchemy (async) y Pydantic.
- **Base de datos**: PostgreSQL en Supabase.

## Modelos de datos
- `Company`: Tabla principal con métricas y relaciones a `Industry` y `Location`.
- `Industry`: Tabla normalizada de industrias.
- `Location`: Tabla normalizada de ubicaciones.
- `Investor`: Tabla normalizada de inversores.
- `CompanyInvestor`: Tabla de unión para la relación N:M entre empresas e inversores.

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
    -   Configurar `pyproject.toml` con dependencias: `fastapi`, `uvicorn`, `sqlalchemy[asyncio]`, `psycopg2-binary`, `pydantic-settings`.
    -   Crear estructura de directorios: `api/`, `core/`, `models/`, `repositories/`, `schemas/`, `services/`.
2.  **Conexión a Base de Datos**:
    -   Implementar `core/config.py` para gestionar variables de entorno (`DATABASE_URL`) con Pydantic-Settings.
    -   Crear `core/database.py` para gestionar la sesión de SQLAlchemy asíncrona.
3.  **Modelos y Schemas**:
    -   Crear los modelos de SQLAlchemy en `models/` para `Company`, `Industry`, `Location`, `Investor`.
    -   Definir los schemas de Pydantic en `schemas/` para las respuestas de la API (ej. `CompanyRead`, `IndustryRead`). Incluir el schema para la lista de inversores anidada.
4.  **Capa de Acceso a Datos (Repositories)**:
    -   Implementar `repositories/company_repository.py` con métodos asíncronos para obtener empresas, aplicando filtros combinados (AND) por industria y ubicación. Usar `joinedload` para incluir eficientemente industrias, ubicaciones e inversores.
    -   Implementar `repositories/industry_repository.py` y `location_repository.py` con métodos para obtener todos los registros.
5.  **Capa de Lógica de Negocio (Services)**:
    -   Crear `services/company_service.py` que utilice los repositorios para obtener y procesar los datos.
6.  **Capa de API (Routers)**:
    -   Implementar los endpoints en `api/`:
        -   `GET /api/v1/companies`: Router que inyecta el servicio y devuelve la lista de empresas.
        -   `GET /api/v1/industries` y `GET /api/v1/locations`: Routers para los datos de los filtros.
        -   `GET /api/v1/health`: Endpoint de chequeo de salud.
7.  **Pruebas Unitarias/Integración**:
    -   Añadir pruebas para los endpoints usando `TestClient` de FastAPI.

## Fase 2: Frontend (UI y Conexión)
1.  **Configuración del entorno Frontend**:
    -   Verificar `package.json` con dependencias: `next`, `react`, `tailwindcss`.
    -   Estructura de directorios: `app/`, `components/`, `lib/`, `types/`.
2.  **Tipos de Datos**:
    -   Definir interfaces en `types/` que coincidan con los schemas de la API del backend.
3.  **Cliente de API**:
    -   Crear `lib/api.ts` con funciones para hacer fetch a los endpoints del backend (`getCompanies`, `getIndustries`, `getLocations`).
4.  **Componentes de UI**:
    -   `components/CompanyTable.tsx`: Componente que renderiza una tabla (`<table>`) con los datos de las empresas.
    -   `components/Filters.tsx`: Componente (cliente) con los `selects` para industria y ubicación. Gestionará la actualización de los query params de la URL.
5.  **Página Principal (Dashboard)**:
    -   Modificar `app/page.tsx` para que sea un Server Component.
    -   Leerá los `searchParams` de la URL para pasarlos a `lib/api.ts`.
    -   Hará fetch de los datos de empresas, industrias y ubicaciones.
    -   Renderizará el componente `Filters` y `CompanyTable`.
6.  **Estilos**:
    -   Aplicar estilos con Tailwind CSS para asegurar una interfaz limpia y responsive.

# Riesgos y Mitigaciones
-   **Riesgo**: Complejidad en la consulta de inversores anidados que afecte el rendimiento.
    -   **Mitigación**: Uso de `joinedload` en SQLAlchemy para asegurar una consulta SQL eficiente y evitar el problema N+1. Realizar pruebas de carga tempranas.
-   **Riesgo**: Sincronización del estado de los filtros en el frontend.
    -   **Mitigación**: Adoptar el patrón de estado en la URL (query params) desde el principio, que se alinea con las mejores prácticas de Next.js App Router y simplifica la lógica a largo plazo.
-   **Riesgo**: Desacople entre los schemas del backend y los tipos del frontend.
    -   **Mitigación**: Mantener una comunicación fluida entre equipos o, en un futuro, considerar un monorepo con un paquete de tipos compartido.

# Apéndice
-   **Dataset**: [Top 100 SaaS Companies on Kaggle](https://www.kaggle.com/datasets/shreyasdasari7/top-100-saas-companiesstartups)
-   **Esquema DB**: Ver `scripts/database/01-top-saas-db-creation.sql`.
