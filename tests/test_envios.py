# tests/test_envios.py
# Resultados esperados calculados a mano con MI especificación (código 0182410054).
import pytest
from envios import calc

CASOS = [
    # (id, peso, zona, cliente, dia, cupon, esperado)
    ("CP-01", 0, "urbana", "normal", 2, None, ValueError),
    ("CP-02", 0.1, "urbana", "normal", 2, None, 6000),
    ("CP-03", 3, "urbana", "normal", 2, None, 6000),
    ("CP-04", 3.1, "urbana", "normal", 2, None, 9000),
    ("CP-05", 10, "urbana", "normal", 2, None, 9000),
    ("CP-06", 10.1, "urbana", "normal", 2, None, 9100),
    ("CP-07", 50, "urbana", "normal", 3, None, 41000),
    ("CP-08", 50.1, "urbana", "normal", 3, None, ValueError),
    ("CP-09", -5, "urbana", "normal", 2, None, ValueError),
    ("CP-10", 12, "rural", "normal", 2, None, 12200),
    ("CP-11", 12, "nacional", "normal", 2, None, 15400),
    ("CP-12", 5, "insular", "normal", 2, None, ValueError),
    ("CP-13", 5, "urbana", "normal", 0, None, ValueError),
    ("CP-14", 5, "urbana", "normal", 8, None, ValueError),
    ("CP-15", 12, "urbana", "normal", 2, None, 10600),
    ("CP-16", 12, "urbana", "normal", 6, None, 12600),
    ("CP-17", 12, "urbana", "normal", 2, 'ENVIO10', 9500),
    ("CP-18", 12, "urbana", "normal", 6, 'ENVIO10', 11500),
    ("CP-19", 12, "urbana", "frecuente", 2, None, 10100),
    ("CP-20", 12, "urbana", "frecuente", 6, None, 12100),
    ("CP-21", 12, "urbana", "frecuente", 2, 'ENVIO10', 9100),
    ("CP-22", 12, "urbana", "frecuente", 6, 'ENVIO10', 11100),
    ("CP-23", 12, "urbana", "vip", 2, None, 9000),
    ("CP-24", 12, "urbana", "vip", 7, None, 11000),
    ("CP-25", 12, "urbana", "vip", 2, 'ENVIO10', 8100),
    ("CP-26", 12, "urbana", "vip", 7, 'ENVIO10', 10100),
    ("CP-27", 3, "urbana", "normal", 2, 'PROMO5', 6000),
    ("CP-28", 3, "urbana", "vip", 2, 'ENVIO10', 5000),
    ("CP-29", 5, "rural", "normal", 2, None, 10400),
    ("CP-30", 3, "urbana", "vip", 6, 'ENVIO10', 6600),
    ("CP-31", 20, "nacional", "vip", 7, 'ENVIO10', 20900),
    ("CP-32", 3, "rural", "frecuente", 6, None, 8600),
]

@pytest.mark.parametrize("cid,peso,zona,cliente,dia,cupon,esperado", CASOS,
                         ids=[c[0] for c in CASOS])
def test_calc(cid, peso, zona, cliente, dia, cupon, esperado):
    if esperado is ValueError:
        with pytest.raises(ValueError):
            calc(peso, zona, cliente, dia, cupon)
    else:
        assert calc(peso, zona, cliente, dia, cupon) == esperado
