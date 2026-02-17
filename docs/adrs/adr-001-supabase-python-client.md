# 1. Supabase Python async client para acceso a datos

Fecha: Febrero 17 de 2026

## Status

Aceptada.

## Contexto

El backend (FastAPI) necesita acceder a una base de datos PostgreSQL hospedada en Supabase. La base de datos ya existe y está poblada con datos de empresas SaaS, industrias, ubicaciones e inversores.

Se requiere un cliente que permita realizar queries asíncronas desde FastAPI sin necesidad de gestionar modelos ORM ni migraciones.

## Decisión

Usamos la librería oficial `supabase-py` con el cliente async (`supabase._async.create_client`) para acceder a los datos vía PostgREST.

Alternativas evaluadas:
- **SQLAlchemy async + asyncpg**: acceso SQL directo, pero requiere definir modelos ORM y gestionar conexiones manualmente.
- **postgrest-py**: cliente PostgREST sin el SDK completo de Supabase.
- **Raw HTTP a PostgREST**: máximo control, pero reimplementa funcionalidad ya disponible en el SDK.

## Consecuencias

- No se requieren modelos ORM; las queries se realizan vía API REST (PostgREST).
- Se necesitan las variables de entorno `SUPABASE_URL` y `SUPABASE_KEY`.
- Menor complejidad de configuración al usar el SDK oficial.
- Dependencia directa del servicio Supabase y su disponibilidad.
