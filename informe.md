# Parcial 3 · Ingeniería de Software I

**Universidad de La Guajira · Facultad de Ingenierías · Ingeniería de Sistemas**
**Grupo B1 · 2026-2 · Docente: Ing. Robert Damián Quintero Laverde**

**Estudiante:** María José Cujia Gámez
**Código estudiantil:** 0182410054 (dígitos usados: 410054)

---

## Mis parámetros

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 4 | 1 | 0 | 0 | 5 | 4 | 50 | 3 | 10 | 15 % | 45 % | 15 % | $2.000 | 2 |

## Reglas de paridad aplicadas

| Dígito | Valor | Regla que me toca | Qué se hace |
|---|---|---|---|
| D · tramo 1 | 0 (par) | Incluye el límite | peso ≤ 3 |
| E · fin de semana | 5 (impar) | Recargo después de los descuentos | Se suma $2.000 al final |
| B · cliente y cupón | 1 (impar) | Se aplican ambos | Primero cliente, luego cupón |
| F · cupón inexistente | 4 (par) | Se ignora | No lanza error |

**Solicitud de cambio:** (A + F) mod 3 = (4 + 4) mod 3 = 2 → **Hora pico** (parámetro `hora` de 0 a 23; entre 17 y 19 inclusive, recargo del 8 % después del recargo por zona).

---

## Parte 1 · Requisitos y criterios de aceptación

### 1.1 Especificación del cálculo del costo

| ID | Regla |
|----|-------|
| R1 | 0 < peso ≤ 50 kg. Si no, se lanza el error "peso inválido". |
| R2 | Si la zona no es urbana/rural/nacional, o el día no está entre 1 y 7, se lanza un error. |
| R3 | Tarifa base: peso ≤ 3 → $6.000; 3 < peso ≤ 10 → $9.000; peso > 10 → $9.000 + $800 por cada kg sobre 10 (proporcional). |
| R4 | Recargo por zona: rural +15 %, nacional +45 %, urbana sin recargo. |
| R5 | Sábado (6) y domingo (7): +$2.000, **después** de los descuentos. |
| R6 | Descuento de cliente: frecuente 5 %, VIP 15 %. Cupón ENVIO10: 10 %. Se aplican ambos: primero el del cliente y luego el cupón. |
| R7 | Un cupón que no existe se **ignora** (no es error). |
| R8 | Costo mínimo $5.000. Se redondea al múltiplo de $100 más cercano; los $50 suben. |

**Ejemplo calculado a mano** (12 kg, rural, vip, día 6, ENVIO10):

1. Tarifa: 9.000 + 2 × 800 = 10.600
2. Rural +15 %: 10.600 × 1,15 = 12.190
3. VIP 15 %: 12.190 × 0,85 = 10.361,50
4. Cupón 10 %: 10.361,50 × 0,90 = 9.325,35
5. Sábado, después de descuentos: 9.325,35 + 2.000 = 11.325,35
6. Redondeo → **$11.300**

### 1.2 Historias de usuario 

#### HU-01 · Rechazar envíos con datos inválidos (R1, R2)
*Como operadora de la oficina de EnvíaYa en Riohacha, quiero que el sistema rechace envíos con datos inválidos, para no cobrar ni despachar paquetes que la empresa no puede transportar.*

| CA | Dado | Cuando | Entonces |
|----|------|--------|----------|
| CA-1.1 | un cliente llega a la oficina de Riohacha con una caja que marca 0 kg en la báscula | calculo el costo | se lanza el error "peso inválido" |
| CA-1.2 | un paquete de 50,1 kg con destino a Santa Marta | calculo el costo | se lanza el error "peso inválido" (supera PMAX = 50) |
| CA-1.3 | un envío de 50 kg dentro de Barranquilla (urbana), cliente normal, miércoles (día 3) | calculo el costo | el costo es **$41.000** (9.000 + 40 × 800) |
| CA-1.4 | un envío a San Andrés, zona "insular", que no existe en esta versión | calculo el costo | se lanza un error de zona inválida |
| CA-1.5 | un envío registrado con día 8 (o día 0) | calculo el costo | se lanza un error de día inválido |

#### HU-02 · Cobrar según peso y destino (R3, R4)
*Como comerciante de Cartagena que despacha mercancía, quiero que el costo dependa del peso y del destino, para pagar un precio justo.*

| CA | Dado | Cuando | Entonces |
|----|------|--------|----------|
| CA-2.1 | una caja de 3 kg dentro de Cartagena (urbana), cliente normal, día 2 | calculo el costo | **$6.000** (el límite del tramo 1 está incluido) |
| CA-2.2 | una caja de 3,1 kg dentro de Cartagena, cliente normal, día 2 | calculo el costo | **$9.000** (tramo 2) |
| CA-2.3 | una caja de 12 kg dentro de Cartagena, cliente normal, día 2 | calculo el costo | **$10.600** (9.000 + 2 × 800) |
| CA-2.4 | 12 kg a una finca rural cerca de Palomino, cliente normal, día 2 | calculo el costo | 10.600 × 1,15 = 12.190 → **$12.200** |
| CA-2.5 | 12 kg de Riohacha a Bogotá (nacional), cliente normal, día 2 | calculo el costo | 10.600 × 1,45 = 15.370 → **$15.400** |

#### HU-03 · Aplicar fin de semana, descuentos, cupón, mínimo y redondeo (R5, R6, R7, R8)
*Como dueña de una tienda de artesanías wayuu en Uribia que es cliente VIP, quiero que mis descuentos y cupones se apliquen correctamente y que el recargo del fin de semana no los afecte, para pagar el valor acordado.*

| CA | Dado | Cuando | Entonces |
|----|------|--------|----------|
| CA-3.1 | 3 kg dentro de Santa Marta, cliente VIP, sábado (día 6), sin cupón | calculo el costo | 6.000 × 0,85 = 5.100; + 2.000 (después del descuento) = **$7.100** |
| CA-3.2 | 12 kg dentro de Riohacha, cliente VIP, día 2, cupón ENVIO10 | calculo el costo | 10.600 × 0,85 × 0,90 = 8.109 → **$8.100** (ambos descuentos) |
| CA-3.3 | 3 kg dentro de Manaure, cliente normal, día 2, cupón "PROMO5" (no existe) | calculo el costo | el cupón se ignora: **$6.000** |
| CA-3.4 | 3 kg dentro de Riohacha, cliente VIP, día 2, cupón ENVIO10 | calculo el costo | 6.000 × 0,85 × 0,90 = 4.590 < 5.000 → **$5.000** (mínimo) |
| CA-3.5 | 12 kg dentro de Barranquilla, cliente frecuente, día 2 | calculo el costo | 10.600 × 0,95 = 10.070 → **$10.100** (al más cercano, no truncado) |

### 1.3 Matriz de trazabilidad (requisito → historia → casos de prueba)

| Requisito | Historia | Criterios | Casos de prueba |
|-----------|----------|-----------|-----------------|
| R1 | HU-01 | CA-1.1, 1.2, 1.3 | CP-01, 07, 08, 09 |
| R2 | HU-01 | CA-1.4, 1.5 | CP-12, 13, 14 |
| R3 | HU-02 | CA-2.1, 2.2, 2.3 | CP-02, 03, 04, 05, 06 |
| R4 | HU-02 | CA-2.4, 2.5 | CP-10, 11, 31 |
| R5 | HU-03 | CA-3.1 | CP-16, 18, 20, 22, 24, 26, 30, 32 |
| R6 | HU-03 | CA-3.1, 3.2 | CP-15, 17, 19, 21, 23, 25 |
| R7 | HU-03 | CA-3.3 | CP-27 |
| R8 | HU-03 | CA-3.4, 3.5 | CP-28, 29 |

> La columna de casos de prueba se completa con la Parte 3 (matriz de 32 casos).

---

## Parte 2 · Plan de pruebas

### 2.1 Alcance
**Dentro del alcance:** la función `calc` de `envios.py` (cálculo del costo de envío de EnvíaYa) según las reglas R1 a R8 con mis parámetros, y su refactorización posterior.
**Fuera del alcance:** interfaz de usuario, base de datos, pasarela de pago y rendimiento con carga.

### 2.2 Niveles de prueba

| Nivel | Qué se prueba | Cómo se aplica a este caso |
|---|---|---|
| Unidad | `calc` aislada | Los 32 casos de caja negra y los caminos de caja blanca, automatizados con pytest. |
| Integración | `calc` + `CONFIG` + las reglas combinadas | Casos que mezclan zona + cliente + cupón + fin de semana (CP-15 a CP-26, CP-31, CP-32); verifican que la lectura de CONFIG y el orden de las reglas sean correctos. |
| Sistema | El cálculo completo, usado como lo haría EnvíaYa | Ejecutar `calc` desde la terminal con envíos reales de ejemplo (Riohacha, Santa Marta, Cartagena, Barranquilla). |
| Aceptación | ¿Cumple lo que pidió el negocio? | Verificar los criterios Dado/Cuando/Entonces de HU-01, HU-02 y HU-03 con el docente en la sustentación. |

### 2.3 Estrategia, ambiente y roles
- **Estrategia:** caja negra (particiones, valores límite, tabla de decisión) y caja blanca (caminos independientes). Resultados esperados calculados a mano con mi especificación, nunca copiados del código. Se ejecuta primero contra el código heredado (v1.0.0), luego se corrige y se hace regresión.
- **Ambiente:** Windows, Python 3.14, pytest, pytest-cov, VS Code, Git y GitHub.
- **Roles:** al ser un trabajo individual, asumo todos los roles: analista de requisitos, diseñadora de pruebas, ejecutora de pruebas y desarrolladora (correcciones y refactorización). El docente actúa como cliente en la aceptación.

### 2.4 Riesgos y mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Error de aritmética al calcular esperados a mano | Media | Alto | Revisar cada cálculo paso a paso y contrastarlo con calculadora. |
| Copiar defectos del código heredado en los esperados | Media | Alto | Calcular siempre con la especificación, sin ejecutar el código. |
| Errores de punto flotante en el redondeo | Media | Medio | Casos con $50 exactos (CP-29) y uso de `Decimal` al corregir. |
| Refactorizar rompe algo que funcionaba | Media | Alto | Suite de regresión completa tras cada cambio. |
| Falta de tiempo | Alta | Alto | Priorizar casos de mayor riesgo y hacer commits frecuentes. |

### 2.5 Criterios de entrada y de salida

**Entrada** (para empezar a ejecutar):
- Especificación R1 a R8 aprobada con mis parámetros.
- Casos de prueba diseñados y con esperado calculado.
- Código v1.0.0 con CONFIG lleno y etiquetado en Git.
- Ambiente con Python y pytest funcionando.

**Salida** (para dar las pruebas por terminadas):
- 100 % de los casos ejecutados.
- 100 % de los casos pasan tras las correcciones (regresión en verde).
- 0 defectos abiertos de severidad alta o crítica.
- Cobertura mínima: 90 % de sentencias y 85 % de ramas.

---


## Parte 3 · Diseño de casos de caja negra

### 3.1 Particiones de equivalencia

| Entrada | Partición | Tipo | Representante |
|---|---|---|---|
| peso | peso ≤ 0 | Inválida | −5 |
| peso | 0 < peso ≤ 3 | Válida (tramo 1) | 2 |
| peso | 3 < peso ≤ 10 | Válida (tramo 2) | 5 |
| peso | 10 < peso ≤ 50 | Válida (tramo 3) | 12 |
| peso | peso > 50 | Inválida | 60 |
| zona | urbana / rural / nacional | Válida (3 particiones) | urbana, rural, nacional |
| zona | cualquier otro valor | Inválida | "insular" |
| cliente | normal / frecuente / vip | Válida (3 particiones) | normal, frecuente, vip |
| día | 1 a 5 (entre semana) | Válida | 2 |
| día | 6 (sábado) y 7 (domingo) | Válida (fin de semana) | 6, 7 |
| día | < 1 o > 7 | Inválida | 0, 8 |
| cupón | sin cupón | Válida | None |
| cupón | ENVIO10 | Válida | "ENVIO10" |
| cupón | cupón inexistente | Válida (se ignora, F par) | "PROMO5" |

### 3.2 Valores límite del peso

Mi D = 0 es par, entonces el límite L1 **está incluido** (peso ≤ 3).

| Frontera | Valores | Resultado esperado |
|---|---|---|
| Cero | 0 y 0,1 | Error y $6.000 |
| L1 = 3 | 3 y 3,1 | $6.000 (incluido) y $9.000 |
| L2 = 10 | 10 y 10,1 | $9.000 y $9.080 → $9.100 |
| PMAX = 50 | 50 y 50,1 | $41.000 y Error |

### 3.3 Tabla de decisión: cliente × cupón × fin de semana

Reglas B impar (se aplican ambos: cliente primero y luego cupón) y E impar (el recargo va después de los descuentos). Base: 12 kg, urbana, tarifa $10.600.

| Regla | Cliente | Cupón ENVIO10 | Fin de semana | Cálculo | Resultado |
|---|---|---|---|---|---|
| T1 | normal | No | No | 10.600 | $10.600 |
| T2 | normal | No | Sí | 10.600 + 2.000 = 12.600 | $12.600 |
| T3 | normal | Sí | No | 10.600 × 0,90 = 9.540 | $9.500 |
| T4 | normal | Sí | Sí | 9.540 + 2.000 = 11.540 | $11.500 |
| T5 | frecuente | No | No | 10.600 × 0,95 = 10.070 | $10.100 |
| T6 | frecuente | No | Sí | 10.070 + 2.000 = 12.070 | $12.100 |
| T7 | frecuente | Sí | No | 10.070 × 0,90 = 9.063 | $9.100 |
| T8 | frecuente | Sí | Sí | 9.063 + 2.000 = 11.063 | $11.100 |
| T9 | vip | No | No | 10.600 × 0,85 = 9.010 | $9.000 |
| T10 | vip | No | Sí | 9.010 + 2.000 = 11.010 | $11.000 |
| T11 | vip | Sí | No | 9.010 × 0,90 = 8.109 | $8.100 |
| T12 | vip | Sí | Sí | 8.109 + 2.000 = 10.109 | $10.100 |

### 3.4 Matriz de casos de prueba (32 casos)

| ID | Req. | Entradas | Resultado esperado | Técnica |
|---|---|---|---|---|
| CP-01 | R1 | peso=0, urbana, normal, día 2, cupón — | Error | Valor límite |
| CP-02 | R3 | peso=0,1, urbana, normal, día 2, cupón — | $6.000 | Valor límite |
| CP-03 | R3 | peso=3, urbana, normal, día 2, cupón — | $6.000 | Valor límite (D par: incluido) |
| CP-04 | R3 | peso=3,1, urbana, normal, día 2, cupón — | $9.000 | Valor límite |
| CP-05 | R3 | peso=10, urbana, normal, día 2, cupón — | $9.000 | Valor límite (L2 incluido) |
| CP-06 | R3 | peso=10,1, urbana, normal, día 2, cupón — | $9.100 | Valor límite |
| CP-07 | R1 | peso=50, urbana, normal, día 3, cupón — | $41.000 | Valor límite (PMAX) |
| CP-08 | R1 | peso=50,1, urbana, normal, día 3, cupón — | Error | Valor límite |
| CP-09 | R1 | peso=-5, urbana, normal, día 2, cupón — | Error | Partición inválida |
| CP-10 | R4 | peso=12, rural, normal, día 2, cupón — | $12.200 | Partición (zona) |
| CP-11 | R4 | peso=12, nacional, normal, día 2, cupón — | $15.400 | Partición (zona) |
| CP-12 | R2 | peso=5, insular, normal, día 2, cupón — | Error | Partición inválida (zona) |
| CP-13 | R2 | peso=5, urbana, normal, día 0, cupón — | Error | Valor límite (día) |
| CP-14 | R2 | peso=5, urbana, normal, día 8, cupón — | Error | Valor límite (día) |
| CP-15 | R6 | peso=12, urbana, normal, día 2, cupón — | $10.600 | Tabla de decisión T1 |
| CP-16 | R5 | peso=12, urbana, normal, día 6, cupón — | $12.600 | Tabla de decisión T2 |
| CP-17 | R6 | peso=12, urbana, normal, día 2, cupón ENVIO10 | $9.500 | Tabla de decisión T3 |
| CP-18 | R5 | peso=12, urbana, normal, día 6, cupón ENVIO10 | $11.500 | Tabla de decisión T4 |
| CP-19 | R6 | peso=12, urbana, frecuente, día 2, cupón — | $10.100 | Tabla de decisión T5 |
| CP-20 | R5 | peso=12, urbana, frecuente, día 6, cupón — | $12.100 | Tabla de decisión T6 |
| CP-21 | R6 | peso=12, urbana, frecuente, día 2, cupón ENVIO10 | $9.100 | Tabla de decisión T7 |
| CP-22 | R5 | peso=12, urbana, frecuente, día 6, cupón ENVIO10 | $11.100 | Tabla de decisión T8 |
| CP-23 | R6 | peso=12, urbana, vip, día 2, cupón — | $9.000 | Tabla de decisión T9 |
| CP-24 | R5 | peso=12, urbana, vip, día 7, cupón — | $11.000 | Tabla de decisión T10 |
| CP-25 | R6 | peso=12, urbana, vip, día 2, cupón ENVIO10 | $8.100 | Tabla de decisión T11 |
| CP-26 | R5 | peso=12, urbana, vip, día 7, cupón ENVIO10 | $10.100 | Tabla de decisión T12 |
| CP-27 | R7 | peso=3, urbana, normal, día 2, cupón PROMO5 | $6.000 | Partición (cupón inexistente) |
| CP-28 | R8 | peso=3, urbana, vip, día 2, cupón ENVIO10 | $5.000 | Valor límite (mínimo) |
| CP-29 | R8 | peso=5, rural, normal, día 2, cupón — | $10.400 | Redondeo en $50 |
| CP-30 | R5 | peso=3, urbana, vip, día 6, cupón ENVIO10 | $6.600 | Adivinanza de errores |
| CP-31 | R4 | peso=20, nacional, vip, día 7, cupón ENVIO10 | $20.900 | Combinación completa |
| CP-32 | R5 | peso=3, rural, frecuente, día 6, cupón — | $8.600 | Combinación + redondeo |

### 3.5 Cálculo paso a paso de casos seleccionados

**CP-06** (peso 10,1, urbana, normal, día 2, sin cupón)
1. Peso > 10 → 9.000 + (10,1 − 10) × 800 = 9.080
2. Urbana: sin recargo. Normal: sin descuento. Día 2: sin recargo.
3. 9.080 > 5.000. Redondeo al múltiplo de 100 más cercano → **$9.100**

**CP-26** (12 kg, urbana, vip, día 7, ENVIO10)
1. Tarifa: 9.000 + 2 × 800 = 10.600
2. VIP 15 %: 10.600 × 0,85 = 9.010
3. Cupón 10 %: 9.010 × 0,90 = 8.109
4. Domingo, después de descuentos: 8.109 + 2.000 = 10.109
5. Redondeo → **$10.100**

**CP-29** (5 kg, rural, normal, día 2)
1. Peso 5 → tramo 2: $9.000
2. Rural +15 %: 9.000 × 1,15 = 10.350
3. Es exactamente $50 sobre la centena → sube → **$10.400**

**CP-30** (3 kg, urbana, vip, día 6, ENVIO10)
1. Peso 3 → tramo 1 (límite incluido): $6.000
2. VIP: 6.000 × 0,85 = 5.100
3. Cupón: 5.100 × 0,90 = 4.590
4. Sábado, después de descuentos: 4.590 + 2.000 = 6.590
5. 6.590 > 5.000 → redondeo → **$6.600**

**CP-31** (20 kg, nacional, vip, día 7, ENVIO10)
1. Tarifa: 9.000 + 10 × 800 = 17.000
2. Nacional +45 %: 17.000 × 1,45 = 24.650
3. VIP: 24.650 × 0,85 = 20.952,50
4. Cupón: 20.952,50 × 0,90 = 18.857,25
5. Domingo: 18.857,25 + 2.000 = 20.857,25
6. Redondeo → **$20.900**

**CP-32** (3 kg, rural, frecuente, día 6, sin cupón)
1. Tarifa: $6.000
2. Rural: 6.000 × 1,15 = 6.900
3. Frecuente: 6.900 × 0,95 = 6.555
4. Sábado: 6.555 + 2.000 = 8.555
5. Redondeo → **$8.600**

### 3.6 Matriz de trazabilidad completa

| Requisito | Historia | Criterios | Casos de prueba |
|---|---|---|---|
| R1 | HU-01 | CA-1.1, 1.2, 1.3 | CP-01, 07, 08, 09 |
| R2 | HU-01 | CA-1.4, 1.5 | CP-12, 13, 14 |
| R3 | HU-02 | CA-2.1, 2.2, 2.3 | CP-02, 03, 04, 05, 06 |
| R4 | HU-02 | CA-2.4, 2.5 | CP-10, 11, 31 |
| R5 | HU-03 | CA-3.1 | CP-16, 18, 20, 22, 24, 26, 30, 32 |
| R6 | HU-03 | CA-3.1, 3.2 | CP-15, 17, 19, 21, 23, 25 |
| R7 | HU-03 | CA-3.3 | CP-27 |
| R8 | HU-03 | CA-3.4, 3.5 | CP-28, 29 |

---

## Parte 4 · Caja blanca
(pendiente)

## Parte 5 · Automatización, ejecución y defectos

> **Análisis preliminar** (se formaliza luego con ID, pasos, esperado/obtenido, severidad y prioridad).

| Línea del código | ¿Defecto para mí? | Por qué |
|------------------|:-----------------:|---------|
| `p > 50` | No | Mi PMAX es 50, coincide. |
| `p <= L1` | No | Con D par el límite se incluye. |
| `d > 6` | **Sí** | Solo toma el domingo; el sábado (6) también debe recargar (`d >= 6`). |
| Recargo de fin de semana antes de descuentos | **Sí** | Con E impar va después de los descuentos. |
| Descuento de cliente y luego cupón | No | Coincide con B impar. |
| Cupón desconocido se ignora | No | Coincide con F par. |
| `int(t / 100) * 100` | **Sí** | Trunca; R8 pide redondear al más cercano (los $50 suben). |
| No valida zona ni día | **Sí** | Falta R2. |
| Mensaje `"peso invalido"` | Posible (menor) | R1 pide "peso inválido" (con tilde). |

## Parte 6 · Mantenimiento y refactorización
(pendiente)

## Parte 7 · Gestión de configuración
(pendiente)

## Parte 8 · Solicitud de cambio y análisis de impacto
(pendiente)
