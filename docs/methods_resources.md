# Métodos y Recursos

## 1. Enfoque metodológico

El desarrollo del prototipo se ha abordado mediante una metodología iterativa e incremental, dividiendo el trabajo en fases claramente diferenciadas: diseño conceptual (CA1), definición de requisitos funcionales y diseño de interacción (CA2), e implementación técnica (CA3).

Cada fase ha aportado decisiones clave para la siguiente, lo que permitió construir una solución con alineación entre la experiencia de usuario, los datos geoespaciales, y la arquitectura técnica. El enfoque se apoya en principios de desarrollo ágil y arquitectura desacoplada para permitir evolución, escalabilidad y mantenibilidad del sistema.

## 2. Stack tecnológico y herramientas

Para el desarrollo del prototipo funcional, se definió una pila tecnológica moderna dividida en tres capas:

### Backend

- **Lenguaje:** Python 3.13
- **Framework:** FastAPI
- **Servidor:** Uvicorn (ASGI)
- **Base de datos:** PostgreSQL con extensión PostGIS
- **Conexión:** psycopg2
- **Gestión de entorno:** python-dotenv
- **Contenerización:** Docker (python:3.13-slim)

### Frontend

- **Framework:** React.js
- **Visualización:** Leaflet.js
- **Bundler:** Vite
- **API:** Fetch con servicios REST
- **Despliegue local/producción:** Docker + Serve

### Infraestructura y CI/CD

- **Orquestación:** Docker Compose
- **Configuración:** .env.example
- **Integración futura:** GitHub Actions

## 3. Organización del proyecto

El proyecto se estructura con separación por responsabilidades:

```
are-u-query-ous/
├── backend/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── tests/
├── frontend/
│   ├── components/
│   ├── hooks/
│   ├── contexts/
│   └── types.js
├── data/
├── deployment/
├── docs/
└── .github/
```

## 4. Recursos adicionales

- Manual de instalación (`installation_manual.md`)
- Archivo `.env.example`
- Reportes por fase (`implementation_report.md`, `project_schedule_update.md`)
