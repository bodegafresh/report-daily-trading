# TRADER CONSISTENTE 2026 🧱📈

Repositorio para construir un sistema de trading **consistente, disciplinado y emocionalmente estable**, usando datos reales (tu herramienta de registro) y un marco de trabajo por **pilares** (hábitos, mentalidad, estrategia, emociones y métricas).

> **Norte del proyecto**
> Pasar de _práctica en demo con enfoque_ → a _operación real controlada_ desde **01/02/2026**, con reglas claras y métricas que mandan.

---

## 🎯 Objetivo 2026 (NORTE)

- **Inicio real:** 01/02/2026
- **Modo actual (enero 2026):** Demo / entrenamiento
- **Riesgo por operación (real):** **USD 5–10**
- **Operaciones diarias (real):** **5 a 8**
- **Enfoque principal:** **consistencia + ejecución de reglas** (no “ganar por ganar”)
- **Métrica madre:** **% de reglas respetadas** (la rentabilidad viene después)

---

## 🧭 Cómo trabajar este repo (conversaciones en paralelo)

Este proyecto se divide en **5 pilares**.
La idea es que tengas **conversaciones separadas** (conmigo o contigo mismo) por pilar, sin mezclar temas:

1. **Disciplina** → reglas, rutinas, no-negociables
2. **Mentalidad** → identidad, creencias, narrativa interna
3. **Estrategia** → checklist de entrada/no-entrada, escenarios prohibidos
4. **Control emocional** → escalas, protocolos STOP, triggers
5. **Métricas y revisión** → dashboards, revisión semanal/mensual, condiciones para pasar a real

> ✅ Una conversación = un pilar = un avance concreto.
> ❌ Evitar conversaciones “mezcladas” (estrategia + emociones + dudas + ajustes) porque terminan en caos.

---

## 🧱 Los 5 pilares del sistema

### 01) Disciplina (80% del resultado)

**Objetivo:** hacer lo correcto incluso cuando no apetece.

**Incluye:**

- Reglas no negociables
- Rutina diaria / pre-market / post-market
- Protocolo para días malos
- Límites de operaciones y pérdidas

---

### 02) Mentalidad (identidad del trader)

**Objetivo:** operar desde proceso y probabilidad, no desde urgencia, ego o necesidad.

**Incluye:**

- Identidad del trader que estás construyendo
- Creencias limitantes
- Reglas de pensamiento
- Narrativa interna

---

### 03) Estrategia (simple y repetible)

**Objetivo:** tener **UNA estrategia oficial** (y no cinco medias estrategias).

**Incluye:**

- Estrategia oficial (setup y reglas)
- Checklist de entrada
- Checklist de NO entrada (filtro)
- Gestión de riesgo
- Escenarios prohibidos

---

### 04) Control emocional (en tiempo real)

**Objetivo:** detectar emoción antes de que controle el mouse.

**Incluye:**

- Escala emocional 1–10 (antes de operar)
- Protocolo STOP (cuándo parar)
- Lista de emociones recurrentes
- Auto-chequeo en vivo

---

### 05) Métricas y revisión (realidad, no opinión)

**Objetivo:** que los datos manden, no la memoria.

**Incluye:**

- Métricas clave (winrate, PF, drawdown, reglas)
- Revisión semanal y mensual
- Condiciones para operar en real (gate)
- Comparación de performance por activo/horario/emoción

---

## ✅ Condiciones para operar en real (Gate 01/02/2026)

Para evitar “tirarte al agua” con emoción, el salto a real se hace con criterios:

- **20 sesiones consecutivas** respetando reglas
- **Winrate ≥ 58%** (o el umbral que definas según payout)
- **Sin martingala** (ni “recuperación” emocional)
- Rutina cumplida **≥ 90%**
- Control emocional estable (sin tilt recurrente)

> Nota: Si ganas rompiendo reglas, **eso cuenta como pérdida del sistema**.

---

## 🗂️ Estructura del repositorio

Este repo contiene:

1. Tu **herramienta de tracking** (app Python)
2. El **marco TRADER CONSISTENTE 2026** (carpetas por pilar)

```text
report-daily-trading/
├── trades_gui.py                # Aplicación principal (UI, lógica y reportes)
├── trades.csv                   # Registro de operaciones (cabecera auto-generada)
├── sessions.csv                 # Registro de sesiones cronometradas
├── trading_log.md               # Reporte manual alternativo (histórico)
├── report.md                    # Reporte generado (MD) - opcional
├── build/, dist/                # Artefactos de PyInstaller (opcional)
├── trades_gui.spec              # Especificación de build para PyInstaller
│
├── trading-project/             # ✅ TRADER CONSISTENTE 2026 (framework)
│   ├── README.md                # Este documento (si decides moverlo aquí)
│   ├── 00_objetivo_y_reglas/
│   │   ├── objetivo_2026.md
│   │   ├── reglas_no_negociables.md
│   │   └── condiciones_para_real.md
│   │
│   ├── 01_disciplina/
│   │   ├── reglas_no_negociables.md
│   │   ├── rutina_diaria.md
│   │   ├── rutina_pre_market.md
│   │   ├── rutina_post_market.md
│   │   └── protocolo_dias_malos.md
│   │
│   ├── 02_mentalidad/
│   │   ├── identidad_del_trader.md
│   │   ├── creencias_limitantes.md
│   │   ├── narrativa_interna.md
│   │   └── reglas_de_pensamiento.md
│   │
│   ├── 03_estrategia/
│   │   ├── estrategia_oficial.md
│   │   ├── checklist_entrada.md
│   │   ├── checklist_no_entrada.md
│   │   ├── gestion_de_riesgo.md
│   │   └── escenarios_prohibidos.md
│   │
│   ├── 04_control_emocional/
│   │   ├── escala_emocional.md
│   │   ├── protocolo_stop.md
│   │   ├── emociones_recurrentes.md
│   │   └── auto_chequeo_en_vivo.md
│   │
│   └── 05_metricas_y_revision/
│       ├── metricas_clave.md
│       ├── revision_semanal.md
│       ├── revision_mensual.md
│       └── bitacora_aprendizajes.md
│
└── README.md                    # (Opcional) README general del repo
```

> Sugerencia práctica:
>
> - Mantén el README actual (de la app) como **README_APP.md**
> - Y usa este como **README.md** (del proyecto global)
> - O bien deja este dentro de `trading-project/README.md`

---

## 🧰 La herramienta (tracking) — resumen rápido

La app de escritorio (Python + tkinter) permite:

- Registrar operaciones con campos controlados
- Guardar en CSV (`trades.csv`, `sessions.csv`)
- Calcular estadísticas (win rate, PnL, objetivos)
- Cronometrar tiempo efectivo
- Exportar reportes en Markdown

### Ejecutar

```bash
python trades_gui.py
```

---

## 🧩 Flujo de trabajo recomendado (enero 2026 → febrero 2026)

### Enero 2026 (Demo / entrenamiento)

- Objetivo diario: **cumplir reglas**
- 5–8 operaciones máximas
- Si hay lateralidad: **no operar**
- Registrar emoción antes y después

### Desde 01/02/2026 (Real controlado)

- Operaciones de **USD 5–10**
- 5–8 operaciones/día
- STOP por pérdidas consecutivas
- No subir monto por emoción
- Revisión semanal obligatoria

---

## 🗣️ Cómo pedirme ayuda (prompts útiles)

Copia y pega según lo que quieras trabajar:

- **Disciplina:**
  “Ayúdame a ajustar mis reglas no negociables y mi rutina diaria. Quiero que sean realistas y medibles.”

- **Mentalidad:**
  “Hoy siento urgencia por recuperar dinero. Ayúdame a reencuadrar esto y a crear un guion mental antes de operar.”

- **Estrategia:**
  “Quiero que mi estrategia oficial quede en una sola página. Aquí está mi checklist actual; simplifícalo y hazlo más estricto.”

- **Control emocional:**
  “Estoy entrando por aburrimiento. Diseña un protocolo STOP específico para mí y señales tempranas de tilt.”

- **Métricas:**
  “Analicemos trades.csv y sessions.csv: ¿cuáles son mis mejores horarios/activos y qué emoción se asocia a mis pérdidas?”

---

## 📌 Licencia / Nota

Este repositorio es un proyecto personal de mejora continua.
Si lo haces público, evita publicar credenciales o información sensible.

---

Autor: @bodegafresh · 2026
