# tests/test_caja_blanca.py
# Casos de caja blanca (caminos independientes) y casos adicionales.
# Resultados esperados calculados a mano con MI especificacion (codigo 0182410054).
import pytest
from envios import calc

CASOS_BLANCA = [
    # (id, peso, zona, cliente, dia, cupon, esperado)
    ("CP-33", 3, "rural",    "normal",    2, None, 6900),   # 6000 x 1,15
    ("CP-34", 3, "nacional", "normal",    2, None, 8700),   # 6000 x 1,45
    ("CP-35", 3, "urbana",   "normal",    7, None, 8000),   # 6000 + 2000 (domingo)
    ("CP-36", 3, "urbana",   "frecuente", 2, None, 5700),   # 6000 x 0,95
    ("CP-37", 3, "urbana",   "vip",       2, None, 5100),   # 6000 x 0,85
    ("CP-38", 3, "urbana",   "normal",    2, "ENVIO10", 5400),  # 6000 x 0,90
]

@pytest.mark.parametrize("cid,peso,zona,cliente,dia,cupon,esperado",
                         CASOS_BLANCA, ids=[c[0] for c in CASOS_BLANCA])
def test_caja_blanca(cid, peso, zona, cliente, dia, cupon, esperado):
    assert calc(peso, zona, cliente, dia, cupon) == esperado


def test_cp39_flag_eliminado(capsys):
    """CP-39 (actualizado en v2.0.0): el argumento flag ya no existe y calc no imprime."""
    with pytest.raises(TypeError):
        calc(3, "urbana", "normal", 2, None, True)
    assert calc(3, "urbana", "normal", 2, None) == 6000
    assert capsys.readouterr().out == ""


def test_cp40_mensaje_peso_invalido():
    """CP-40: R1 pide exactamente el mensaje 'peso inválido' (con tilde)."""
    with pytest.raises(ValueError) as error:
        calc(0, "urbana", "normal", 2)
    assert str(error.value) == "peso inválido"
