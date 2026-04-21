#!/usr/bin/env python3
"""
5G NR Peak Data Rate (PDR) Calculator
Based on 3GPP TS 38.306 Equation (1)

PDR = 10^-6 * sum_j [ v_Layers(j) * Q_m(j) * f(j) * R_max
                       * (N_PRB(j,mu) * 12 / Ts_mu)
                       * (1 - OH(j)) ]
      × TDD_DL_ratio

Run: python3 pdr_calculator.py
Requires: Python 3.8+ with tkinter (included in most Python distributions)
"""

import tkinter as tk
from tkinter import ttk
import math

# ─────────────────────────────────────── constants
R_MAX = 948 / 1024   # 3GPP TS 38.306 §4.1.2, fixed maximum code rate

# Colours — dark technical theme
C = {
    "bg":       "#0e1117",
    "bg2":      "#161b27",
    "bg3":      "#1c2235",
    "bg4":      "#222840",
    "accent":   "#f5a623",
    "accent2":  "#4fc3f7",
    "accent3":  "#69f0ae",
    "fg":       "#e2e6f0",
    "fg2":      "#8890a6",
    "fg3":      "#555e78",
    "danger":   "#ef5350",
    "border":   "#2c3452",
    "border2":  "#3a4466",
}

FONTS = {
    "mono":    ("Consolas", 10),
    "mono_b":  ("Consolas", 10, "bold"),
    "mono_sm": ("Consolas",  9),
    "mono_lg": ("Consolas", 13, "bold"),
    "mono_xl": ("Consolas", 26, "bold"),
    "mono_hd": ("Consolas", 11, "bold"),
}

MOD_LABELS = ["QPSK  (Qm=2)", "16-QAM  (Qm=4)", "64-QAM  (Qm=6)", "256-QAM  (Qm=8)"]
MOD_VALUES = {"QPSK  (Qm=2)": 2, "16-QAM  (Qm=4)": 4,
              "64-QAM  (Qm=6)": 6, "256-QAM  (Qm=8)": 8}

MU_LABELS  = ["μ=0   15 kHz", "μ=1   30 kHz", "μ=2   60 kHz", "μ=3  120 kHz"]
MU_VALUES  = {"μ=0   15 kHz": 0, "μ=1   30 kHz": 1,
              "μ=2   60 kHz": 2, "μ=3  120 kHz": 3}

OH_PRESETS = {
    "DL FR1 14%": 14.0,
    "DL FR2 18%": 18.0,
    "UL FR1  8%":  8.0,
    "UL FR2 10%": 10.0,
    "Custom":      0.0,
}

# ─────────────────────────────────────── physics
def Ts_mu(mu: int) -> float:
    """Average OFDM symbol duration in seconds (3GPP TS 38.306 §4.1.2)."""
    return 1e-3 / (14 * (2 ** mu))


def tdd_dl_ratio(pattern: str, s_dl_syms: int) -> tuple[float, dict]:
    """
    Compute DL ratio from a TDD pattern string.

    D = full DL slot  (14/14 DL symbols)
    U = full UL slot  ( 0/14 DL symbols)
    S = special slot  (s_dl_syms/14 DL symbols)

    Returns (ratio, stats_dict).
    """
    pat = pattern.strip().upper()
    if not pat:
        return 1.0, {"D": 0, "S": 0, "U": 0, "total": 0, "dl_eq": 0.0}
    n_d = pat.count('D')
    n_s = pat.count('S')
    n_u = pat.count('U')
    total = len(pat)
    dl_eq = n_d + n_s * (s_dl_syms / 14.0)
    ratio = dl_eq / total if total > 0 else 0.0
    stats = {"D": n_d, "S": n_s, "U": n_u, "total": total, "dl_eq": dl_eq}
    return ratio, stats


def compute_pdr(layers_data: list[dict], ratio: float) -> tuple[float, list[float]]:
    """
    Compute PDR in Mbps.

    Returns (total_pdr, [per_layer_pdr]).
    """
    per_layer = []
    for L in layers_data:
        ts = Ts_mu(L["mu"])
        bits_per_sec = (
            L["v"] * L["qm"] * L["f"] * R_MAX
            * (L["nprb"] * 12 / ts)
            * (1 - L["oh"])
        )
        per_layer.append(1e-6 * bits_per_sec * ratio)
    return sum(per_layer), per_layer


# ─────────────────────────────────────── helpers
def _entry(parent, var, width=10, **kw):
    return tk.Entry(
        parent, textvariable=var, width=width,
        bg=C["bg2"], fg=C["fg"], insertbackground=C["accent2"],
        relief="flat", highlightbackground=C["border"],
        highlightthickness=1, font=FONTS["mono"], **kw
    )


def _spinbox(parent, var, lo, hi, inc=1, fmt="%.0f", width=8, cmd=None, **kw):
    sb = tk.Spinbox(
        parent, from_=lo, to=hi, increment=inc, textvariable=var,
        format=fmt, width=width,
        bg=C["bg2"], fg=C["fg"], insertbackground=C["fg"],
        buttonbackground=C["bg3"], relief="flat",
        highlightbackground=C["border"], highlightthickness=1,
        font=FONTS["mono"], command=cmd, **kw
    )
    if cmd:
        sb.bind("<KeyRelease>", lambda _: cmd())
    return sb


def _label(parent, text, color=None, font=None, **kw):
    return tk.Label(
        parent, text=text,
        bg=kw.pop("bg", C["bg"]),
        fg=color or C["fg2"],
        font=font or FONTS["mono"],
        **kw
    )


def _combo(parent, var, values, width=14, cmd=None):
    style = ttk.Style()
    style.configure(
        "Dark.TCombobox",
        fieldbackground=C["bg2"],
        background=C["bg3"],
        foreground=C["fg"],
        selectbackground=C["bg4"],
        selectforeground=C["accent2"],
        arrowcolor=C["accent"],
    )
    cb = ttk.Combobox(
        parent, textvariable=var, values=values,
        state="readonly", width=width,
        font=FONTS["mono"], style="Dark.TCombobox"
    )
    if cmd:
        cb.bind("<<ComboboxSelected>>", lambda _: cmd())
    return cb


def _sep(parent):
    f = tk.Frame(parent, bg=C["border"], height=1)
    f.pack(fill="x", padx=0, pady=4)


def _section_header(parent, text):
    row = tk.Frame(parent, bg=C["bg"])
    row.pack(fill="x", pady=(10, 2))
    tk.Label(row, text="▸ " + text, bg=C["bg"],
             fg=C["accent"], font=FONTS["mono_hd"]).pack(side="left")
    tk.Frame(row, bg=C["border"], height=1).pack(
        side="left", fill="x", expand=True, padx=(8, 0), pady=5)
    return row


# ─────────────────────────────────────── layer card
_layer_counter = 0


class LayerCard(tk.Frame):
    def __init__(self, parent, on_remove, on_change):
        global _layer_counter
        _layer_counter += 1
        self._num = _layer_counter
        super().__init__(parent,
                         bg=C["bg3"],
                         highlightbackground=C["border2"],
                         highlightthickness=1)
        self._on_remove = on_remove
        self._on_change = on_change
        self._vars: dict = {}
        self._build()

    def _lbl(self, parent, text):
        return tk.Label(parent, text=text, bg=C["bg3"],
                        fg=C["fg2"], font=FONTS["mono"], anchor="w")

    def _build(self):
        # ── card header
        hdr = tk.Frame(self, bg=C["bg2"], padx=10, pady=5)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"  Component Carrier / Layer {self._num}",
                 bg=C["bg2"], fg=C["accent"], font=FONTS["mono_b"]).pack(side="left")
        tk.Button(hdr, text=" ✕ remove ", bg=C["bg2"], fg=C["danger"],
                  font=FONTS["mono_sm"], relief="flat", bd=0,
                  cursor="hand2", activebackground=C["bg2"],
                  activeforeground=C["danger"],
                  command=lambda: self._on_remove(self)).pack(side="right")

        # ── body grid
        body = tk.Frame(self, bg=C["bg3"], padx=12, pady=10)
        body.pack(fill="x")
        body.columnconfigure(1, weight=1)
        body.columnconfigure(3, weight=1)

        def row(r, lbl1, w1, lbl2=None, w2=None):
            self._lbl(body, lbl1).grid(row=r, column=0, sticky="w",
                                        padx=(0, 6), pady=3)
            w1.grid(row=r, column=1, sticky="ew", pady=3)
            if lbl2 is not None:
                self._lbl(body, "  " + lbl2).grid(row=r, column=2,
                                                    sticky="w", padx=(12, 6), pady=3)
                w2.grid(row=r, column=3, sticky="ew", pady=3)

        # v_Layers
        v_var = tk.IntVar(value=1)
        self._vars["v"] = v_var
        row(0, "v_Layers  (MIMO spatial layers 1–8)",
            _spinbox(body, v_var, 1, 8, cmd=self._on_change))

        # Modulation + f
        qm_var = tk.StringVar(value="256-QAM  (Qm=8)")
        f_var  = tk.DoubleVar(value=1.0)
        self._vars["qm_str"] = qm_var
        self._vars["f"]      = f_var
        row(1, "Modulation  Q_m",
            _combo(body, qm_var, MOD_LABELS, cmd=self._on_change),
            "f  scaling factor  {1, 0.8, 0.75, 0.4}",
            _combo(body, f_var, [1.0, 0.8, 0.75, 0.4], width=8,
                   cmd=self._on_change))

        # N_PRB + μ
        nprb_var = tk.IntVar(value=217)
        mu_var   = tk.StringVar(value="μ=1   30 kHz")
        self._vars["nprb"]   = nprb_var
        self._vars["mu_str"] = mu_var
        row(2, "N_PRB  (allocated bandwidth PRBs)",
            _spinbox(body, nprb_var, 1, 275, cmd=self._on_change),
            "SCS  μ  (subcarrier spacing numerology)",
            _combo(body, mu_var, MU_LABELS, cmd=self._on_change))

        # OH preset + value
        oh_preset_var = tk.StringVar(value="DL FR1 14%")
        oh_val_var    = tk.DoubleVar(value=14.0)
        self._vars["oh_preset"] = oh_preset_var
        self._vars["oh"]        = oh_val_var

        def _oh_preset_changed(*_):
            preset = oh_preset_var.get()
            if preset != "Custom":
                oh_val_var.set(OH_PRESETS[preset])
            self._on_change()

        oh_preset_var.trace_add("write", _oh_preset_changed)
        oh_val_var.trace_add("write", lambda *_: self._on_change())

        row(3, "OH  overhead  (%) — preset",
            _combo(body, oh_preset_var, list(OH_PRESETS), cmd=_oh_preset_changed),
            "OH value  (%)",
            _spinbox(body, oh_val_var, 0, 50, inc=0.5, fmt="%.1f",
                     cmd=self._on_change))

        # live per-layer PDR
        self._pdr_lbl = tk.Label(body, text="",
                                  bg=C["bg3"], fg=C["accent3"],
                                  font=FONTS["mono_b"], anchor="e")
        self._pdr_lbl.grid(row=4, column=0, columnspan=4,
                            sticky="e", pady=(6, 0))

        # traces for combo vars
        for var in [qm_var, mu_var]:
            var.trace_add("write", lambda *_: self._on_change())
        for var in [v_var, nprb_var]:
            var.trace_add("write", lambda *_: self._on_change())

    def set_pdr_label(self, pdr_val: float, ratio: float):
        ts = Ts_mu(MU_VALUES.get(self._vars["mu_str"].get(), 1))
        pdr_full = pdr_val / ratio if ratio > 0 else 0
        self._pdr_lbl.config(
            text=(f"Layer PDR (full BW): {pdr_full:.2f} Mbps  "
                  f"→  ×TDD: {pdr_val:.2f} Mbps")
        )

    def get(self) -> dict | None:
        try:
            qm_key = self._vars["qm_str"].get()
            mu_key = self._vars["mu_str"].get()
            # handle combo f (may be string)
            f_raw = self._vars["f"].get()
            return {
                "v":    int(self._vars["v"].get()),
                "qm":   MOD_VALUES.get(qm_key, 8),
                "f":    float(f_raw),
                "nprb": int(self._vars["nprb"].get()),
                "mu":   MU_VALUES.get(mu_key, 1),
                "oh":   float(self._vars["oh"].get()) / 100.0,
            }
        except (tk.TclError, ValueError, KeyError):
            return None


# ─────────────────────────────────────── main application
class PDRCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("5G NR  Peak Data Rate Calculator  —  3GPP TS 38.306 Eq.(1)")
        self.configure(bg=C["bg"])
        self.minsize(900, 640)
        self.resizable(True, True)
        self._cards: list[LayerCard] = []
        self._setup_ttk()
        self._build_ui()
        self._add_layer()    # one layer by default
        self._refresh()

    # ── ttk dark theme
    def _setup_ttk(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".",
                         background=C["bg"],
                         foreground=C["fg"],
                         troughcolor=C["bg2"],
                         bordercolor=C["border"],
                         focuscolor=C["accent2"],
                         font=FONTS["mono"])
        style.configure("TScrollbar",
                         background=C["bg3"],
                         troughcolor=C["bg2"],
                         arrowcolor=C["fg2"],
                         borderwidth=0)
        style.configure("Vertical.TScrollbar", width=10)
        style.configure("TSeparator", background=C["border"])
        style.configure("Dark.TCombobox",
                         fieldbackground=C["bg2"],
                         background=C["bg3"],
                         foreground=C["fg"],
                         arrowcolor=C["accent"],
                         selectbackground=C["bg4"],
                         selectforeground=C["accent2"],
                         bordercolor=C["border"])
        style.map("Dark.TCombobox",
                  fieldbackground=[("readonly", C["bg2"])],
                  selectbackground=[("readonly", C["bg4"])],
                  selectforeground=[("readonly", C["accent2"])])

    # ── UI skeleton
    def _build_ui(self):
        # ── topbar
        topbar = tk.Frame(self, bg="#090c14", padx=16, pady=8)
        topbar.pack(fill="x", side="top")
        tk.Label(topbar, text="5G NR  PDR Calculator",
                 bg="#090c14", fg=C["accent"],
                 font=FONTS["mono_hd"]).pack(side="left")
        tk.Label(topbar,
                 text=" │  3GPP TS 38.306 Eq.(1)  │  R_max = 948/1024",
                 bg="#090c14", fg=C["fg3"],
                 font=FONTS["mono_sm"]).pack(side="left")

        # ── formula bar
        fbar = tk.Frame(self, bg=C["bg2"],
                        highlightbackground=C["border"], highlightthickness=1,
                        padx=16, pady=8)
        fbar.pack(fill="x", padx=10, pady=(6, 0))
        tk.Label(fbar,
                 text=("PDR = 10⁻⁶ × Σⱼ [ v_Layers(j) · Q_m(j) · f(j) · R_max"
                       "  ·  (N_PRB(j,μ)·12 / Tₛᵘ)  ·  (1 − OH(j)) ]"
                       "  ×  TDD_DL_ratio"),
                 bg=C["bg2"], fg=C["accent2"],
                 font=FONTS["mono"]).pack(anchor="w")
        tk.Label(fbar,
                 text=("R_max = 948/1024 = 0.9258     "
                       "Tₛᵘ = 10⁻³ / (14 × 2ᵘ)  seconds     "
                       "TDD_DL_ratio = (D + S·sym_DL/14) / total_slots"),
                 bg=C["bg2"], fg=C["fg3"],
                 font=FONTS["mono_sm"]).pack(anchor="w", pady=(2, 0))

        # ── main body: left pane + right results
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=10, pady=6)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=1, minsize=260)
        body.rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=C["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        right = tk.Frame(body, bg=C["bg"])
        right.grid(row=0, column=1, sticky="nsew")

        self._build_tdd(left)
        self._build_layers_panel(left)
        self._build_results(right)

    # ── TDD section
    def _build_tdd(self, parent):
        _section_header(parent, "TDD Slot Configuration")

        tdd_card = tk.Frame(parent, bg=C["bg2"],
                            highlightbackground=C["border"],
                            highlightthickness=1, padx=14, pady=10)
        tdd_card.pack(fill="x", pady=(0, 6))
        tdd_card.columnconfigure(1, weight=1)
        tdd_card.columnconfigure(3, weight=1)

        def lbl(text, row, col, **kw):
            tk.Label(tdd_card, text=text, bg=C["bg2"],
                     fg=kw.pop("fg", C["fg2"]), font=FONTS["mono"],
                     anchor="w", **kw).grid(
                row=row, column=col, sticky="w", padx=(0, 6), pady=3)

        # Pattern entry
        lbl("Slot pattern  (D / U / S):", 0, 0)
        self._tdd_pat_var = tk.StringVar(value="DDDSUUDDDSUU")
        pat_entry = tk.Entry(
            tdd_card, textvariable=self._tdd_pat_var, width=30,
            bg=C["bg"], fg=C["accent2"], insertbackground=C["accent2"],
            relief="flat", highlightbackground=C["border2"],
            highlightthickness=1, font=("Consolas", 12))
        pat_entry.grid(row=0, column=1, columnspan=3, sticky="ew",
                       padx=(0, 0), pady=3)

        # S-slot DL symbols
        lbl("DL symbols in each S slot  (0–14):", 1, 0)
        self._s_dl_var = tk.IntVar(value=6)
        _spinbox(tdd_card, self._s_dl_var, 0, 14,
                 cmd=self._refresh).grid(row=1, column=1, sticky="w", pady=3)

        lbl("Examples: ms2.5 → DDSU  | ms5 → DDDSUUDDDSUU", 1, 2,
            fg=C["fg3"])

        # Live stats row
        self._tdd_stats_lbl = tk.Label(
            tdd_card, text="", bg=C["bg2"], fg=C["accent"],
            font=FONTS["mono_b"], anchor="w")
        self._tdd_stats_lbl.grid(row=2, column=0, columnspan=4,
                                  sticky="w", pady=(4, 0))

        # Traces
        self._tdd_pat_var.trace_add("write", lambda *_: self._refresh())
        self._s_dl_var.trace_add("write", lambda *_: self._refresh())

    # ── Layers panel
    def _build_layers_panel(self, parent):
        hdr_row = tk.Frame(parent, bg=C["bg"])
        hdr_row.pack(fill="x", pady=(8, 2))
        tk.Label(hdr_row, text="▸ Component Carriers / Layers  (J)",
                 bg=C["bg"], fg=C["accent"],
                 font=FONTS["mono_hd"]).pack(side="left")
        tk.Frame(hdr_row, bg=C["border"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 8), pady=5)
        tk.Button(hdr_row, text="  + Add Layer  ",
                  bg=C["bg3"], fg=C["accent2"],
                  font=FONTS["mono_b"], relief="flat", bd=0,
                  cursor="hand2", padx=6, pady=3,
                  activebackground=C["bg4"],
                  activeforeground=C["accent2"],
                  command=self._add_layer).pack(side="right")

        # Scrollable canvas
        wrap = tk.Frame(parent, bg=C["bg"])
        wrap.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(wrap, bg=C["bg"],
                                  highlightthickness=0, bd=0)
        vsb = ttk.Scrollbar(wrap, orient="vertical",
                             command=self._canvas.yview,
                             style="Vertical.TScrollbar")
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._layers_frame = tk.Frame(self._canvas, bg=C["bg"])
        self._layers_win_id = self._canvas.create_window(
            (0, 0), window=self._layers_frame, anchor="nw")

        def _on_canvas_resize(e):
            self._canvas.itemconfig(self._layers_win_id, width=e.width)

        def _on_frame_resize(e):
            self._canvas.configure(
                scrollregion=self._canvas.bbox("all"))

        self._canvas.bind("<Configure>", _on_canvas_resize)
        self._layers_frame.bind("<Configure>", _on_frame_resize)

        # Mouse-wheel scrolling
        def _wheel(e):
            self._canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units")
        self._canvas.bind_all("<MouseWheel>", _wheel)

    # ── Results panel
    def _build_results(self, parent):
        _section_header(parent, "Results")

        # Big PDR display
        big_card = tk.Frame(parent, bg=C["bg2"],
                            highlightbackground=C["accent"],
                            highlightthickness=1, padx=14, pady=14)
        big_card.pack(fill="x", pady=(0, 8))
        tk.Label(big_card, text="EFFECTIVE  PDR",
                 bg=C["bg2"], fg=C["fg2"],
                 font=FONTS["mono"]).pack()
        self._big_pdr_lbl = tk.Label(big_card, text="—",
                                      bg=C["bg2"], fg=C["accent"],
                                      font=FONTS["mono_xl"])
        self._big_pdr_lbl.pack()
        tk.Label(big_card, text="Mbps  (PHY layer, peak)",
                 bg=C["bg2"], fg=C["fg3"],
                 font=FONTS["mono_sm"]).pack()

        # Metrics grid
        metrics = tk.Frame(parent, bg=C["bg"])
        metrics.pack(fill="x", pady=(0, 8))
        metrics.columnconfigure((0, 1), weight=1)

        def metric_card(row, col, label):
            card = tk.Frame(metrics, bg=C["bg2"],
                            highlightbackground=C["border"],
                            highlightthickness=1, padx=10, pady=8)
            card.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
            tk.Label(card, text=label, bg=C["bg2"],
                     fg=C["fg2"], font=FONTS["mono_sm"],
                     anchor="w").pack(fill="x")
            var = tk.StringVar(value="—")
            tk.Label(card, textvariable=var, bg=C["bg2"],
                     fg=C["fg"], font=FONTS["mono_b"],
                     anchor="w").pack(fill="x")
            return var

        self._v_ratio    = metric_card(0, 0, "TDD DL ratio")
        self._v_pdr_full = metric_card(0, 1, "PDR  (no TDD,  Mbps)")
        self._v_pdr_eff  = metric_card(1, 0, "PDR × TDD  (Mbps)")
        self._v_slots    = metric_card(1, 1, "DL slots equivalent")

        # Breakdown
        _section_header(parent, "Per-Layer Breakdown")
        self._breakdown = tk.Frame(parent, bg=C["bg"])
        self._breakdown.pack(fill="x")

        # Slot pattern visualization
        _section_header(parent, "Slot Pattern")
        self._slot_vis_frame = tk.Frame(parent, bg=C["bg"])
        self._slot_vis_frame.pack(fill="x")

    # ── layer management
    def _add_layer(self):
        card = LayerCard(
            self._layers_frame,
            on_remove=self._remove_layer,
            on_change=self._refresh,
        )
        card.pack(fill="x", pady=4, padx=1)
        self._cards.append(card)
        self._refresh()

    def _remove_layer(self, card):
        if card in self._cards:
            self._cards.remove(card)
        self._refresh()

    # ── compute and refresh
    def _refresh(self, *_):
        pattern = self._tdd_pat_var.get()
        try:
            s_dl = int(self._s_dl_var.get())
        except (tk.TclError, ValueError):
            s_dl = 6

        ratio, stats = tdd_dl_ratio(pattern, s_dl)

        # Stats label
        n_d, n_s, n_u, tot = (stats["D"], stats["S"],
                               stats["U"], stats["total"])
        dl_eq = stats["dl_eq"]
        self._tdd_stats_lbl.config(
            text=(
                f"D={n_d}  S={n_s}(×{s_dl}sym)  U={n_u}  "
                f"total={tot} slots  │  DL_equiv={dl_eq:.2f} slots  "
                f"│  DL ratio = {ratio:.4f}  ({ratio*100:.1f}%)"
            )
        )

        # Collect layer data
        layers_data = [c.get() for c in self._cards if c.get() is not None]
        if not layers_data:
            self._big_pdr_lbl.config(text="—")
            for v in [self._v_ratio, self._v_pdr_full,
                      self._v_pdr_eff, self._v_slots]:
                v.set("—")
            return

        total_pdr, per_layer = compute_pdr(layers_data, ratio)
        total_pdr_full, _    = compute_pdr(layers_data, 1.0)

        self._big_pdr_lbl.config(text=f"{total_pdr:.1f}")
        self._v_ratio.set(f"{ratio:.4f}  ({ratio*100:.1f}%)")
        self._v_pdr_full.set(f"{total_pdr_full:.2f} Mbps")
        self._v_pdr_eff.set(f"{total_pdr:.2f} Mbps")
        self._v_slots.set(f"{dl_eq:.2f} / {tot}")

        # Per-layer labels
        for i, (card, pdr_val) in enumerate(zip(self._cards, per_layer)):
            card.set_pdr_label(pdr_val, ratio)

        # Breakdown
        for w in self._breakdown.winfo_children():
            w.destroy()
        for i, (L, pv) in enumerate(zip(layers_data, per_layer)):
            mu_label = [k for k, v in MU_VALUES.items() if v == L["mu"]][0]
            qm_label = [k for k, v in MOD_VALUES.items() if v == L["qm"]][0]
            row = tk.Frame(self._breakdown, bg=C["bg2"],
                           highlightbackground=C["border"],
                           highlightthickness=1, padx=10, pady=5)
            row.pack(fill="x", pady=2)
            tk.Label(row,
                     text=(f"L{i+1}  v={L['v']}  {qm_label.split()[0]}"
                           f"  f={L['f']}  N_PRB={L['nprb']}"
                           f"  {mu_label.strip()}  OH={L['oh']*100:.1f}%"),
                     bg=C["bg2"], fg=C["fg2"],
                     font=FONTS["mono_sm"], anchor="w").pack(
                side="left", fill="x", expand=True)
            tk.Label(row, text=f"{pv:.2f} Mbps",
                     bg=C["bg2"], fg=C["accent3"],
                     font=FONTS["mono_b"]).pack(side="right")

        # Slot visualizer
        self._draw_slot_vis(pattern, s_dl, ratio)

    def _draw_slot_vis(self, pattern: str, s_dl: int, ratio: float):
        for w in self._slot_vis_frame.winfo_children():
            w.destroy()

        pat = pattern.strip().upper()
        if not pat:
            return

        vis = tk.Canvas(self._slot_vis_frame, bg=C["bg2"],
                        height=36, highlightthickness=0)
        vis.pack(fill="x", pady=2)

        slot_colors = {
            "D": (C["accent2"],  C["bg"]),
            "U": (C["fg3"],      C["fg"]),
            "S": (C["accent"],   C["bg"]),
        }
        labels = {"D": "D", "U": "U", "S": "S"}

        def draw(event=None):
            vis.delete("all")
            w = vis.winfo_width()
            if w < 10:
                return
            n = len(pat)
            slot_w = max(4, (w - 4) / n)
            for i, ch in enumerate(pat):
                x0 = 2 + i * slot_w
                x1 = x0 + slot_w - 1
                fill, text_c = slot_colors.get(ch, (C["fg3"], C["fg"]))
                vis.create_rectangle(x0, 4, x1, 32, fill=fill,
                                      outline=C["bg"])
                if slot_w > 12:
                    vis.create_text((x0 + x1) / 2, 18,
                                    text=labels.get(ch, ch),
                                    fill=text_c,
                                    font=FONTS["mono_sm"])
            # legend
            vis.create_text(w - 4, 18, anchor="e",
                             text=f"DL ratio: {ratio*100:.1f}%",
                             fill=C["accent"], font=FONTS["mono_b"])

        vis.bind("<Configure>", draw)
        vis.after(10, draw)


# ─────────────────────────────────────── entry point
if __name__ == "__main__":
    app = PDRCalculatorApp()
    app.mainloop()