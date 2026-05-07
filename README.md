# Estado de proyectos de Layton

`layton-projects-status` es la fuente publica de datos para Layton Projects Mission Control. La repo expone archivos JSON estaticos con informacion segura sobre el estado, avance, tecnologia y proximos pasos de los proyectos del ecosistema Layton.

No contiene credenciales, URLs privadas, configuraciones internas ni datos sensibles. Su objetivo es alimentar una vista publica y controlada, no sincronizar automaticamente todo lo que exista en repositorios privados.

## Consumo desde el dashboard

La app `layton-projects-dashboard`, visualmente llamada Layton Projects Mission Control, consume el indice principal desde GitHub Raw:

```text
https://raw.githubusercontent.com/juanmalay/layton-projects-status/main/projects.json
```

Cada item del indice incluye un `dataUrl` relativo hacia su ficha individual:

```text
projects/{id}.json
```

El flujo de consumo actual es:

1. Cargar `projects.json` para pintar tarjetas, filtros, resumenes, KPIs y paneles generales.
2. Leer `dataUrl` cuando el usuario abre el detalle premium de un proyecto.
3. Consultar `projects/{id}.json` para mostrar milestones, bloqueo actual, proximo paso y metadatos ampliados.

## Editar `projects.json`

`projects.json` es el indice publico. Cada item debe conservar estos campos principales:

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

Reglas para editarlo:

1. No cambiar un `id` salvo que exista un error evidente y tambien se renombre su archivo individual.
2. Mantener `dataUrl` como `projects/{id}.json`.
3. Para repos privados, usar `repositoryVisibility: "private"` y `repositoryUrl: null`.
4. Para repos publicos, usar solo URLs publicas conocidas.
5. Actualizar `updatedAt` en formato ISO.
6. No inventar commits reales; si no hay sincronizacion segura, usar `Pending synchronization`.

## Editar archivos individuales

Cada archivo en `/projects` representa el detalle publico de un proyecto. La ruta debe coincidir con el `dataUrl` del indice:

```text
projects/plataforma-hseq.json
projects/turisfera.json
projects/layton-projects-dashboard.json
```

La estructura esperada por archivo es:

```json
{
  "id": "",
  "name": "",
  "type": "",
  "status": "",
  "progress": 0,
  "repositoryVisibility": "private",
  "repositoryUrl": null,
  "publicDemoUrl": null,
  "techStack": [],
  "summary": "",
  "currentBlock": "",
  "nextStep": "",
  "lastCommit": {
    "message": "Pending synchronization",
    "date": "",
    "branch": "main"
  },
  "milestones": [
    {
      "title": "",
      "status": "",
      "date": ""
    }
  ],
  "updatedAt": ""
}
```

Los archivos individuales pueden tener mas detalle que `projects.json`, especialmente en `milestones`, siempre que la informacion sea publica y segura.

## Informacion publica permitida

Se puede publicar:

- Nombre publico del proyecto.
- Tipo de producto o categoria.
- Estado general y porcentaje de avance aproximado.
- Stack tecnologico general.
- Resumen funcional sin clientes, secretos ni infraestructura privada.
- Bloqueo actual descrito en terminos de producto o tecnologia.
- Proximo paso general.
- URL de repositorios publicos.
- URL de demos publicas, si existen y son seguras.
- Milestones sin fechas inventadas ni datos internos.

## Informacion que nunca debe publicarse

No publicar:

- Tokens, API keys, secretos, contrasenas o credenciales.
- Variables `.env`.
- URLs privadas de despliegue, bases de datos, paneles internos o ambientes no publicos.
- Nombres de clientes, contratos, documentos internos o informacion confidencial.
- Dumps, backups, rutas locales sensibles o capturas con datos privados.
- Commits inventados o fechas especificas no verificadas.
- Infraestructura privada de repositorios marcados como privados.

## Flujo manual actual

El mantenimiento por ahora es manual:

1. Editar el archivo individual en `projects/{id}.json`.
2. Actualizar el item correspondiente en `projects.json`.
3. Usar `updatedAt` con fecha ISO.
4. Validar que todos los JSON sean validos.
5. Validar que cada `dataUrl` exista.
6. Revisar que no haya informacion sensible.
7. Hacer commit y push solo despues de revisar el diff.

## Futuro flujo con GitHub Actions

Mas adelante se puede automatizar parte del proceso con GitHub Actions:

- Validar JSON en cada pull request.
- Verificar que cada `dataUrl` apunte a un archivo existente.
- Comparar IDs entre `projects.json` y `/projects`.
- Bloquear patrones de secretos conocidos.
- Sincronizar ultimo commit solo para repos publicos permitidos.
- Generar un reporte de consistencia antes de publicar cambios.

La automatizacion debe seguir priorizando control editorial y seguridad publica sobre sincronizacion total.
