# tests/test_hora_pico.py
# Solicitud de cambio (A + F) mod 3 = 2: hora pico.
# Pruebas escritas ANTES de implementar el cambio. Esperados calculados a mano.
import pytest
from envios import calc

CASOS_HORA = [
    # (id, peso, zona, cliente, dia, cupon, hora, esperado)
    ("CP-41", 3, "urbana", "normal", 2, None, 16, 6000),
    ("CP-42", 3, "urbana", "normal", 2, None, 17, 6500),
    ("CP-43", 3, "urbana", "normal", 2, None, 18, 6500),
    ("CP-44", 3, "urbana", "normal", 2, None, 19, 6500),
    ("CP-45", 3, "urbana", "normal", 2, None, 20, 6000),
    ("CP-46", 3, "urbana", "normal", 2, None, 0, 6000),
    ("CP-47", 3, "urbana", "normal", 2, None, 23, 6000),
    ("CP-48", 3, "urbana", "normal", 2, None, -1, ValueError),
    ("CP-49", 3, "urbana", "normal", 2, None, 24, ValueError),
    ("CP-50", 3, "urbana", "normal", 2, None, None, 6000),
    ("CP-51", 12, "rural", "normal", 2, None, 18, 13200),
    ("CP-52", 3, "urbana", "normal", 6, None, 18, 8500),
    ("CP-53", 12, "nacional", "vip", 3, 'ENVIO10', 19, 12700),
    ("CP-54", 3, "urbana", "vip", 2, 'ENVIO10', 17, 5000),
    ("CP-55", 3, "rural", "frecuente", 7, None, 17, 9100),
]


@pytest.mark.parametrize("cid,peso,zona,cliente,dia,cupon,hora,esperado", CASOS_HORA,
                         ids=[c[0] for c in CASOS_HORA])
def test_hora_pico(cid, peso, zona, cliente, dia, cupon, hora, esperado):
    if esperado is ValueError:
        with pytest.raises(ValueError):
            calc(peso, zona, cliente, dia, cupon, hora=hora)
    else:
        assert calc(peso, zona, cliente, dia, cupon, hora=hora) == esperado


def test_hora_solo_por_nombre():
    """hora es solo por nombre: una llamada vieja con un 6.º argumento posicional sigue fallando."""
    with pytest.raises(TypeError):
        calc(3, "urbana", "normal", 2, None, 18)
