from decimal import Decimal, ROUND_HALF_UP

CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.15,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.15,
    "RECARGO_FINDE": 2000,
}

# Constantes con nombre (antes eran numeros magicos)
PESO_MAXIMO = 50                    # PMAX
TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_POR_KG_EXCEDENTE = 800
DESCUENTO_FRECUENTE = 0.05
DESCUENTO_CUPON_ENVIO10 = 0.10
CUPON_ENVIO10 = "ENVIO10"
PRIMER_DIA_FIN_DE_SEMANA = 6        # sábado (el domingo es 7)
DIA_MINIMO = 1
DIA_MAXIMO = 7
COSTO_MINIMO = 5000
MULTIPLO_REDONDEO = 100
ZONAS_VALIDAS = ("urbana", "rural", "nacional")


def calc(peso, zona, cliente, dia, cupon=None, flag=False):
    if peso <= 0 or peso > PESO_MAXIMO:
        raise ValueError("peso inválido")
    if zona not in ZONAS_VALIDAS:
        raise ValueError("zona inválida")
    if dia < DIA_MINIMO or dia > DIA_MAXIMO:
        raise ValueError("día inválido")

    if peso <= CONFIG["L1"]:
        costo = TARIFA_TRAMO_1
    elif peso <= CONFIG["L2"]:
        costo = TARIFA_TRAMO_2
    else:
        costo = TARIFA_TRAMO_2 + (peso - CONFIG["L2"]) * TARIFA_POR_KG_EXCEDENTE

    if zona == "rural":
        costo = costo + costo * CONFIG["RECARGO_RURAL"]
    elif zona == "nacional":
        costo = costo + costo * CONFIG["RECARGO_NACIONAL"]

    if cliente == "frecuente":
        costo = costo - costo * DESCUENTO_FRECUENTE
    if cliente == "vip":
        costo = costo - costo * CONFIG["DESC_VIP"]
    if cupon == CUPON_ENVIO10:
        costo = costo - costo * DESCUENTO_CUPON_ENVIO10

    if dia >= PRIMER_DIA_FIN_DE_SEMANA:
        costo = costo + CONFIG["RECARGO_FINDE"]
    if costo < COSTO_MINIMO:
        costo = COSTO_MINIMO

    if flag:
        print("costo:", costo)
    redondeado = (Decimal(str(round(costo, 6))) / MULTIPLO_REDONDEO).quantize(
        Decimal(1), rounding=ROUND_HALF_UP)
    return int(redondeado) * MULTIPLO_REDONDEO
