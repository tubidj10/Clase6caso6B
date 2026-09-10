# Ajuste real del contrato de citas

La primera llamada sobre correo_01 devolvió clasificación benign, pero evidence incluyó “Asunto: Reunión semanal” y comillas añadidas a otra cita. El validador exige subcadenas exactas; rechazó la respuesta. La salida original, la respuesta completa de API, el consumo y los hashes del prompt anterior se conservan en corrida_inicial_01/.

Se precisó el system prompt para prohibir prefijos, comillas añadidas y puntos suspensivos en las citas. No se cambió el validador para tolerar el error ni se editó la respuesta original. La nueva corrida_01 permite comprobar si la instrucción más específica resuelve la discrepancia. Las corridas 02 y 03 comprueban contextos diferentes.
