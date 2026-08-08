# JARVIS — Dependencias

## Filosofía

Las dependencias se incorporan cuando resuelven un problema concreto.

Una biblioteca no debe incorporarse únicamente porque sea popular, moderna o utilizada habitualmente en proyectos profesionales.

Antes de agregar una dependencia se debe determinar:

1. Qué problema resuelve.
2. Si Python puede resolverlo mediante la biblioteca estándar.
3. Si una dependencia externa aporta una ventaja significativa.
4. Si introduce un nivel razonable de complejidad.
5. Si genera acoplamiento innecesario.

---

## Gestión del proyecto

### uv

Se utilizará `uv` para gestionar el proyecto Python, sus dependencias y el entorno virtual.

---

## Dependencias actuales

En este momento no se requieren dependencias de aplicación.

---

## Dependencias candidatas

Estas herramientas pueden incorporarse cuando aparezca una necesidad concreta:

### Pydantic

Para validación y estructuración de datos.

### pytest

Para pruebas automatizadas.

### Ruff

Para análisis estático, linting y formato del código.

### FastAPI

Para exponer JARVIS mediante una API HTTP cuando sea necesario.

### SQLAlchemy

Para interactuar con una base de datos mediante Python.

### PostgreSQL

Como posible sistema de almacenamiento persistente.

### SDK de IA

Se incorporará el SDK oficial del proveedor de IA seleccionado cuando se implemente la interacción con modelos.

### Bibliotecas de audio

Se seleccionarán cuando se diseñe e implemente el sistema de voz.

---

## Regla

Ninguna dependencia candidata debe considerarse obligatoria hasta que exista una necesidad concreta que justifique su incorporación.
