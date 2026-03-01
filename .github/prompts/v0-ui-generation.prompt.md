<!-- 
Este fue el prompt diseñado por el agente para crear el diseño de la UI del dashboard usando la herramienta v0 de Vercel. El prompt incluye el contexto del proyecto, los ADRs relevantes, las especificaciones de la UI y las especificaciones de la funcionalidad. El diseño se enfoca en un dashboard oscuro para analistas e inversionistas que evalúan empresas SaaS, con un layout claro y profesional, utilizando Tailwind CSS y siguiendo las mejores prácticas de accesibilidad.
 -->
Diseña un dashboard oscuro (tema slate-900/800) para analistas/inversionistas que evalúan empresas SaaS.

Layout
Header: título "Top SaaS Dashboard", subtítulo descriptivo.
Filtros: 2 dropdowns (Industria, Ubicación) + botón "Limpiar filtros", alineados horizontalmente.
Tabla HTML (<table>) con columnas: Nombre, Industria, Ubicación, Productos, Año Fundación, Total Inversión, Ingresos Anuales, Valoración. Moneda formateada ($X.XM/$X.XB). Scroll horizontal en mobile (overflow-x-auto).
Paginación: botones Anterior/Siguiente (disabled en límites), "Página X de Y", total registros.
Empty state: mensaje cuando no hay resultados.
Loading state: skeleton con animate-pulse para tabla, filtros y paginación.
Error state: mensaje de error + botón "Reintentar".
Decisiones arquitectónicas
Filtros reflejados en URL search params (compartibles).
Tabla es Server Component (datos como props).
Filtros y Paginación son Client Components (interactividad).
Estilo
Tailwind CSS, tema oscuro, tipografía Geist. Diseño profesional, minimalista, responsivo. Contraste WCAG AA.