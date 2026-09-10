# Proceso documentado

Construcción docente en una sesión; no se atribuyen despliegues ni revisiones humanas inexistentes.

## Decisión 1: correo como dato no confiable
El mensaje se entrega como resultado de herramienta, con advertencia explícita de no seguir sus instrucciones. No se habilitan herramientas de navegación o envío. La salida solo es una clasificación propuesta con citas.

## Decisión 2: fallo real de citas y ajuste
La primera corrida del escenario 01 clasificó benign, pero añadió Asunto: y comillas a las citas. El validador las rechazó por no ser subcadenas exactas. Se conserva completa en proceso/corrida_inicial_01/, con respuesta original, fecha, tokens e instrucciones utilizadas.

Se precisó el prompt para exigir citas sin etiquetas ni comillas añadidas. No se editó la respuesta ni se relajó el validador. La nueva corrida_01 y sus archivos validacion.json y solicitudes_api.json permiten comprobar el resultado del ajuste. proceso/ajuste_citas.md explica el cambio.

## Decisión 3: distinguir ataque y contexto educativo
Las entradas 02 y 03 contienen la misma frase de manipulación en contextos distintos: pedido activo de contraseña y boletín que advierte no obedecer. No basta una lista de palabras para decidir. La validación técnica de citas no certifica la clasificación; debe revisarla una persona.

## Evidencia y limitaciones de la historia
Las pruebas guardadas muestran verificaciones realizadas sobre los archivos incluidos. El historial Git permite ubicar implementación y documentación. No se conserva una conversación completa con la IA ni una validación de campo empresarial. Las corridas preservan las instrucciones efectivamente enviadas al modelo; esas sí pueden auditarse literalmente.
