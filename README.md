# Report Daily Trading

## Descripción general

Aplicación de escritorio creada en Python para llevar un registro diario de operaciones de trading discrecional. Proporciona una interfaz gráfica construida con `tkinter` que permite capturar operaciones, visualizar estadísticas clave, monitorear objetivos diarios de PnL y tiempo efectivo, y generar reportes en formato Markdown.

El proyecto está pensado para traders minoristas que desean documentar su desempeño, emociones y notas asociadas a cada operación sin depender de hojas de cálculo manuales.

## Características principales

- **Registro estructurado de operaciones:** formulario rápido con campos controlados (`activo`, `timeframe`, `dirección`, `resultado`, `payout`, `emoción`, `notas`).
- **Persistencia en CSV:** las operaciones se guardan en `trades.csv` y las sesiones de tiempo efectivo en `sessions.csv`.
- **Estadísticas automáticas:** win rate diario y acumulado, conteo de operaciones, PnL neto, progresos contra objetivos personalizados.
- **Cronómetro integrado:** iniciar, pausar y finalizar sesiones, con persistencia del tiempo efectivo diario.
- **Gráfico embebido:** barras de operaciones por hora y línea de PnL acumulado para la jornada actual, gracias a `matplotlib`.
- **Exportación a Markdown:** generación de un reporte consolidado (`report.md`) listo para compartir o archivar.

## Capturas / Demo

> Añade capturas de pantalla o GIFs del flujo principal cuando las tengas disponibles. Esto ayuda a entender rápidamente la experiencia de usuario.

## Estructura del repositorio

```text
report-daily-trading/
├── trades_gui.py       # Aplicación principal (UI, lógica y reportes)
├── trades.csv          # Registro de operaciones (cabecera auto-generada)
├── sessions.csv        # Registro de sesiones cronometradas
├── trading_log.md      # Reporte manual alternativo (histórico)
├── README.md           # Este documento
├── build/, dist/       # Artefactos generados por PyInstaller (opcional)
└── trades_gui.spec     # Especificación de build para PyInstaller
```

## Requisitos previos

- macOS, Linux o Windows con Python 3.10+ (probado en macOS).
- Librerías Python listadas en la sección siguiente.

### Dependencias Python

El proyecto se apoya exclusivamente en módulos de la biblioteca estándar y `matplotlib`. Puedes instalarlos en un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install matplotlib
```

> `tkinter` viene incluido en la instalación oficial de Python (en macOS puede requerir `python-tk` desde brew si usas distribuciones alternativas).

## Uso

1. **Preparar los archivos CSV** (auto-creados si no existen):
   - `trades.csv`
   - `sessions.csv`
2. **Ejecutar la aplicación:**

   ```bash
   python trades_gui.py
   ```

3. **Registrar operaciones:** completa el formulario y presiona `Agregar operación`.
4. **Cronometrar la sesión:** usa `Iniciar`, `Pausar`, `Finalizar` para registrar duración efectiva.
5. **Actualizar estadísticas y gráfico:** el panel lateral y la visualización se recalculan automáticamente; también puedes forzar con `Actualizar gráfico`.
6. **Exportar reporte:** `Generar reporte (MD)` crea `report.md` con métricas y tabla de operaciones.

### Atajos y detalles útiles

- Los combos (`activo`, `timeframe`, etc.) restringen la entrada a valores válidos para mantener consistencia del dataset.
- El progreso de objetivos se basa en variables configurables dentro de la interfaz (`PnL objetivo`, `Min. efectivos`).
- El cronómetro persiste el tiempo del día en archivos `.elapsed_YYYY-MM-DD.txt` para evitar pérdidas si la app se reinicia.
- La función `Cargar CSV` permite importar registros desde otra fuente (sobrescribe `trades.csv`).

## Reportes

La opción `Generar reporte (MD)` produce `report.md` en la raíz del proyecto. Incluye win rate y PnL (diario y acumulado) más una tabla de todas las operaciones registradas en `trades.csv`.

## Build como ejecutable

El repositorio incluye artefactos de PyInstaller (`build/`, `dist/`, `trades_gui.spec`). Para generar un binario independiente:

```bash
pip install pyinstaller
pyinstaller trades_gui.spec
```

El ejecutable quedará en `dist/trades_gui`. Puedes empaquetarlo para distribuir la aplicación sin depender de Python instalado.

## Contribución y mantenimiento

- Ajusta los catálogos (`ASSETS`, `TIMEFRAMES`, `DIRECTIONS`, `OUTCOMES`, `EMOTIONS`) directamente en `trades_gui.py` según tus necesidades.
- Si deseas internacionalizar la app, centraliza los textos de la UI en una sección dedicada y considera extraerlos a archivos de traducción.
- Añade pruebas específicas para las funciones de cálculo (`_recalc_stats`, `_make_md_report`) si decides extraerlas a módulos independientes.

## Próximos pasos sugeridos

- Añadir filtros por fecha/activo en la UI para facilitar análisis histórico.
- Generar dashboards adicionales (por semana/mes) y métricas sobre emociones.
- Incorporar guardado automático incremental o sincronización con bases de datos remotas.

---

Autor: @bodegafresh · 2025
