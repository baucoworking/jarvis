# JARVIS — Herramientas

## Objetivo

Las herramientas permiten que JARVIS realice acciones sobre su entorno.

Una herramienta representa una capacidad concreta que puede ser utilizada por JARVIS.

---

## Estructura conceptual

Cada herramienta debe tener:

```text
Tool
├── name
├── description
├── parameters
├── permissions
└── execute()
```

### name

Identificador de la herramienta.

### description

Descripción de lo que hace la herramienta.

### parameters

Datos necesarios para ejecutar la herramienta.

### permissions

Permisos necesarios para utilizarla.

### execute()

Operación que realiza la acción.

---

## Ejemplo

```text
OpenSpotifyTool

name:
open_spotify

description:
Abre Spotify en el dispositivo.

parameters:
ninguno

permissions:
EXECUTE

execute():
abre Spotify
```

---

## ToolRegistry

JARVIS tendrá un registro de herramientas disponibles.

Conceptualmente:

```text
ToolRegistry
├── OpenSpotifyTool
├── OpenApplicationTool
├── ReadFileTool
└── ...
```

El registro permitirá que JARVIS conozca qué herramientas existen y cuáles están disponibles.

---

## Principios

- Una herramienta debe tener una responsabilidad concreta.
- Las herramientas deben declarar sus parámetros.
- Las herramientas deben tener permisos definidos.
- Las herramientas no deben contener lógica central de JARVIS.
- Agregar una herramienta nueva no debería requerir modificar el núcleo de JARVIS.
