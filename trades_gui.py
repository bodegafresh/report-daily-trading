#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# --- Matplotlib embebido ---
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Archivos
TRADES_CSV = Path("trades.csv")
SESSIONS_CSV = Path("sessions.csv")

# Catálogos controlados
ASSETS = ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CAD", "EUR/JPY", "EUR/GBP"]
TIMEFRAMES = ["1m", "5m"]
DIRECTIONS = ["↑", "↓"]
OUTCOMES = ["win", "loss", "tie"]
EMOTIONS = ["Neutral", "Confiado", "Enfocado", "Ansioso", "Impulsivo", "Cansado", "Frustrado"]

# Columnas tabla
COLUMNS = [
    "datetime","date","asset","timeframe","amount",
    "direction","outcome","payout_pct","pnl","emotion","notes"
]

def ensure_headers(path: Path, headers: list[str]):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)

def parse_float(s, default=0.0):
    try:
        return float(s)
    except:
        return default

class TradingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Trading")
        self.geometry("1280x760")
        self.minsize(1100, 640)

        ensure_headers(TRADES_CSV, COLUMNS)
        ensure_headers(SESSIONS_CSV, ["session_id","start","end","duration_min","notes"])

        # Objetivos por defecto
        self.daily_target_pnl = tk.DoubleVar(value=20.0)   # USD
        self.daily_target_minutes = tk.IntVar(value=60)    # minutos

        self._build_ui()
        self._load_trades()
        self._recalc_stats()
        self._tick_timer()   # loop cronómetro
        self._refresh_chart()  # inicializa gráfico

    # ---------- UI ----------
    def _build_ui(self):
        # TOP: inputs
        top = ttk.Frame(self, padding=6)
        top.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top, text="Activo").grid(row=0, column=0, sticky="w", padx=2)
        self.asset_cb = ttk.Combobox(top, values=ASSETS, width=10, state="readonly")
        self.asset_cb.set(ASSETS[0]); self.asset_cb.grid(row=0, column=1, padx=2)

        ttk.Label(top, text="Timeframe").grid(row=0, column=2, sticky="w", padx=2)
        self.tf_cb = ttk.Combobox(top, values=TIMEFRAMES, width=5, state="readonly")
        self.tf_cb.set("1m"); self.tf_cb.grid(row=0, column=3, padx=2)

        ttk.Label(top, text="Monto (USD)").grid(row=0, column=4, sticky="w", padx=2)
        self.amount_var = tk.StringVar(value="10")
        ttk.Entry(top, textvariable=self.amount_var, width=7).grid(row=0, column=5, padx=2)

        ttk.Label(top, text="Dirección").grid(row=0, column=6, sticky="w", padx=2)
        self.dir_cb = ttk.Combobox(top, values=DIRECTIONS, width=3, state="readonly")
        self.dir_cb.set("↓"); self.dir_cb.grid(row=0, column=7, padx=2)

        ttk.Label(top, text="Resultado").grid(row=0, column=8, sticky="w", padx=2)
        self.out_cb = ttk.Combobox(top, values=OUTCOMES, width=5, state="readonly")
        self.out_cb.set("win"); self.out_cb.grid(row=0, column=9, padx=2)

        ttk.Label(top, text="Payout %").grid(row=0, column=10, sticky="w", padx=2)
        self.payout_var = tk.StringVar(value="82")
        ttk.Entry(top, textvariable=self.payout_var, width=5).grid(row=0, column=11, padx=2)

        ttk.Label(top, text="Emoción").grid(row=0, column=12, sticky="w", padx=2)
        self.emotion_cb = ttk.Combobox(top, values=EMOTIONS, width=10, state="readonly")
        self.emotion_cb.set("Neutral"); self.emotion_cb.grid(row=0, column=13, padx=2)

        ttk.Label(top, text="Notas").grid(row=0, column=14, sticky="w", padx=2)
        self.notes_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.notes_var, width=22).grid(row=0, column=15, padx=2)

        # fila botones
        btns = ttk.Frame(self, padding=(6,2))
        btns.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(btns, text="Agregar operación", command=self.add_trade).grid(row=0, column=0, padx=3)
        ttk.Button(btns, text="Cargar CSV", command=self.load_csv).grid(row=0, column=1, padx=3)
        ttk.Button(btns, text="Borrar seleccionada", command=self.delete_selected).grid(row=0, column=2, padx=3)
        ttk.Button(btns, text="Generar reporte (MD)", command=self.export_md).grid(row=0, column=3, padx=3)
        ttk.Button(btns, text="Actualizar gráfico", command=self._refresh_chart).grid(row=0, column=4, padx=3)

        # RIGHT: Cronómetro, objetivos y stats
        right = ttk.Frame(self, padding=6)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        # Cronómetro
        box_timer = ttk.LabelFrame(right, text="Sesión & Tiempo efectivo", padding=8)
        box_timer.pack(fill=tk.X, pady=(0,8))
        self.timer_label = ttk.Label(box_timer, text="00:00:00", font=("SF Pro", 16, "bold"))
        self.timer_label.grid(row=0, column=0, padx=4)
        ttk.Button(box_timer, text="Iniciar", command=self.start_session).grid(row=0, column=1, padx=2)
        ttk.Button(box_timer, text="Pausar", command=self.pause_session).grid(row=0, column=2, padx=2)
        ttk.Button(box_timer, text="Finalizar", command=self.end_session).grid(row=0, column=3, padx=2)
        self.effective_today_var = tk.StringVar(value="Hoy: 0 min")
        ttk.Label(box_timer, textvariable=self.effective_today_var).grid(row=1, column=0, columnspan=4, sticky="w", pady=(6,0))

        # Objetivos
        box_goal = ttk.LabelFrame(right, text="Objetivo diario", padding=8)
        box_goal.pack(fill=tk.X, pady=(0,8))

        ttk.Label(box_goal, text="PnL objetivo (USD)").grid(row=0, column=0, sticky="w")
        ttk.Entry(box_goal, textvariable=self.daily_target_pnl, width=8).grid(row=0, column=1, padx=4)
        ttk.Label(box_goal, text="Min. efectivos").grid(row=0, column=2, sticky="w")
        ttk.Entry(box_goal, textvariable=self.daily_target_minutes, width=6).grid(row=0, column=3, padx=4)

        # Barras de progreso
        ttk.Label(box_goal, text="Progreso PnL").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.pbar_pnl = ttk.Progressbar(box_goal, orient="horizontal", mode="determinate", length=220, maximum=100)
        self.pbar_pnl.grid(row=1, column=1, columnspan=3, sticky="we", padx=4, pady=(6,0))
        self.pbar_pnl_lbl = ttk.Label(box_goal, text="0%  (restante: 0.00)")
        self.pbar_pnl_lbl.grid(row=2, column=1, columnspan=3, sticky="w")

        ttk.Label(box_goal, text="Progreso Tiempo").grid(row=3, column=0, sticky="w", pady=(6,0))
        self.pbar_time = ttk.Progressbar(box_goal, orient="horizontal", mode="determinate", length=220, maximum=100)
        self.pbar_time.grid(row=3, column=1, columnspan=3, sticky="we", padx=4, pady=(6,0))
        self.pbar_time_lbl = ttk.Label(box_goal, text="0%  (restante: 0 min)")
        self.pbar_time_lbl.grid(row=4, column=1, columnspan=3, sticky="w")

        # Stats
        box_stats = ttk.LabelFrame(right, text="Estadísticas", padding=8)
        box_stats.pack(fill=tk.X)
        self.daily_ops_var = tk.StringVar()
        self.daily_wr_var = tk.StringVar()
        self.cum_ops_var = tk.StringVar()
        self.cum_wr_var = tk.StringVar()
        self.daily_pnl_var = tk.StringVar()
        self.cum_pnl_var = tk.StringVar()
        ttk.Label(box_stats, textvariable=self.daily_ops_var).pack(anchor="w")
        ttk.Label(box_stats, textvariable=self.daily_wr_var).pack(anchor="w")
        ttk.Label(box_stats, textvariable=self.daily_pnl_var).pack(anchor="w")
        ttk.Separator(box_stats, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(box_stats, textvariable=self.cum_ops_var).pack(anchor="w")
        ttk.Label(box_stats, textvariable=self.cum_wr_var).pack(anchor="w")
        ttk.Label(box_stats, textvariable=self.cum_pnl_var).pack(anchor="w")

        # CENTER: Tabla + Gráfico
        center = ttk.PanedWindow(self, orient=tk.VERTICAL)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Tabla
        table_frame = ttk.Frame(center)
        self.tree = ttk.Treeview(table_frame, columns=COLUMNS, show="headings", height=14)
        for c in COLUMNS:
            self.tree.heading(c, text=c)
            w = 90
            if c == "datetime": w = 160
            if c == "notes": w = 260
            if c in ("pnl","payout_pct","amount"): w = 70
            if c in ("emotion","asset","timeframe","direction","outcome"): w = 80
            self.tree.column(c, width=w, anchor="center")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=vsb.set)
        center.add(table_frame)

        # Gráfico
        chart_frame = ttk.LabelFrame(center, text="Hoy: Operaciones por hora y PnL acumulado", padding=6)
        self.figure = Figure(figsize=(7, 2.6), dpi=100)
        self.ax1 = self.figure.add_subplot(111)  # Se reutiliza con doble eje si quieres
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        center.add(chart_frame)

        # Status
        self.status = ttk.Label(self, text="Listo.", padding=4, anchor="w")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Estado cronómetro
        self.timer_running = False
        self.timer_start = None
        self.elapsed_today = self._load_elapsed_today()

    # ---------- Cronómetro / Sesiones ----------
    def _tick_timer(self):
        if self.timer_running and self.timer_start is not None:
            total = self.elapsed_today + int((datetime.now() - self.timer_start).total_seconds())
        else:
            total = self.elapsed_today
        self.timer_label.configure(text=self._format_hhmmss(total))
        self._update_goal_bars()   # refresca progreso tiempo
        self.after(1000, self._tick_timer)

    def start_session(self):
        if self.timer_running: return
        self.timer_running = True
        self.timer_start = datetime.now()
        self.status.config(text="Sesión iniciada.")

    def pause_session(self):
        if not self.timer_running or self.timer_start is None: return
        elapsed = int((datetime.now() - self.timer_start).total_seconds())
        self.elapsed_today += max(elapsed, 0)
        self.timer_running = False
        self.timer_start = None
        self._save_today_elapsed(); self._update_effective_today_label()
        self.status.config(text="Sesión pausada.")
        self._update_goal_bars()

    def end_session(self):
        start = None; end = None
        if self.timer_running and self.timer_start is not None:
            start = self.timer_start; end = datetime.now()
            elapsed = int((end - start).total_seconds())
            self.elapsed_today += max(elapsed, 0)
            self.timer_running = False; self.timer_start = None
        self._save_today_elapsed(); self._update_effective_today_label()
        if start and end:
            ensure_headers(SESSIONS_CSV, ["session_id","start","end","duration_min","notes"])
            sid = f"{start.strftime('%Y%m%d')}-{int(start.timestamp())}"
            with SESSIONS_CSV.open("a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([sid, start.strftime("%Y-%m-%d %H:%M:%S"),
                                        end.strftime("%Y-%m-%d %H:%M:%S"),
                                        round((end-start).total_seconds()/60, 2), ""])
        self.status.config(text="Sesión finalizada.")
        self._recalc_stats()
        self._update_goal_bars()

    def _format_hhmmss(self, total_seconds:int)->str:
        hrs = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

    def _elapsed_store_path(self):
        return Path(f".elapsed_{datetime.now().date().isoformat()}.txt")

    def _load_elapsed_today(self) -> int:
        p = self._elapsed_store_path()
        if p.exists():
            try: return int(p.read_text().strip())
            except: return 0
        return 0

    def _save_today_elapsed(self):
        self._elapsed_store_path().write_text(str(self.elapsed_today))
        self._update_effective_today_label()

    def _update_effective_today_label(self):
        mins = round(self.elapsed_today/60, 1)
        self.effective_today_var.set(f"Hoy: {mins} min efectivos")

    # ---------- Datos ----------
    def _load_trades(self):
        self.tree.delete(*self.tree.get_children())
        with TRADES_CSV.open("r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                self.tree.insert("", tk.END, values=[row.get(c,"") for c in COLUMNS])
        self.status.config(text="Datos cargados.")
        self._update_effective_today_label()

    def add_trade(self):
        try:
            amount = parse_float(self.amount_var.get(), 0)
            payout_pct = parse_float(self.payout_var.get(), 0)
        except:
            messagebox.showerror("Error", "Monto/Payout inválidos."); return

        dt = datetime.now()
        date_str = dt.date().isoformat()
        outcome = self.out_cb.get()
        pnl = 0.0
        if outcome == "win":   pnl = round(amount * (payout_pct/100.0), 2)
        elif outcome == "loss": pnl = -round(amount, 2)

        row = {
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "date": date_str,
            "asset": self.asset_cb.get(),
            "timeframe": self.tf_cb.get(),
            "amount": f"{amount:.2f}",
            "direction": self.dir_cb.get(),
            "outcome": outcome,
            "payout_pct": f"{payout_pct:.2f}",
            "pnl": f"{pnl:.2f}",
            "emotion": self.emotion_cb.get(),
            "notes": self.notes_var.get().strip(),
        }
        ensure_headers(TRADES_CSV, COLUMNS)
        with TRADES_CSV.open("a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=COLUMNS).writerow(row)

        self.tree.insert("", tk.END, values=[row[c] for c in COLUMNS])
        self.status.config(text="Operación agregada.")
        self._recalc_stats()
        self._update_goal_bars()
        self._refresh_chart()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel: return
        target_rows = [self.tree.item(i)["values"] for i in sel]
        for i in sel: self.tree.delete(i)

        keep = []
        with TRADES_CSV.open("r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                v = [row.get(c,"") for c in COLUMNS]
                if v not in target_rows: keep.append(row)
        with TRADES_CSV.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS); w.writeheader(); w.writerows(keep)

        self.status.config(text="Operación eliminada.")
        self._recalc_stats()
        self._update_goal_bars()
        self._refresh_chart()

    def load_csv(self):
        path = filedialog.askopenfilename(title="Selecciona un CSV", filetypes=[("CSV","*.csv")])
        if not path: return
        data = Path(path).read_text(encoding="utf-8")
        TRADES_CSV.write_text(data, encoding="utf-8")
        self._load_trades()
        self._recalc_stats()
        self._update_goal_bars()
        self._refresh_chart()

    def export_md(self):
        out = Path("report.md")
        out.write_text(self._make_md_report(), encoding="utf-8")
        self.status.config(text=f"Reporte generado: {out}")

    # ---------- Métricas ----------
    def _read_trades(self):
        rows = []
        with TRADES_CSV.open("r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                try: row["_dt"] = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
                except: continue
                rows.append(row)
        return rows

    def _recalc_stats(self):
        rows = self._read_trades()
        today = datetime.now().date().isoformat()

        daily = [r for r in rows if r["date"] == today]
        w_d = sum(1 for r in daily if r["outcome"] == "win")
        l_d = sum(1 for r in daily if r["outcome"] == "loss")
        t_d = sum(1 for r in daily if r["outcome"] not in ("win","loss"))
        pnl_d = sum(parse_float(r["pnl"], 0) for r in daily)
        wr_d = (w_d/(w_d+l_d)*100) if (w_d+l_d)>0 else 0.0

        w_a = sum(1 for r in rows if r["outcome"] == "win")
        l_a = sum(1 for r in rows if r["outcome"] == "loss")
        t_a = sum(1 for r in rows if r["outcome"] not in ("win","loss"))
        pnl_a = sum(parse_float(r["pnl"], 0) for r in rows)
        wr_a = (w_a/(w_a+l_a)*100) if (w_a+l_a)>0 else 0.0

        self.daily_ops_var.set(f"Hoy: Ops {len(daily)}  |  W {w_d}  L {l_d}  T {t_d}")
        self.daily_wr_var.set(f"WinRate diario: {wr_d:.1f}%")
        self.daily_pnl_var.set(f"PnL diario: {pnl_d:+.2f} USD")
        self.cum_ops_var.set(f"Acumulado: Ops {len(rows)}  |  W {w_a}  L {l_a}  T {t_a}")
        self.cum_wr_var.set(f"WinRate acumulado: {wr_a:.1f}%")
        self.cum_pnl_var.set(f"PnL acumulado: {pnl_a:+.2f} USD")

        # guarda para progreso PnL
        self._last_pnl_daily = pnl_d

    def _update_goal_bars(self):
        # PnL
        target_pnl = max(0.01, self.daily_target_pnl.get())
        pnl = getattr(self, "_last_pnl_daily", 0.0)
        pct_pnl = max(0, min(100, (pnl/target_pnl)*100))
        self.pbar_pnl["value"] = pct_pnl
        restante = max(0.0, target_pnl - pnl)
        self.pbar_pnl_lbl.config(text=f"{pct_pnl:.0f}%  (restante: {restante:+.2f} USD)")

        # Tiempo
        tgt_min = max(1, self.daily_target_minutes.get())
        mins = self.elapsed_today/60
        pct_t = max(0, min(100, (mins/tgt_min)*100))
        self.pbar_time["value"] = pct_t
        restante_t = max(0, tgt_min - mins)
        self.pbar_time_lbl.config(text=f"{pct_t:.0f}%  (restante: {restante_t:.1f} min)")

    # ---------- Gráfico ----------
    def _refresh_chart(self):
        rows = [r for r in self._read_trades() if r["date"] == datetime.now().date().isoformat()]
        # bucket por hora (local)
        ops_per_hour = defaultdict(int)
        pnl_per_hour = defaultdict(float)
        for r in rows:
            hour = r["_dt"].strftime("%H:00")
            ops_per_hour[hour] += 1
            pnl_per_hour[hour] += parse_float(r["pnl"], 0)

        # orden cronológico
        hours_sorted = sorted(set(list(ops_per_hour.keys()) + list(pnl_per_hour.keys())))
        if not hours_sorted:
            self.ax1.clear()
            self.ax1.set_title("Sin datos de hoy")
            self.ax1.set_xlabel("Hora")
            self.ax1.set_ylabel("Ops")
            self.canvas.draw()
            return

        ops = [ops_per_hour[h] for h in hours_sorted]
        pnl_cum = []
        acc = 0.0
        for h in hours_sorted:
            acc += pnl_per_hour[h]
            pnl_cum.append(acc)

        self.ax1.clear()
        # barras de operaciones
        self.ax1.bar(hours_sorted, ops)
        self.ax1.set_ylabel("Operaciones")
        self.ax1.set_xlabel("Hora")

        # línea de PnL acumulado (segundo eje)
        ax2 = self.ax1.twinx()
        ax2.plot(hours_sorted, pnl_cum, marker="o")
        ax2.set_ylabel("PnL acumulado (USD)")

        self.ax1.set_title("Operaciones por hora (barras) y PnL acumulado (línea)")
        self.figure.tight_layout()
        self.canvas.draw()

    # ---------- Reporte MD ----------
    def _make_md_report(self) -> str:
        rows = self._read_trades()
        rows.sort(key=lambda r: r["_dt"])
        today = datetime.now().date().isoformat()

        w_a = sum(1 for r in rows if r["outcome"] == "win")
        l_a = sum(1 for r in rows if r["outcome"] == "loss")
        pnl_a = sum(parse_float(r["pnl"]) for r in rows)
        wr_a = (w_a/(w_a+l_a)*100) if (w_a+l_a)>0 else 0.0

        daily = [r for r in rows if r["date"] == today]
        w_d = sum(1 for r in daily if r["outcome"] == "win")
        l_d = sum(1 for r in daily if r["outcome"] == "loss")
        pnl_d = sum(parse_float(r["pnl"]) for r in daily)
        wr_d = (w_d/(w_d+l_d)*100) if (w_d+l_d)>0 else 0.0

        lines = []
        lines.append("# Reporte de Trading\n\n")
        lines.append(f"**WinRate acumulado:** {wr_a:.1f}%  |  **PnL acumulado:** {pnl_a:+.2f} USD\n\n")
        lines.append(f"**WinRate diario:** {wr_d:.1f}%  |  **PnL diario:** {pnl_d:+.2f} USD\n\n")
        lines.append("## Operaciones\n")
        lines.append("| datetime | asset | tf | amount | dir | outcome | payout% | pnl | emotion | notes |\n")
        lines.append("|---|---|---:|---:|:--:|:--:|---:|---:|:--:|---|\n")
        for r in rows:
            lines.append(f"| {r['datetime']} | {r['asset']} | {r['timeframe']} | {r['amount']} | "
                         f"{r['direction']} | {r['outcome']} | {r['payout_pct']} | {r['pnl']} | "
                         f"{r['emotion']} | {r['notes']} |\n")
        return "".join(lines)

# main
if __name__ == "__main__":
    app = TradingApp()
    app.mainloop()
