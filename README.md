# Plantilla de Proyecto ITE

Plantilla base de ITE para encargos nuevos. Stack completo con backend FastAPI + PostgreSQL, frontend React + TypeScript, y CI configurado que bloquea el merge si los tests fallan.

## Requisitos previos

Software necesario:

- **Python 3.11+**
- **Node.js 20+**
- **PostgreSQL 15+** (solo para desarrollo local sin Docker)
- **Docker + Docker Compose** (recomendado)
- **uv** (gestor de dependencias Python)
- **pnpm** (gestor de dependencias Node.js)

### Instalación de PostgreSQL por sistema operativo

- **macOS:** `brew install postgresql@15`
- **Ubuntu/Debian:** `sudo apt-get install postgresql-15`
- **Windows:** Descargar instalador desde [postgresql.org](https://www.postgresql.org/download/windows/)

## Instalación y configuración

### Opción A: Desarrollo local

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto
   ```

2. **Instalar PostgreSQL localmente** (ver sección de requisitos previos)

3. **Crear base de datos**
   ```bash
   createdb app_db
   ```

4. **Backend**
   ```bash
   cd backend
   uv sync
   export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/app_db"
   uv run alembic upgrade head
   uv run uvicorn src.main:app --reload
   ```

5. **Frontend**
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

### Opción B: Docker (recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto
   ```

2. **Levantar servicios**
   ```bash
   make docker-up
   # o: docker-compose up -d
   ```

3. **Ejecutar migraciones**
   ```bash
   make db-migrate
   # o: docker-compose exec backend uv run alembic upgrade head
   ```

4. **Acceder a los servicios**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:5173
   - PostgreSQL: localhost:5432

## Comandos disponibles (Makefile)

| Comando | Descripción |
|---------|-------------|
| `make install` | Instala dependencias backend + frontend |
| `make test` | Ejecuta tests backend + frontend |
| `make lint` | Ejecuta linters backend + frontend |
| `make coverage` | Reporte de cobertura de tests |
| `make docker-up` | Levanta servicios con docker-compose |
| `make docker-down` | Baja servicios docker-compose |
| `make db-migrate` | Ejecuta migraciones Alembic |
| `make db-seed` | Carga datos de ejemplo en PostgreSQL |
| `make clean` | Limpia archivos temporales |

## Comandos de base de datos

### Crear migración nueva
```bash
cd backend
uv run alembic revision --autogenerate -m "descripción"
```

### Ejecutar migraciones
```bash
uv run alembic upgrade head
```

### Revertir última migración
```bash
uv run alembic downgrade -1
```

### Ver historial de migraciones
```bash
uv run alembic history
```

### Acceder a PostgreSQL shell

**Docker:**
```bash
docker-compose exec postgres psql -U app_user -d app_db
```

**Local:**
```bash
psql -U app_user -d app_db
```

## Ejecutar tests

### Backend
```bash
cd backend
uv run pytest                # tests básicos
uv run pytest -v             # verbose
uv run pytest --cov          # con cobertura
```

### Frontend
```bash
cd frontend
pnpm test                    # tests básicos
pnpm test:coverage           # con cobertura
```

### Todo a la vez
```bash
make test
```

## CI/CD

El proyecto incluye GitHub Actions configurado (`.github/workflows/ci.yml`) que:

- Ejecuta tests backend con servicio PostgreSQL
- Ejecuta tests frontend
- Ejecuta linters
- **Bloquea el merge si algo falla**

### Habilitar protección de merge en GitHub

1. **Settings → Branches → Add rule**
2. **Branch name pattern:** `main`
3. **Habilitar:**
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
     - Marcar: `backend-tests`, `frontend-tests`
   - ✅ Require branches to be up to date before merging
4. **Save changes**

Esto asegura que ningún PR puede mergearse a `main` sin que pasen todos los tests.

## Estándar de "done" de ITE

Este proyecto cumple el estándar de done definido en [ITE-3](/ITE/issues/ITE-3):

- [x] Tests unitarios existen y pasan
- [x] Tests de integración con PostgreSQL existen y pasan
- [x] Linters configurados y pasan
- [x] CI configurado en GitHub Actions
- [x] CI ejecuta tests + linters
- [x] Branch protection configurado para bloquear merge si CI falla
- [x] README completo con instrucciones de instalación y uso
- [x] Docker configurado para desarrollo

## Estructura del proyecto

```
proyecto/
├── backend/                 # FastAPI + PostgreSQL
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── models/
│   ├── tests/
│   ├── alembic/
│   ├── pyproject.toml
│   └── alembic.ini
├── frontend/                # React + TypeScript
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── components/
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de CI
├── docker-compose.yml      # Servicios Docker
├── Makefile                # Comandos disponibles
├── .gitignore
└── README.md
```

## Próximos pasos

Si vas a usar esta plantilla en un encargo nuevo:

1. **Hacer fork o copiar esta plantilla**
   ```bash
   git clone <url-plantilla> mi-nuevo-proyecto
   cd mi-nuevo-proyecto
   rm -rf .git
   git init
   ```

2. **Renombrar el proyecto**
   - Actualizar `pyproject.toml` (campo `name`)
   - Actualizar `package.json` (campo `name`)
   - Actualizar este README con el nombre del proyecto

3. **Configurar repositorio en GitHub**
   ```bash
   git add .
   git commit -m "Initial commit from ITE template"
   git remote add origin <url-nuevo-repositorio>
   git push -u origin main
   ```

4. **Habilitar branch protection** (ver sección CI/CD arriba)

5. **Empezar a desarrollar**
   - Crear rama: `git checkout -b feature/mi-feature`
   - Hacer cambios
   - Commit y push
   - Abrir PR en GitHub
   - Verificar que CI pasa antes de mergear

## Soporte

Para dudas o problemas con esta plantilla, consulta la documentación del proyecto ITE o contacta al equipo técnico.
