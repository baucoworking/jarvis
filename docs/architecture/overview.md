# JARVIS — Descripción General de la Arquitectura

## 1. Propósito

Este documento describe la arquitectura de alto nivel de JARVIS, sus principales capas y las relaciones entre ellas.

El objetivo es mantener un sistema modular en el que las tecnologías individuales puedan reemplazarse sin requerir cambios en toda la aplicación.

---

## 2. Principios arquitectónicos

### Separación de responsabilidades

Cada componente debe tener una responsabilidad claramente definida.

Un componente no debe asumir responsabilidades que pertenecen a otro componente.

### Inversión de dependencias

La lógica de negocio principal y los conceptos del dominio no deben depender directamente de la infraestructura ni de proveedores externos.

El dominio no debe depender directamente de:

- Gemini
- PostgreSQL
- APIs de Windows
- librerías de audio específicas
- servicios externos específicos

### Independencia de proveedores

JARVIS debe interactuar con tecnologías externas mediante abstracciones siempre que resulte práctico.

Ejemplo:

```text
JARVIS
   ↓
Interfaz de IA
   ↓
Implementación de Gemini
```

El proveedor de IA debe poder reemplazarse sin tener que rediseñar todo el sistema.

### Testabilidad

El comportamiento importante de la aplicación debe poder probarse sin requerir servicios externos reales siempre que sea posible.

### Configuración ≠ código

Los secretos, claves de API, URLs, nombres de modelos, configuraciones específicas del entorno y valores similares no deben estar escritos directamente en la lógica de la aplicación.

---

## 3. Capas de alto nivel

JARVIS está dividido en las siguientes capas conceptuales:

```text
Interfaces
    ↓
Aplicación
    ↓
Dominio
    ↓
Infraestructura
```

### Interfaces

Responsables de la interacción con JARVIS.

Ejemplos:

- Voz
- Interfaz de escritorio
- CLI
- API

### Aplicación

Coordina los casos de uso y los flujos de trabajo de la aplicación.

Ejemplos:

- conversación
- recuperación de memoria
- ejecución de tareas
- ejecución de herramientas

### Dominio

Contiene los conceptos y las reglas que definen a JARVIS.

Ejemplos:

- Message
- Conversation
- Memory
- Tool
- Event
- Permission
- Task

### Infraestructura

Proporciona las implementaciones concretas de las capacidades externas.

Ejemplos:

- proveedores de IA
- bases de datos
- sistemas de audio
- integraciones con el sistema operativo
- APIs externas

---

## 4. Estructura conceptual

```text
                         JARVIS
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Interfaces                    Aplicación
              │                           │
              └─────────────┬─────────────┘
                            │
                          Dominio
                            │
              ┌─────────────┼─────────────┐
              │             │             │
             IA           Audio        Base de datos
              │             │             │
            Infraestructura / Integraciones
```

Este diagrama es conceptual. No representa la implementación final.

---

## 5. Subsistemas principales

Se espera que JARVIS contenga los siguientes subsistemas principales:

- Voice
- Memory
- AI
- Tools
- Scheduler
- Personality

Sus responsabilidades detalladas están documentadas por separado en `architecture/modules.md`.

---

## 6. Regla sobre dependencias externas

Los proveedores externos deben permanecer reemplazables siempre que resulte práctico.

Por ejemplo:

```text
AIProvider
├── GeminiProvider
├── OpenAIProvider
└── LocalProvider
```

El resto de JARVIS debería depender de la abstracción `AIProvider` en lugar de depender directamente de un proveedor específico.

---

## 7. Evolución de la arquitectura

Esta arquitectura está diseñada intencionalmente para evolucionar.

Se pueden introducir nuevas tecnologías cuando resuelvan un problema concreto, pero no deben adoptarse simplemente porque sean populares o porque se las considere "profesionales".

Los cambios arquitectónicos que afecten significativamente al sistema deben documentarse como Registros de Decisiones Arquitectónicas (ADR, por sus siglas en inglés).
