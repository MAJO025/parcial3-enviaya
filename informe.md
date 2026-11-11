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

**Ejemplo calculado a mano** (peso 12, rural, vip, día 6, ENVIO10):

1. Tarifa: 9.000 + 2 × 800 = 10.600
2. Rural +15 %: 10.600 × 1,15 = 12.190
3. VIP 15 %: 12.190 × 0,85 = 10.361,50
4. Cupón 10 %: 10.361,50 × 0,90 = 9.325,35
5. Sábado, después de descuentos: 9.325,35 + 2.000 = 11.325,35
6. Redondeo → **$11.300**

### 1.2 Historias de usuario

#### HU-01 · Validar los datos del envío (R1, R2)
*Como operador de EnvíaYa, quiero que el sistema rechace envíos con datos inválidos, para no cobrar ni despachar paquetes que la empresa no puede transportar.*

| CA | Dado | Cuando | Entonces |
|----|------|--------|----------|
| CA-1.1 | un paquete de 0 kg | calculo el costo | se lanza el error "peso inválido" |
| CA-1.2 | un paquete de 50,1 kg | calculo el costo | se lanza el error "peso inválido" |
| CA-1.3 | 50 kg, urbana, normal, día 3 | calculo el costo | **$41.000** (9.000 + 40 × 800) |
| CA-1.4 | zona "aérea" (no válida) | calculo el costo | se lanza un error |
| CA-1.5 | día 8 (o día 0) | calculo el costo | se lanza un error |

#### HU-02 · Tarifa base y recargo por zona (R3, R4)
*Como cliente, quiero que el costo dependa del peso y del destino, para pagar un precio justo según lo que envío.*

| CA | Dado | Cuando | Entonces |
|----|------|--------|----------|
| CA-2.1 | 3 kg, urbana, normal, día 2 | calculo el costo | **$6.000** (el límite está incluido) |
| CA-2.2 | 3,1 kg, urbana, normal, día 2 | calculo el costo | **$9.000** (tramo 2) |
| CA-2.3 | 12 kg, urbana, normal, día 2 | calculo el costo | **$10.600** (9.000 + 2 × 800) |
| CA-2.4 | 12 kg, rural, normal, día 2 | calculo el costo | 10.600 × 1,15 = 12.190 → **$12.200** |
| CA-2.5 | 12 kg, nacional, normal, día 2 | calculo el costo | 10.600 × 1,45 = 15.370 → **$15.400** |

#### HU-03 · Fin de semana, descuentos, cupón, mínimo y redondeo (R5, R6, R7, R8)
*Como cliente frecuente o VIP, quiero que mis descuentos y cupones se apliquen correctamente y que el recargo de fin de semana no los afecte, para pagar el valor acordado.*

| CA | Dado | Cuando | Entonces |
|----|------|--------|----------|
| CA-3.1 | 3 kg, urbana, VIP, día 6, sin cupón | calculo el costo | 6.000 × 0,85 = 5.100; + 2.000 = **$7.100** |
| CA-3.2 | 12 kg, urbana, VIP, día 2, ENVIO10 | calculo el costo | 10.600 × 0,85 × 0,90 = 8.109 → **$8.100** |
| CA-3.3 | 3 kg, urbana, normal, día 2, cupón "PROMO5" | calculo el costo | el cupón se ignora: **$6.000** |
| CA-3.4 | 3 kg, urbana, VIP, día 2, ENVIO10 | calculo el costo | 6.000 × 0,85 × 0,90 = 4.590 < 5.000 → **$5.000** |
| CA-3.5 | 12 kg, urbana, frecuente, día 2 | calculo el costo | 10.600 × 0,95 = 10.070 → **$10.100** |

### 1.3 Matriz de trazabilidad

| Requisito | Historia | Criterios | Casos de prueba |
|-----------|----------|-----------|-----------------|
| R1 | HU-01 | CA-1.1, 1.2, 1.3 | (se completa en la Parte 3) |
| R2 | HU-01 | CA-1.4, 1.5 | (pendiente) |
| R3 | HU-02 | CA-2.1, 2.2, 2.3 | (pendiente) |
| R4 | HU-02 | CA-2.4, 2.5 | (pendiente) |
| R5 | HU-03 | CA-3.1 | (pendiente) |
| R6 | HU-03 | CA-3.1, 3.2 | (pendiente) |
| R7 | HU-03 | CA-3.3 | (pendiente) |
| R8 | HU-03 | CA-3.4, 3.5 | (pendiente) |

---

## Parte 2 · Plan de pruebas
(pendiente)

## Parte 3 · Diseño de casos de caja negra
(pendiente)

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
