# Clasificador de correos sospechosos

## Qué construí
Clasifica mensajes de demostración según indicios y contexto. No abre enlaces, no responde y no bloquea cuentas.

La arquitectura es solicitud → LLM → herramienta de lectura y cálculo → observación → LLM → JSON validado → revisión humana. La llamada a la API es real; la herramienta se ejecuta localmente. No es un evaluador académico.

## Cómo se lo pedí
Especificación de construcción: “Clasifica mensajes de demostración según indicios y contexto. No abre enlaces, no responde y no bloquea cuentas. Usá una herramienta real de lectura de archivos, conservá las observaciones, devolvé JSON y exigí aprobación humana. No inventes datos ni ejecutes acciones externas”. El contrato operativo completo está en prompts/system_prompt.md y prompts/user_prompt.md. Esta especificación no se presenta como una transcripción de toda la conversación de desarrollo.

## Cómo usarlo
Requiere Python 3.10 o superior y OPENAI_API_KEY configurada en el entorno. No se incluye ninguna clave. No hay dependencias externas que instalar.

Desde la raíz del repositorio:

```sh
python3 src/main.py entradas/solicitud_01.json corridas/nueva_corrida_01
```

Repetir con solicitud_02 y solicitud_03 usando carpetas nuevas. El programa rechaza sobrescribir una corrida. Las carpetas corridas/corrida_01 a corrida_03 ya contienen ejecuciones reales: **para evaluar la entrega no es necesario ejecutar nuevamente ni proporcionar una clave**.

Pruebas de herramientas, sin API ni costo:

```sh
python3 tests/test_tools.py
```

## Qué funciona
Tres escenarios con entradas, herramienta invocada, observación, respuestas originales de la API, JSON final, fecha, modelo, tokens y validación. El programa distingue validated, needs_review y failed: si falla una comprobación, conserva la evidencia y termina con código 2; no presenta el resultado como aprobado.

El modelo es gpt-5-mini-2025-08-07, con razonamiento minimal y salida estructurada. La ejecución llama únicamente a la API de OpenAI y lee datos locales. No navega los enlaces que puedan aparecer en los archivos.

## Qué falta o qué falló
No es un antivirus ni demuestra la identidad del remitente. Las clasificaciones pueden equivocarse; las citas verifican procedencia del texto, no la verdad del mensaje. Los dominios example.invalid son ejemplos sin servicios reales. No se acredita eficacia sobre correo de producción.

La revisión humana nunca es un campo decorativo: la persona responsable debe comprobar los datos y firmar cualquier acción fuera de este programa. El software no demuestra que una persona haya revisado realmente las corridas adjuntas.

## Estructura y evidencia
- prompts/: contrato escrito de sistema y solicitud.
- config/: herramienta y esquema de salida.
- src/: implementación.
- datos/: archivos de entrada sintéticos y reproducibles.
- entradas/: solicitudes utilizadas.
- corridas/: las tres ejecuciones conservadas; metadata.json identifica fuente y consumo.
- tests/ y proceso/: comprobaciones y decisiones reconstruibles.
- DECISIONES.md: historia y límites de esta construcción.
- gobierno_riesgos.md: permisos, fallas y revisión.

## Autoría y procedencia
Material docente sintético creado para una prueba de corrección, no entrega de un alumno ni sistema de una empresa real. Las ejecuciones se realizaron durante su preparación el 9 de septiembre de 2026. Los commits corresponden a esta construcción; no simulan semanas de trabajo ni participación de personas ficticias.
