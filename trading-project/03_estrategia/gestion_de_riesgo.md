# Gestión de Riesgo (binarias) — versión simple y ejecutable

**Objetivo:** sobrevivir + estabilizar ejecución.
En binaria, el edge es chico: el riesgo debe ser **aburrido y constante**.

---

## 1) Principios

- **Riesgo fijo por operación** (definido antes de empezar) :contentReference[oaicite:11]{index=11}
- El tamaño NO cambia por emoción (prohibido “recuperar”) :contentReference[oaicite:12]{index=12}
- Un día “válido” es el que respeta reglas, no el que más gana

---

## 2) Unidades (R) para pensar claro

- 1R = tu stake base (ej: 5 USD o 10 USD)
- Win típico ≈ +0.80R a +0.85R (según payout) :contentReference[oaicite:13]{index=13}
- Loss = -1R
- Tie = 0R

Tu enfoque es **defender R**, no “hacer dinero hoy”.

---

## 3) Límites operativos (con tus reglas)

- Máximo **8 operaciones/día** :contentReference[oaicite:14]{index=14}
- **3 pérdidas consecutivas = STOP inmediato** :contentReference[oaicite:15]{index=15}
- Si rompo una regla → sesión inválida (aunque termine verde) :contentReference[oaicite:16]{index=16}

---

## 4) Límites de pérdida por día (recomendación práctica)

Elige UNO (simple) y no lo negocies:

### Opción A (más conservadora)

- **Max Daily Loss = -3R** (ej: 3 pérdidas netas) → STOP del día

### Opción B (si tu día típico tiene 6–8 trades)

- **Max Daily Loss = -4R** → STOP del día

> Nota: con payout ~0.83R, recuperar un -4R requiere muchas operaciones buenas.
> Mejor cortar temprano.

---

## 5) Stake base y escalamiento (prohibido martingala emocional)

**Regla:** no se escala por pérdida. Se escala solo por **condición A+** predefinida.

### Stake base

- Trade #1 a #N: siempre **1R** (monto fijo)

### Excepción “A+” (muy rara)

Puedes permitir **máximo 1 trade A+ por sesión** en 1.5R SOLO si:

- Checklist completo + mercado operable + no hay presión emocional
- Aún no hay 2 pérdidas seguidas
- No es para recuperar
  Si hay duda → 1R.

---

## 6) Selección por activo (riesgo también es “dónde opero”)

Tu análisis muestra que excluir BTC y GBP mejora mucho el EV de la muestra. :contentReference[oaicite:17]{index=17}
Por lo tanto:

- Si el día está “feo”, **reduce universo** a EUR/USD (core) en vez de saltar de activo.

---

## 7) Registro mínimo (para tu bot / sesiones)

Tu Excel de sesiones ya contempla:

- emotion_start, energy, sleep_quality
- blocked_no_trade
- rules_compliance
- wins/losses/breakevens
- notes

Regla: si activaste STOP o evitaste operar por filtro, se registra como victoria de proceso.
