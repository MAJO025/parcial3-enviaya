# Changelog

Todos los cambios importantes de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [2.0.0] - 2026-11-11

### Added
- Patrón Estrategia para el recargo por zona: clase abstracta `RecargoZona` y las
  estrategias `ZonaUrbana`, `ZonaRural` y `ZonaNacional`.
- Funciones con una sola responsabilidad: `validar_entradas`, `calcular_tarifa_base`,
  `aplicar_recargo_zona`, `aplicar_descuento_cliente`, `aplicar_cupon`,
  `aplicar_recargo_fin_de_semana`, `aplicar_costo_minimo` y `redondear_al_centenar`.
- Diagrama de clases UML del patrón Estrategia (`evidencias/uml_estrategia_zonas.png`).

### Changed
- Los números mágicos ahora son constantes con nombre (`PESO_MAXIMO`, `COSTO_MINIMO`, etc.).
- Los parámetros de `calc` tienen nombres descriptivos: `peso`, `zona`, `cliente`, `dia`, `cupon`.
- El caso de prueba CP-39 ahora verifica que `flag` ya no existe.

### Removed
- **Cambio incompatible:** se elimina el argumento `flag` de `calc` y el `print` interno.
  Quien llamaba `calc(..., flag=True)` ahora recibe un `TypeError`.
- Código muerto (`t = t` en la zona urbana).

## [1.0.1] - 2026-11-11

### Added
- Suite de 40 pruebas automatizadas con pytest (32 de caja negra y 8 de caja blanca).
- Configuración de pytest (`pytest.ini`) y dependencias de desarrollo (`requirements-dev.txt`).

### Fixed
- DEF-01: el sábado ahora suma el recargo de fin de semana (R5).
- DEF-02: el recargo de fin de semana se suma después de los descuentos (R5).
- DEF-03: el costo se redondea al múltiplo de $100 más cercano y los $50 suben (R8).
- DEF-04: se validan la zona y el día y se lanza `ValueError` si no son válidos (R2).
- DEF-05: el mensaje de error del peso es "peso inválido", con tilde (R1).

## [1.0.0] - 2026-11-11

### Added
- Versión heredada de la función `calc` para el cálculo del costo de envío, con `CONFIG`
  personalizado (sin modificaciones).

[Unreleased]: https://github.com/MAJO025/parcial3-enviaya/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/MAJO025/parcial3-enviaya/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/MAJO025/parcial3-enviaya/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/MAJO025/parcial3-enviaya/releases/tag/v1.0.0
