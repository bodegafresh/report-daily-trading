# Estrategia Oficial — “3/6/21 + Volatilidad + Momentum”

**Mercado:** Fixed Time (binarias) sobre Forex (principal) + índices compuestos (entrenamiento fin de semana)
**TF de ejecución:** 1m (timing)
**TF de sesgo:** 5m (dirección / filtro)
**Expiraciones:** 1m y 5m (según contexto)

> Objetivo: una estrategia **simple, repetible y filtrada**.
> No se busca “adivinar”: se busca **operar solo cuando el mercado está operable**.

---

## 1) Indicadores (set final)

**En gráfico 1m y 5m:**

- **EMA 3** (gatillo)
- **EMA 6** (gatillo / micro-impulso)
- **EMA 21** (tendencia operable)
- _(Opcional recomendado)_ **EMA 50** (filtro de dirección, reduce falsos en Forex)

**Volatilidad / contexto**

- **Bollinger Bands (20, 2)**

**Momentum**

- **RSI (7)**
- **MACD (5, 13, 3)** _(o el equivalente rápido de tu plataforma)_

---

## 2) Universo de activos (regla estratégica)

Según tu muestra cuantitativa, el edge cambia drásticamente por activo:

- **Evitar como activo “core”: BTC/USD** (EV muy negativo en la muestra). :contentReference[oaicite:2]{index=2}
- **GBP/USD en “observación”**: en tu muestra está negativo; solo se opera si cumple filtros estrictos o se elimina del plan. :contentReference[oaicite:3]{index=3}
- **Core recomendado (para construir consistencia): EUR/USD** (mejor comportamiento relativo vs GBP en tu dataset). :contentReference[oaicite:4]{index=4}
- **Fines de semana (entrenamiento):** índices compuestos (Asia/Compound/Euro) como “simulador”, pero **no se usan para evaluar tu edge principal**.

**Regla de foco:** máximo **2 activos por sesión**. (Menos decisiones = mejor ejecución)

---

## 3) Concepto central: “Mercado operable”

Tu estrategia gana cuando se cumplen 3 cosas:

1. **Dirección clara** (EMA21 con pendiente y estructura)
2. **Volatilidad suficiente** (Bollinger abre / deja de apretar)
3. **Momentum confirmando** (RSI y/o MACD salen de zona neutra)

Si falta 1 → **NO TRADE**.

---

## 4) Sesgo (5m) y Timing (1m)

### A) Sesgo en 5m (antes de buscar entradas en 1m)

- Solo busco **CALL** si:
  - Precio por encima de EMA21 en 5m
  - EMA21 con pendiente alcista
  - (Opcional) precio también sobre EMA50
- Solo busco **PUT** si:
  - Precio por debajo de EMA21 en 5m
  - EMA21 con pendiente bajista
  - (Opcional) precio también bajo EMA50

### B) Timing en 1m (la entrada real)

Busco uno de estos 2 modelos:

**Modelo 1 — Continuación con pullback (el más “limpio”)**

- Tendencia definida (EMA21 inclinada)
- Pullback hacia EMA6 o EMA21
- Vela de rechazo + recuperación de momentum
- Entrada en la 1ra o 2da vela de reanudación

**Modelo 2 — Reversión a la media (solo en extremos)**

- Precio “fuera” o tocando banda externa + señal de agotamiento
- RSI extremo (no neutro) + pérdida de momentum (MACD histo se achica)
- Confirmación con vela (rechazo / envolvente)
- Entrada buscando retorno a banda media / EMA21

> Nota: tus screenshots de pérdidas muestran que entrar en “medio del rango” (sin tendencia + Bollinger apretado) te castiga. Eso queda prohibido.

---

## 5) Elección de expiración (regla simple)

- **1 minuto** SOLO si:
  - Hay impulso (velas con cuerpo, poca mecha)
  - Bollinger está abriendo o ya abierta
  - Entrada no es tarde
- **5 minutos** si:
  - Es pullback a EMA21 en tendencia
  - Hay estructura pero el 1m está ruidoso
  - Quieres “aire” para evitar el ruido del 1m

---

## 6) Reglas de sesión (por encima de la estrategia)

Las reglas no negociables mandan:

- Máx 8 operaciones/día
- 3 pérdidas seguidas = STOP
- Prohibido martingala emocional / aumentar por recuperar
- No operar en lateralidad clara
- No operar por aburrimiento/urgencia :contentReference[oaicite:5]{index=5}

---

## 7) Qué es un “buen trade”

Un trade es **bueno** si:

- Cumplió checklist (entrada)
- No violó escenarios prohibidos
- Fue ejecutado con calma (sin persecución)

El resultado (win/loss) es secundario frente a la calidad del proceso.
