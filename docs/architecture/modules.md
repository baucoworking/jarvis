# JARVIS — Módulos

## Voice

Responsable de recibir, procesar y producir audio.

Responsabilidades:

- entrada del micrófono
- transmisión de audio
- interacción mediante voz
- salida de audio
- gestión de interrupciones

Voice no debe contener lógica de negocio ni lógica específica de ningún proveedor de IA.

---

## Memory

Responsable de almacenar, recuperar y gestionar información relevante para JARVIS.

Responsabilidades:

- almacenamiento de memorias
- recuperación de memorias
- clasificación de memorias
- ciclo de vida de las memorias

Memory no debe depender directamente de una implementación específica de base de datos.

---

## AI

Responsable del razonamiento, la generación y la interacción con modelos de IA.

Responsabilidades:

- interacción con modelos
- preparación del contexto
- generación de respuestas
- decisiones sobre ejecución de herramientas (tool calling)
- adaptación específica para cada modelo

Los proveedores de IA deben poder reemplazarse.

---

## Tools

Responsable de permitir que JARVIS realice acciones.

Una herramienta representa una capacidad concreta disponible para JARVIS.

Ejemplos:

- `OpenSpotifyTool`
- `OpenApplicationTool`
- `ReadFileTool`
- `SearchWebTool`

Las herramientas deben exponer una interfaz consistente al resto del sistema.

---

## Scheduler

Responsable de las operaciones basadas en tiempo y de las operaciones programadas.

Ejemplos:

- recordatorios
- tareas programadas
- operaciones recurrentes
- acciones retrasadas

---

## Personality

Responsable del comportamiento comunicativo y de las características de personalidad de JARVIS.

Ejemplos:

- estilo de comunicación
- tono
- humor
- comportamiento conversacional
- preferencias de respuesta

Personality debe influir en la forma en que JARVIS se comunica sin contener lógica de negocio no relacionada.
