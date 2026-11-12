# tabla_casos.py
# Muestra en la terminal una tabla con todos los casos de prueba:
# entradas, resultado esperado (calculado a mano), resultado obtenido y si pasa o falla.
#
# Uso (desde la carpeta del proyecto):   python tabla_casos.py
from envios import calc
from tests.test_envios import CASOS
from tests.test_caja_blanca import CASOS_BLANCA

try:                                   # solo existe después de la Parte 8
    from tests.test_hora_pico import CASOS_HORA
except ImportError:
    CASOS_HORA = []


def en_pesos(valor):
    """Formatea 10100 como $10.100; los errores se muestran como 'Error'."""
    if valor is ValueError or valor == "Error":
        return "Error"
    return "${:,}".format(valor).replace(",", ".")


def obtener(peso, zona, cliente, dia, cupon, hora):
    """Ejecuta calc; si lanza ValueError devuelve 'Error'."""
    try:
        if hora is None:
            return calc(peso, zona, cliente, dia, cupon)
        return calc(peso, zona, cliente, dia, cupon, hora=hora)
    except ValueError:
        return "Error"


# Se unifican las tres listas en un mismo formato:
# (id, peso, zona, cliente, dia, cupon, hora, esperado)
filas = [(c[0], c[1], c[2], c[3], c[4], c[5], None, c[6]) for c in CASOS + CASOS_BLANCA]
filas += list(CASOS_HORA)

encabezado = ["ID", "Peso", "Zona", "Cliente", "Día", "Cupón", "Hora", "Esperado", "Obtenido", "Resultado"]
datos, pasan = [], 0
for cid, peso, zona, cliente, dia, cupon, hora, esperado in filas:
    obtenido = obtener(peso, zona, cliente, dia, cupon, hora)
    ok = obtenido == ("Error" if esperado is ValueError else esperado)
    pasan += ok
    datos.append([cid, str(peso).replace(".", ","), zona, cliente, str(dia), cupon or "-",
                  "-" if hora is None else str(hora), en_pesos(esperado), en_pesos(obtenido),
                  "OK" if ok else "FALLA"])

anchos = [max(len(str(f[i])) for f in [encabezado] + datos) for i in range(len(encabezado))]
linea = "+-" + "-+-".join("-" * a for a in anchos) + "-+"


def fila(valores):
    return "| " + " | ".join(str(v).ljust(a) for v, a in zip(valores, anchos)) + " |"


print(linea)
print(fila(encabezado))
print(linea)
for d in datos:
    print(fila(d))
print(linea)
total = len(datos)
print(f"Casos: {total}   Pasan: {pasan}   Fallan: {total - pasan}   Porcentaje que pasa: {pasan / total * 100:.1f} %".replace(".", ","))
