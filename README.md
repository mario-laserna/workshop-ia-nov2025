# Workshop IA - Noviembre 2025

Proyecto full-stack para workshop de Inteligencia Artificial usando FastAPI (Backend) y Next.js (Frontend).

## 🏗️ Estructura del Proyecto

```
workshop-ia-nov2025-prep/
├── src/
│   ├── backend/          # API FastAPI (Python 3.12+, uv)
│   └── frontend/         # App Next.js 16 (TypeScript, React 19)
├── scripts/
│   ├── database/         # Scripts SQL y dataset
│   └── dev/              # Scripts de desarrollo (run-backend.sh, run-frontend.sh)
├── docs/adrs/            # Decisiones arquitectónicas
│
│   # Tests dentro de cada proyecto:
│   # src/backend/tests/       - Tests del backend (pytest)
│   # src/frontend/__tests__/  - Tests del frontend (Vitest)
```

## 🚀 Quick Start

### Requisitos
- **Backend**: Python 3.12+ y `uv`
- **Frontend**: Node.js 18+ y `npm`

### ⚠️ Configuración Inicial (una sola vez)

```bash
# Backend
cd src/backend
cp .env.example .env
uv sync

# Frontend (en otra terminal)
cd src/frontend
cp .env.local.example .env.local
npm install
```

### 🎯 Ejecutar la Aplicación

**Usa terminales separadas para cada servidor:**

**Terminal 1 - Backend (http://localhost:8000):**
```bash
./scripts/dev/run-backend.sh
```

**Terminal 2 - Frontend (http://localhost:3000):**
```bash
./scripts/dev/run-frontend.sh
```

### 📍 URLs Importantes
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## ✅ Verificación

Abre http://localhost:3000 y verifica que el componente "Backend Status" muestre:
- Status: **healthy** ✅
- Version: **1.0.0**
- Environment: **development**
- Auto-refresh cada 30 segundos

**Troubleshooting:** Si no ves status "healthy", verifica que ambos servidores estén corriendo y las variables de entorno configuradas correctamente.

## 🛠️ Stack Tecnológico

| Backend | Frontend |
|---------|----------|
| Python 3.12 + FastAPI | TypeScript + Next.js 16 |
| uv (gestor de paquetes) | npm |
| Pydantic (validación) | React 19 (App Router) |
| Ruff + MyPy (calidad) | Tailwind CSS |
| Uvicorn (servidor ASGI) | SWR (data fetching) |

## 📋 Comandos Útiles

### Backend (desde `src/backend/`)
```bash
uv run ruff format .          # Formateo
uv run ruff check .           # Linting
uv run mypy .                 # Type checking
uv run pytest                 # Tests
```

### Frontend (desde `src/frontend/`)
```bash
npm run dev                   # Desarrollo
npm run build                 # Build producción
npm run lint                  # Linting
npm test                      # Tests
```

## 🏛️ Arquitectura

**Backend (Patrón por capas):**
- `api/` → Routers (endpoints HTTP)
- `services/` → Lógica de negocio
- `repositories/` → Acceso a datos
- `schemas/` → Validación (Pydantic)

**Frontend (Next.js App Router):**
- `app/` → Pages y layouts
- `components/` → Componentes React
- `lib/` → Utilidades, tipos, API client

## 🔐 Variables de Entorno

Copiar archivos de ejemplo y configurar:
- **Backend**: `src/backend/.env.example` → `.env`
- **Frontend**: `src/frontend/.env.local.example` → `.env.local`

## 📝 Convenciones de Código

**Reglas generales:**
- Máximo **500 líneas por archivo**
- Type hints/tipos explícitos obligatorios
- Coverage mínimo: **60%**

**Python:** `snake_case` (funciones/vars), `PascalCase` (clases), docstrings Google  
**TypeScript:** `camelCase` (funciones/vars), `PascalCase` (componentes), prefijo `use` (hooks)

Ver [`.github/instructions/coding-rules.instructions.md`](.github/instructions/coding-rules.instructions.md) para detalles completos.

## 🧪 Testing

### Backend
```bash
cd src/backend
uv run pytest
```

### Frontend
```bash
cd src/frontend
npm test
```

## 📖 Documentación

- [Instrucciones Generales (Copilot)](.github/copilot-instructions.md)
- [Reglas de Codificación](.github/instructions/coding-rules.instructions.md)
- [Instrucciones Frontend](.github/instructions/frontend.instructions.md)
- [Instrucciones Backend](.github/instructions/backend.instructions.md)

## 📄 License

Este proyecto es parte del Workshop IA - Noviembre 2025 de Manuel Zapata.

---

**Workshop IA - Noviembre 2025** | [Manuel Zapata](https://manuelzapata.gumroad.com/l/workshop-guiado-ai)
