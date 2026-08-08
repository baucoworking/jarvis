# JARVIS — Eventos

## Objetivo

Los eventos representan acontecimientos que ya ocurrieron dentro de JARVIS o en su entorno.

Un evento describe algo que sucedió.

No representa una orden para realizar una acción.

---

## Eventos iniciales

### UserStartedSpeaking

El usuario comenzó a hablar.

### UserStoppedSpeaking

El usuario dejó de hablar.

### MessageReceived

JARVIS recibió un mensaje.

### ResponseGenerated

JARVIS generó una respuesta.

### MemoryCreated

Se creó una nueva memoria.

### ToolExecuted

Una herramienta fue ejecutada.

### ReminderTriggered

Se activó un recordatorio.

### DeviceChanged

Cambió el estado o dispositivo relevante para JARVIS.

---

## Eventos vs acciones

Un evento:

```text
ToolExecuted
```

significa:

> Una herramienta ya fue ejecutada.

Una acción:

```text
ExecuteTool
```

significa:

> Se solicita ejecutar una herramienta.

Estas dos ideas deben mantenerse separadas.

---

## Principios

- Los eventos representan acontecimientos.
- Los eventos deben ser independientes de una implementación concreta.
- Los componentes pueden reaccionar a eventos relevantes.
- Un evento no debe asumir qué componente reaccionará ante él.
