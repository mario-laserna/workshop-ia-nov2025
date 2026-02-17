# Diagrama C4 - Nivel 2: Contenedores del Sistema

## Descripcion

Este diagrama muestra los contenedores que componen el sistema **Top SaaS Dashboard** y sus interacciones.

### Contenedores

| Contenedor | Tecnologia | Responsabilidad |
|---|---|---|
| **Frontend** | Next.js 16 (React, TypeScript) | Interfaz web del dashboard. Renderiza tabla de empresas, filtros y paginacion. Server Components para data fetching. |
| **Backend API** | FastAPI (Python 3.12+) | API REST que expone endpoints de empresas, industrias y ubicaciones con filtros y paginacion. |
| **Base de datos** | PostgreSQL (Supabase) | Almacena datos de empresas SaaS, industrias, ubicaciones e inversores. Acceso via PostgREST. |

### Protocolos de comunicacion

- **Frontend → Backend API**: HTTP/REST (JSON) por puerto 8000
- **Backend API → Base de datos**: HTTP/PostgREST via SDK de Supabase

## Diagrama

```mermaid
C4Container
    title Diagrama de Contenedores - Top SaaS Dashboard

    Person(user, "Inversionista / Analista", "Consulta metricas de empresas SaaS.")

    System_Boundary(b0, "Top SaaS Dashboard") {
        Container(frontend, "Frontend", "Next.js 16, TypeScript", "Dashboard web con filtros, tabla de empresas y paginacion.")
        Container(backend, "Backend API", "FastAPI, Python 3.12+", "API REST con endpoints de empresas, industrias y ubicaciones.")
        ContainerDb(db, "Base de Datos", "PostgreSQL / Supabase", "Almacena empresas, industrias, ubicaciones e inversores.")
    }

    Rel(user, frontend, "Consulta dashboard", "HTTPS")
    Rel(frontend, backend, "Solicita datos", "HTTP/REST JSON")
    Rel(backend, db, "Consulta datos", "HTTP/PostgREST")
```
