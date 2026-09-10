# Análisis económico medido

## Modelo y tarifa
Se utilizó gpt-5-mini-2025-08-07, efectivamente devuelto por la API. Tarifa consultada el 9 de septiembre de 2026: USD 0,25 por millón de tokens de entrada sin caché, USD 0,025 por millón en caché y USD 2 por millón de tokens de salida, incluidos los de razonamiento. Fuente: https://developers.openai.com/api/docs/models/gpt-5-mini

La elección es acotada: la tarea está delimitada por herramienta y esquema; no requiere investigación abierta ni un modelo de mayor capacidad. Las corridas permiten comprobar el desempeño en los tres escenarios. No se realizó una comparación experimental con modelos más pequeños: no se afirma haber demostrado un óptimo global de costo.

## Mediciones
| Corrida | Tokens entrada | Tokens salida | USD por corrida |
|---|---:|---:|---:|
| corrida_01 | 1392 | 130 | 0.00060800 |
| corrida_02 | 1423 | 166 | 0.00068775 |
| corrida_03 | 1447 | 161 | 0.00068375 |

Promedio medido de las tres corridas: **USD 0.00065983**. Cada corrida incluye las dos llamadas, la invocación de herramienta y la respuesta final. Uso por llamada y posibles tokens en caché: respuesta_api_01.json y respuesta_api_02.json. El precio es un cálculo con tarifa publicada; no una factura del proveedor.

Fórmula: (entrada total − entrada en caché) × 0,25 / 1.000.000 + entrada en caché × 0,025 / 1.000.000 + salida × 2 / 1.000.000. No sumar razonamiento por segunda vez: forma parte de salida.

## Proyección y supuestos
Supuesto docente: 100 corridas por semana, durante 52 semanas. Costo API semanal: USD 0.065983; anual: USD 3.431133. Es una proyección sobre estos ejemplos pequeños, no sobre repositorios o volúmenes mayores. Reintentos y cambios de modelo incrementarían el costo.

Costo humano supuesto: 2 minutos de revisión por corrida a USD 15/hora = USD 0,50 por corrida, USD 50 por semana y USD 2.600 por año. Son supuestos didácticos, no tiempos medidos ni tarifas de mercado. Equipo, almacenamiento y electricidad no se midieron. El costo API no equivale al costo total del proceso.
