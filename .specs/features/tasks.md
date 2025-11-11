# Plan de Tareas: Análisis de Empresas SaaS

Este documento desglosa el plan de `planning.md` en tareas ejecutables.

## Épica 1: Diseño y Arquitectura

### Diseño de Arquitectura (ADRs)
- [ ] **ADR-001**: Documentar la decisión sobre la estrategia de renderizado y estado en el Frontend.
- [ ] **ADR-002**: Documentar la decisión sobre el diseño de la respuesta de la API para datos relacionados.
- [ ] **ADR-003**: Documentar la decisión sobre la gestión de secretos de la Base de Datos (Supabase).

### Diseño de Diagramas (C4 y ER)
- [ ] **Diagrama C4 - Contexto**: Crear el diagrama de contexto del sistema usando MermaidJS.
- [ ] **Diagrama C4 - Contenedores**: Crear el diagrama de contenedores (Frontend, Backend, Supabase) usando MermaidJS.
- [ ] **Diagrama Entidad-Relación (ER)**: Crear el diagrama ER basado en `01-top-saas-db-creation.sql` usando MermaidJS.

### Documentación de Arquitectura
- [ ] Integrar los diagramas (C4, ER) en un archivo `docs/architecture.md`.

## Épica 2: Desarrollo del Backend (API Core)

### Configuración del Entorno
- [ ] Configurar `pyproject.toml` con dependencias: `fastapi`, `uvicorn`, `supabase-py`, `pydantic-settings`.
- [ ] Crear la estructura de directorios: `src/backend/api/`, `core/`, `repositories/`, `schemas/`, `services/`.
- [ ] Configurar `uv` y el entorno virtual.

### Conexión a Supabase
- [ ] Implementar `src/backend/core/config.py` para gestionar `SUPABASE_URL` y `SUPABASE_KEY` con `pydantic-settings`.
- [ ] Crear archivo `.env.example` con las variables de entorno de Supabase.
- [ ] Implementar `src/backend/core/supabase.py` para inicializar y exponer el cliente de Supabase.

### Schemas Pydantic
- [ ] Definir schemas Pydantic en `src/backend/schemas/` para las respuestas de la API (`CompanyRead`, `IndustryRead`, etc.), incluyendo datos anidados para los inversores.

### Capa de Acceso a Datos (Repositories)
- [ ] Implementar `src/backend/repositories/company_repository.py` con método que use el cliente de `supabase-py` para obtener empresas, aplicando filtros y seleccionando datos relacionados.
- [ ] Implementar `src/backend/repositories/industry_repository.py` con método para obtener todas las industrias.
- [ ] Implementar `src/backend/repositories/location_repository.py` con método para obtener todas las ubicaciones.

### Capa de Lógica de Negocio (Services)
- [ ] Implementar `src/backend/services/company_service.py` que utilice los repositorios.

### Capa de API (Routers)
- [ ] Implementar `src/backend/api/health.py` con el endpoint `GET /api/v1/health`.
- [ ] Implementar `src/backend/api/companies.py` con el endpoint `GET /api/v1/companies`.
- [ ] Implementar `src/backend/api/industries.py` con el endpoint `GET /api/v1/industries`.
- [ ] Implementar `src/backend/api/locations.py` con el endpoint `GET /api/v1/locations`.
- [ ] Integrar los routers en `src/backend/main.py`.

## Épica 3: Pruebas del Backend (Servicios y Endpoints)

### Configuración de Pruebas
- [ ] Configurar el entorno de pruebas con `pytest` y `unittest.mock`.
- [ ] Crear fixtures para el cliente de API (`TestClient`).

### Implementación de Pruebas
- [ ] **Pruebas de Servicios (Unitarias)**:
    - [ ] Crear pruebas para `company_service.py` usando mocks para simular las respuestas del repositorio (cliente de Supabase).
- [ ] **Pruebas de Endpoints (Integración)**:
    - [ ] Crear pruebas para `GET /api/v1/companies` (casos con y sin filtros), mockeando la capa de servicio.
    - [ ] Crear pruebas para `GET /api/v1/industries` y `GET /api/v1/locations`.
    - [ ] Crear pruebas para `GET /api/v1/health`.

## Épica 4: Desarrollo del Frontend (UI)

### Configuración del Entorno
- [ ] Verificar dependencias en `package.json`.
- [ ] Crear la estructura de directorios: `src/frontend/components/`, `lib/`, `types/`.

### Desarrollo de la Lógica
- [ ] Definir interfaces en `src/frontend/types/` que coincidan con los schemas de la API.
- [ ] Implementar `src/frontend/lib/api.ts` con funciones `fetch` para `getCompanies`, `getIndustries`, y `getLocations`.

### Desarrollo de Componentes de UI
- [ ] Crear componente `src/frontend/components/Filters.tsx` con selects para industria y ubicación.
- [ ] Crear componente `src/frontend/components/CompanyTable.tsx` para renderizar los datos en una tabla.
- [ ] Aplicar estilos base con Tailwind CSS a los componentes.

### Integración de la Página
- [ ] Modificar `src/frontend/app/page.tsx` para que sea un Server Component.
- [ ] Implementar la lectura de `searchParams` para pasarlos a la función `getCompanies`.
- [ ] Renderizar los componentes `Filters` y `CompanyTable` en la página principal.