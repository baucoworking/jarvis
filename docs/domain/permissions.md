# JARVIS — Permisos

## Objetivo

El sistema de permisos determina qué acciones puede realizar JARVIS y bajo qué condiciones.

El hecho de que JARVIS tenga una herramienta disponible no significa automáticamente que pueda utilizarla sin restricciones.

---

## Categorías iniciales

### READ

Permite consultar información.

Ejemplos:

- Leer archivos
- Consultar información
- Consultar memoria

### EXECUTE

Permite ejecutar una acción.

Ejemplos:

- Abrir una aplicación
- Ejecutar una operación
- Iniciar un proceso

### MODIFY

Permite modificar información.

Ejemplos:

- Modificar archivos
- Modificar configuraciones
- Actualizar información

### EXTERNAL

Permite interactuar con sistemas o personas externas.

Ejemplos:

- Enviar un mensaje
- Enviar un correo
- Publicar contenido

### CRITICAL

Representa acciones con consecuencias especialmente importantes.

Estas acciones requieren una política específica y no deben ejecutarse automáticamente por defecto.

---

## Política de ejecución

Cada herramienta deberá determinar:

1. Qué permiso requiere.
2. Si puede ejecutarse automáticamente.
3. Si requiere confirmación del usuario.
4. Qué información debe registrarse.
5. Qué condiciones impiden su ejecución.

---

## Principio

Los permisos deben formar parte del diseño de una herramienta desde el momento en que se crea.

No deben agregarse únicamente después de que la herramienta ya pueda ejecutar acciones.
