# 2. Arquitectura por capas (Router - Service - Repository)

Fecha: Febrero 17 de 2026

## Status

Aceptada.

## Contexto

El backend necesita una estructura clara que separe responsabilidades para facilitar el mantenimiento, la testabilidad y la escalabilidad del codigo. Se requiere definir como organizar routers, logica de negocio y acceso a datos.

## Decision

Adoptamos el patron de capas Router - Service - Repository con inyeccion de dependencias via `Depends()` de FastAPI.

- **Router**: recibe requests HTTP, valida parametros y delega al servicio.
- **Service**: contiene logica de negocio y orquesta llamadas al repositorio.
- **Repository**: encapsula el acceso a datos via el cliente Supabase.

Alternativas evaluadas:
- **Logica directa en routers**: simple pero no escalable ni testeable de forma aislada.
- **Patron CQRS**: sobredimensionado para la complejidad actual del proyecto.
- **Arquitectura hexagonal**: mayor abstraccion de la necesaria para este alcance.

## Consecuencias

- Mas archivos y boilerplate por la separacion en capas.
- Clara separacion de responsabilidades entre capas.
- Facilidad de testing unitario con mocks en cada capa.
- Escalabilidad del codigo al agregar nuevas funcionalidades.
