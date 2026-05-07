# Estado de proyectos de Layton

Esta repo publica funciona como fuente de datos estatica para el portafolio personal de Layton. Su objetivo es exponer un radar publico de proyectos sin depender de tokens, credenciales, APIs privadas ni acceso directo a repositorios privados.

## Como lo consume el portafolio

La app del portafolio puede leer los datos desde GitHub Raw usando el indice principal:

```text
projects.json
```

Cada item del indice apunta a una ficha individual mediante `dataUrl`:

```text
projects/{project-id}.json
```

Flujo recomendado:

1. Cargar `projects.json` para listar tarjetas, filtros y resumen general.
2. Usar `dataUrl` para consultar `projects/{project-id}.json` cuando se abra el detalle de un proyecto.
3. Tratar esta repo como fuente publica de solo lectura desde el cliente.

## Como actualizar manualmente un proyecto

1. Editar el proyecto individual en `projects/{project-id}.json`.
2. Actualizar el item correspondiente en `projects.json` con los mismos valores publicos.
3. Cambiar `updatedAt` usando fecha ISO.
4. Validar que el JSON sea valido antes de publicar.
5. Hacer commit y push solo despues de revisar que no haya informacion sensible.

## Campos publicos

Cada proyecto expone estos campos:

- `id`
- `name`
- `type`
- `status`
- `progress`
- `repositoryVisibility`
- `repositoryUrl`
- `publicDemoUrl`
- `dataUrl`
- `techStack`
- `summary`
- `currentBlock`
- `nextStep`
- `lastCommit`
- `updatedAt`

Los repos privados deben usar `repositoryVisibility: "private"` y `repositoryUrl: null`.

## Que no debe ponerse aqui

No publicar:

- Tokens, API keys, credenciales o secretos.
- URLs privadas de despliegue, bases de datos, paneles internos o ambientes no publicos.
- Nombres de clientes, contratos, documentos internos o informacion confidencial.
- Commits inventados o datos que parezcan verificables si no fueron sincronizados.
- Variables `.env`, backups, dumps de base de datos o archivos de configuracion privada.

## Plan futuro

Mas adelante se puede automatizar la sincronizacion con GitHub Actions para:

- Leer metadatos publicos de repos permitidos.
- Actualizar fechas y ultimo commit solo cuando la informacion sea publica y segura.
- Validar estructura JSON en cada pull request.
- Publicar reportes de consistencia entre `projects.json` y `projects/`.

Por ahora la actualizacion es manual para mantener control total sobre lo que se expone publicamente.
