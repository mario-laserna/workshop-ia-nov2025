---
applyTo: "src/frontend/**"
---

# Next.js con TypeScript

Propósito: generar componentes React, páginas, API routes y UI accesible, con separación de responsabilidades y seguridad.

- Estructura y convenciones:
  - Usar App Router (`app/` directory) por defecto para nuevos proyectos.
  - Carpetas típicas: `app/`, `components/`, `lib/`, `hooks/`, `types/`, `public/`.
  - Componentes pequeños y composables (Server Components por defecto, Client Components cuando sea necesario).
  - Usar `'use client'` solo cuando se necesite interactividad (hooks, event handlers, browser APIs).
  - Si un componente excede ~150 líneas, sugerir dividir en componentes más pequeños o extraer lógica a hooks personalizados.
  - TypeScript estricto: habilitar `strict: true` en `tsconfig.json`.
  - Usar tipos explícitos para props, estados y retornos de funciones.

- Routing y navegación:
  - Aprovechar file-based routing del App Router.
  - Usar `layout.tsx` para layouts compartidos y `loading.tsx` para estados de carga.
  - Implementar `error.tsx` para manejo de errores en segmentos de ruta.
  - Usar `next/link` para navegación client-side y `useRouter` de `next/navigation` cuando sea necesario.
  - Implementar rutas dinámicas con `[param]` y catch-all routes con `[...slug]`.

- Fetching de datos:
  - Preferir Server Components para fetching de datos (async/await directo en componentes).
  - Usar `fetch` con opciones de Next.js (`cache`, `next.revalidate`) para control de caché.
  - Para Client Components, usar SWR o React Query para fetching y caché de datos.
  - Crear servicios/API clients en `lib/` para centralizar llamadas a APIs externas.
  - Implementar tipos TypeScript para respuestas de API.

- API Routes:
  - Usar Route Handlers en `app/api/` para endpoints REST.
  - Exportar funciones nombradas (`GET`, `POST`, `PUT`, `DELETE`, etc.).
  - Validar request body con Zod o similar.
  - Manejar errores con `NextResponse` y códigos HTTP apropiados.
  - Nunca exponer secretos o claves API en el código cliente.

- Autenticación y autorización:
  - Usar NextAuth.js (Auth.js) para autenticación.
  - Implementar middleware para proteger rutas (`middleware.ts`).
  - Nunca incluir secretos en código; usar variables de entorno (`.env.local`).
  - Validar sesiones en Server Components y API Routes.

- Estilos y UI:
  - Usar Tailwind CSS como framework CSS preferido.
  - Implementar CSS Modules para estilos específicos de componentes cuando sea necesario.
  - Seguir principios de diseño responsive (mobile-first).
  - Usar `next/image` para optimización automática de imágenes.
  - Implementar dark mode con Tailwind o CSS variables.

- Accesibilidad y SEO:
  - Incluir atributos `aria-*` apropiados en componentes interactivos.
  - Usar elementos semánticos HTML (`<header>`, `<nav>`, `<main>`, `<footer>`).
  - Implementar metadata con `generateMetadata` o archivo `metadata` export.
  - Añadir Open Graph y Twitter Card meta tags.
  - Asegurar contraste de colores adecuado (WCAG AA mínimo).
  - Usar `next/font` para optimización de fuentes.

- Performance:
  - Implementar code splitting con dynamic imports (`next/dynamic`).
  - Usar Server Components para reducir JavaScript client-side.
  - Implementar streaming con Suspense boundaries.
  - Optimizar imágenes con `next/image` (lazy loading, responsive images).
  - Implementar caché estratégico con ISR (Incremental Static Regeneration).
  - Analizar bundle con `@next/bundle-analyzer`.

- State Management:
  - Preferir estado local (useState) y composición de componentes.
  - Usar Context API para estado compartido simple.
  - Para estado complejo global, usar Zustand o Jotai.
  - Evitar prop drilling excesivo; considerar composición o context.

- Tests:
  - Vitest o Jest para unit tests.
  - React Testing Library para tests de componentes.
  - Playwright o Cypress para E2E tests.
  - Coverage mínimo del 60%.
  - Tests en carpeta `src/frontend/__tests__/` para tests de componentes y utilidades.

- Tipos y validación:
  - Definir interfaces/types en archivos `.types.ts` o carpeta `types/`.
  - Usar Zod para validación de datos en runtime (forms, API responses).
  - Evitar `any`; usar `unknown` cuando el tipo sea incierto y validar.
  - Crear tipos reutilizables para entidades del dominio.

- Linting y formato:
  - ESLint con configuración de Next.js (`next lint`).
  - Prettier para formateo consistente.
  - Pre-commit hooks con Husky y lint-staged.
  - Ejecutar `npm run lint` y `npm run type-check` antes de commits.

- Ejemplos de prompts:
  - `// copilot: Crear Server Component ProductList que fetch productos desde /api/products y renderice ProductCard para cada uno.`
  - `// copilot: Crear Client Component UserCard con props UserDto (id, name, email) y callback onEdit. Usar Tailwind para estilos.`
  - `// copilot: Generar API Route Handler en app/api/products/route.ts con GET (listar) y POST (crear). Validar body con Zod.`
  - `// copilot: Crear custom hook useProducts que use SWR para fetch /api/products con tipos TypeScript y manejo de errores.`
  - `// copilot: Implementar middleware.ts para proteger rutas /dashboard/* verificando token JWT en cookies.`
  - `// copilot: Crear layout.tsx con navbar, footer y metadata SEO para sección /blog.`
