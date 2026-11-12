from decimal import Decimal, ROUND_HALF_UP

CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.15,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.15,
    "RECARGO_FINDE": 2000,
}

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


def validar_entradas(peso, zona, dia):
    """R1 y R2: lanza ValueError si peso, zona o día no son válidos."""
    if peso <= 0 or peso > PESO_MAXIMO:
        raise ValueError("peso inválido")
    if zona not in ZONAS_VALIDAS:
        raise ValueError("zona inválida")
    if dia < DIA_MINIMO or dia > DIA_MAXIMO:
        raise ValueError("día inválido")


def calcular_tarifa_base(peso):
    """R3: tarifa según el tramo de peso."""
    if peso <= CONFIG["L1"]:
        return TARIFA_TRAMO_1
    if peso <= CONFIG["L2"]:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - CONFIG["L2"]) * TARIFA_POR_KG_EXCEDENTE


def aplicar_recargo_zona(costo, zona):
    """R4: recargo según la zona (la urbana no tiene)."""
    if zona == "rural":
        return costo + costo * CONFIG["RECARGO_RURAL"]
    if zona == "nacional":
        return costo + costo * CONFIG["RECARGO_NACIONAL"]
    return costo


def aplicar_descuento_cliente(costo, cliente):
    """R6: descuento según el tipo de cliente."""
    if cliente == "frecuente":
        return costo - costo * DESCUENTO_FRECUENTE
    if cliente == "vip":
        return costo - costo * CONFIG["DESC_VIP"]
    return costo


def aplicar_cupon(costo, cupon):
    """R6 y R7: aplica ENVIO10; cualquier otro cupón se ignora."""
    if cupon == CUPON_ENVIO10:
        return costo - costo * DESCUENTO_CUPON_ENVIO10
    return costo


def aplicar_recargo_fin_de_semana(costo, dia):
    """R5: suma el recargo en sábado y domingo, después de los descuentos."""
    if dia >= PRIMER_DIA_FIN_DE_SEMANA:
        return costo + CONFIG["RECARGO_FINDE"]
    return costo


def aplicar_costo_minimo(costo):
    """R8: el costo nunca es menor que el mínimo."""
    return max(costo, COSTO_MINIMO)


def redondear_al_centenar(costo):
    """R8: redondea al múltiplo de 100 más cercano; los 50 suben."""
    centenas = (Decimal(str(round(costo, 6))) / MULTIPLO_REDONDEO).quantize(
        Decimal(1), rounding=ROUND_HALF_UP)
    return int(centenas) * MULTIPLO_REDONDEO


def calc(peso, zona, cliente, dia, cupon=None, flag=False):
    validar_entradas(peso, zona, dia)
    costo = calcular_tarifa_base(peso)
    costo = aplicar_recargo_zona(costo, zona)
    costo = aplicar_descuento_cliente(costo, cliente)
    costo = aplicar_cupon(costo, cupon)
    costo = aplicar_recargo_fin_de_semana(costo, dia)
    costo = aplicar_costo_minimo(costo)
    if flag:
        print("costo:", costo)
    return redondear_al_centenar(costo)
