#!/usr/bin/env python3
"""
5G NR Peak Data Rate (PDR) Calculator
3GPP TS 38.306 Eq.(1)  ×  TDD DL ratio
MCS tables from 3GPP TS 38.214 V17.1.0 (2022-05)

Run: python3 pdr_calculator.py
Requires: Python 3.8+, tkinter (standard library)
"""
import tkinter as tk
from tkinter import ttk
import math

# ── palette
C = {
    "bg":      "#0e1117", "bg2": "#161b27", "bg3": "#1c2235",
    "bg4":     "#222840", "bg5": "#2a3356",
    "amber":   "#f5a623", "amber2": "#ffc35a",
    "cyan":    "#4fc3f7", "cyan2":  "#81d4fa",
    "green":   "#69f0ae", "green2": "#a5d6a7",
    "red":     "#ef5350", "purple": "#ce93d8",
    "orange":  "#ffb74d", "blue":   "#90caf9",
    "fg":      "#dde2f0", "fg2": "#7e8aaa", "fg3": "#4a5370",
    "border":  "#222c48", "border2": "#2d3a5c",
    "cQPSK":   "#4fc3f7", "c16": "#69f0ae", "c64": "#ffb74d",
    "c256":    "#ce93d8", "cBPSK": "#ef9a9a",
}
FONTS = {
    "mono":    ("Consolas", 10), "mono_b":  ("Consolas", 10, "bold"),
    "mono_sm": ("Consolas",  9), "mono_lg": ("Consolas", 13, "bold"),
    "mono_xl": ("Consolas", 24, "bold"),
    "mono_hd": ("Consolas", 11, "bold"),
}
MOD_COLORS = {
    "QPSK": C["cQPSK"], "16QAM": C["c16"], "64QAM": C["c64"],
    "256QAM": C["c256"], "π/2-BPSK": C["cBPSK"],
}

# ══════════════════════════════════════════════════════════════
#  3GPP TS 38.214 V17.1.0 MCS TABLES
#  Format per row: (mcs_index, modulation, Qm, CR×1024, spectral_efficiency)
# ══════════════════════════════════════════════════════════════
MCS_TABLES = {
    "T1 — Table 5.1.3.1-1 / 6.1.4.1-1  PDSCH/PUSCH  64QAM max": [
        (0,"QPSK",2,120,0.2344),(1,"QPSK",2,157,0.3066),(2,"QPSK",2,193,0.3770),
        (3,"QPSK",2,251,0.4902),(4,"QPSK",2,308,0.6016),(5,"QPSK",2,379,0.7402),
        (6,"QPSK",2,449,0.8770),(7,"QPSK",2,526,1.0273),(8,"QPSK",2,602,1.1758),
        (9,"QPSK",2,679,1.3262),(10,"16QAM",4,340,1.3281),(11,"16QAM",4,378,1.4766),
        (12,"16QAM",4,434,1.6953),(13,"16QAM",4,490,1.9141),(14,"16QAM",4,553,2.1602),
        (15,"16QAM",4,616,2.4063),(16,"16QAM",4,658,2.5703),(17,"64QAM",6,438,2.5664),
        (18,"64QAM",6,466,2.7305),(19,"64QAM",6,517,3.0293),(20,"64QAM",6,567,3.3223),
        (21,"64QAM",6,616,3.6094),(22,"64QAM",6,666,3.9023),(23,"64QAM",6,719,4.2129),
        (24,"64QAM",6,772,4.5234),(25,"64QAM",6,822,4.8164),(26,"64QAM",6,873,5.1152),
        (27,"64QAM",6,910,5.3320),(28,"64QAM",6,948,5.5547),
    ],
    "T2 — Table 5.1.3.1-2 / 6.1.4.1-2  PDSCH/PUSCH  256QAM max": [
        (0,"QPSK",2,120,0.2344),(1,"QPSK",2,193,0.3770),(2,"QPSK",2,308,0.6016),
        (3,"QPSK",2,449,0.8770),(4,"QPSK",2,602,1.1758),(5,"16QAM",4,378,1.4766),
        (6,"16QAM",4,434,1.6953),(7,"16QAM",4,490,1.9141),(8,"16QAM",4,553,2.1602),
        (9,"16QAM",4,616,2.4063),(10,"16QAM",4,658,2.5703),(11,"64QAM",6,466,2.7305),
        (12,"64QAM",6,517,3.0293),(13,"64QAM",6,567,3.3223),(14,"64QAM",6,616,3.6094),
        (15,"64QAM",6,666,3.9023),(16,"64QAM",6,719,4.2129),(17,"64QAM",6,772,4.5234),
        (18,"64QAM",6,822,4.8164),(19,"64QAM",6,873,5.1152),(20,"256QAM",8,682.5,5.3320),
        (21,"256QAM",8,711,5.5547),(22,"256QAM",8,754,5.8906),(23,"256QAM",8,797,6.2266),
        (24,"256QAM",8,841,6.5703),(25,"256QAM",8,885,6.9141),(26,"256QAM",8,916.5,7.1602),
        (27,"256QAM",8,948,7.4063),
    ],
    "T3 — Table 5.1.3.1-3  PDSCH  Low SE  64QAM max": [
        (0,"QPSK",2,30,0.0586),(1,"QPSK",2,40,0.0781),(2,"QPSK",2,50,0.0977),
        (3,"QPSK",2,64,0.1250),(4,"QPSK",2,78,0.1523),(5,"QPSK",2,99,0.1934),
        (6,"QPSK",2,120,0.2344),(7,"QPSK",2,157,0.3066),(8,"QPSK",2,193,0.3770),
        (9,"QPSK",2,251,0.4902),(10,"QPSK",2,308,0.6016),(11,"QPSK",2,379,0.7402),
        (12,"QPSK",2,449,0.8770),(13,"QPSK",2,526,1.0273),(14,"QPSK",2,602,1.1758),
        (15,"16QAM",4,340,1.3281),(16,"16QAM",4,378,1.4766),(17,"16QAM",4,434,1.6953),
        (18,"16QAM",4,490,1.9141),(19,"16QAM",4,553,2.1602),(20,"16QAM",4,616,2.4063),
        (21,"64QAM",6,438,2.5664),(22,"64QAM",6,466,2.7305),(23,"64QAM",6,517,3.0293),
        (24,"64QAM",6,567,3.3223),(25,"64QAM",6,616,3.6094),(26,"64QAM",6,666,3.9023),
        (27,"64QAM",6,719,4.2129),(28,"64QAM",6,772,4.5234),
    ],
    "T4 — Table 6.1.4.1-3  PUSCH  Transform Precoding  π/2-BPSK": [
        (0,"π/2-BPSK",1,60,0.0586),(1,"π/2-BPSK",1,80,0.0781),(2,"π/2-BPSK",1,100,0.0977),
        (3,"π/2-BPSK",1,128,0.1250),(4,"π/2-BPSK",1,156,0.1523),(5,"π/2-BPSK",1,198,0.1934),
        (6,"QPSK",2,120,0.2344),(7,"QPSK",2,157,0.3066),(8,"QPSK",2,193,0.3770),
        (9,"QPSK",2,251,0.4902),(10,"QPSK",2,308,0.6016),(11,"QPSK",2,379,0.7402),
        (12,"QPSK",2,449,0.8770),(13,"QPSK",2,526,1.0273),(14,"QPSK",2,602,1.1758),
        (15,"16QAM",4,340,1.3281),(16,"16QAM",4,378,1.4766),(17,"16QAM",4,434,1.6953),
        (18,"16QAM",4,490,1.9141),(19,"16QAM",4,553,2.1602),(20,"16QAM",4,616,2.4063),
        (21,"64QAM",6,438,2.5664),(22,"64QAM",6,466,2.7305),(23,"64QAM",6,517,3.0293),
        (24,"64QAM",6,567,3.3223),(25,"64QAM",6,616,3.6094),(26,"64QAM",6,666,3.9023),
        (27,"64QAM",6,719,4.2129),(28,"64QAM",6,772,4.5234),
    ],
}
TBL_KEYS = list(MCS_TABLES.keys())
R_MAX = 948 / 1024

# ── physics
def Ts(mu: int) -> float:
    return 1e-3 / (14 * (2 ** mu))

def tdd_ratio(pattern: str, s_dl: int):
    pat = pattern.strip().upper()
    if not pat:
        return 1.0, {"D":0,"S":0,"U":0,"total":0,"dlEq":0.0}
    nD = pat.count('D'); nS = pat.count('S'); nU = pat.count('U')
    total = len(pat); dlEq = nD + nS*(s_dl/14)
    return dlEq/total, {"D":nD,"S":nS,"U":nU,"total":total,"dlEq":dlEq}

def pdr_peak(v: dict, ratio: float) -> float:
    return 1e-6*v["v"]*v["qm"]*v["f"]*R_MAX*(v["nprb"]*12/Ts(v["mu"]))*(1-v["oh"])*ratio

def pdr_mcs(v: dict, ratio: float) -> float:
    return 1e-6*v["v"]*v["qm"]*v["f"]*(v["cr"]/1024)*(v["nprb"]*12/Ts(v["mu"]))*(1-v["oh"])*ratio

def bits_per_slot(v: dict) -> float:
    return v["nprb"]*12*14*(1-v["oh"])*v["qm"]*(v["cr"]/1024)

# ── helpers
def _lbl(parent, text, color=None, font=None, bg=None, anchor="w", **kw):
    return tk.Label(parent, text=text,
                    bg=bg or C["bg"], fg=color or C["fg2"],
                    font=font or FONTS["mono"], anchor=anchor, **kw)

def _spinbox(parent, var, lo, hi, inc=1, fmt="%.0f", width=8, cmd=None):
    sb = tk.Spinbox(parent, from_=lo, to=hi, increment=inc, textvariable=var,
                    format=fmt, width=width,
                    bg=C["bg2"], fg=C["fg"], insertbackground=C["fg"],
                    buttonbackground=C["bg3"], relief="flat",
                    highlightbackground=C["border"], highlightthickness=1,
                    font=FONTS["mono"], command=cmd)
    if cmd:
        sb.bind("<KeyRelease>", lambda _: cmd())
    return sb

def _combo(parent, var, values, width=22, cmd=None):
    cb = ttk.Combobox(parent, textvariable=var, values=values,
                      state="readonly", font=FONTS["mono"], width=width,
                      style="Dark.TCombobox")
    if cmd:
        cb.bind("<<ComboboxSelected>>", lambda _: cmd())
    return cb

def _section(parent, text, bg=None):
    bg = bg or C["bg"]
    row = tk.Frame(parent, bg=bg)
    row.pack(fill="x", pady=(8, 2))
    _lbl(row, "▸ "+text, color=C["amber"], font=FONTS["mono_hd"], bg=bg).pack(side="left")
    tk.Frame(row, bg=C["border"], height=1).pack(side="left", fill="x", expand=True, padx=(8,0), pady=5)


# ══════════════════════════════════════════════════════════════
#  LAYER CARD
# ══════════════════════════════════════════════════════════════
MU_LABELS  = ["μ=0  15 kHz","μ=1  30 kHz","μ=2  60 kHz","μ=3  120 kHz"]
MU_VALUES  = {l:i for i,l in enumerate(MU_LABELS)}
F_VALUES   = [1.0, 0.8, 0.75, 0.4]
OH_PRESETS = {"DL FR1 14%":14,"DL FR2 18%":18,"UL FR1 8%":8,"UL FR2 10%":10,"Custom":14}
_lc = 0

class LayerCard(tk.Frame):
    def __init__(self, parent, on_remove, on_change):
        global _lc
        _lc += 1
        self._num = _lc
        super().__init__(parent, bg=C["bg3"],
                         highlightbackground=C["border2"], highlightthickness=1)
        self._on_remove = on_remove
        self._on_change = on_change
        self._build()

    def _build(self):
        # header
        hdr = tk.Frame(self, bg=C["bg2"], padx=10, pady=5)
        hdr.pack(fill="x")
        _lbl(hdr, f"  Layer {self._num}", color=C["amber"],
             font=FONTS["mono_b"], bg=C["bg2"]).pack(side="left")
        self._pdr_lbl = _lbl(hdr, "", color=C["green"],
                              font=FONTS["mono_b"], bg=C["bg2"])
        self._pdr_lbl.pack(side="left", padx=8)
        tk.Button(hdr, text=" ✕ remove ", bg=C["bg2"], fg=C["red"],
                  font=FONTS["mono_sm"], relief="flat", bd=0, cursor="hand2",
                  activebackground=C["bg2"], activeforeground=C["red"],
                  command=lambda: self._on_remove(self)).pack(side="right")

        # MCS banner
        mcs_row = tk.Frame(self, bg=C["bg4"], padx=10, pady=7)
        mcs_row.pack(fill="x")

        _lbl(mcs_row, "38.214 Table:", bg=C["bg4"]).pack(side="left")
        self._tbl_var = tk.StringVar(value=TBL_KEYS[1])  # T2 256QAM default
        tbl_cb = _combo(mcs_row, self._tbl_var, TBL_KEYS, width=38,
                        cmd=self._on_table_change)
        tbl_cb.pack(side="left", padx=(4,14))

        _lbl(mcs_row, "MCS:", bg=C["bg4"]).pack(side="left")
        self._mcs_var = tk.StringVar()
        self._mcs_cb = _combo(mcs_row, self._mcs_var, [], width=36,
                              cmd=self._on_change)
        self._mcs_cb.pack(side="left", padx=(4,14))

        # MCS info labels
        self._mod_lbl = _lbl(mcs_row, "", color=C["cyan"], font=FONTS["mono_b"], bg=C["bg4"])
        self._mod_lbl.pack(side="left", padx=4)

        self._rebuild_mcs_options(select_idx=25)

        # body
        body = tk.Frame(self, bg=C["bg3"], padx=10, pady=8)
        body.pack(fill="x")
        body.columnconfigure((1,3), weight=1)

        def row(r, lbl1, w1, lbl2=None, w2=None):
            _lbl(body, lbl1, bg=C["bg3"]).grid(row=r, column=0, sticky="w", pady=2)
            w1.grid(row=r, column=1, sticky="ew", padx=(4,14), pady=2)
            if lbl2:
                _lbl(body, lbl2, bg=C["bg3"]).grid(row=r, column=2, sticky="w", pady=2)
                w2.grid(row=r, column=3, sticky="ew", padx=(4,0), pady=2)

        cb = self._on_change
        self._v_var    = tk.IntVar(value=1)
        self._f_var    = tk.StringVar(value="1.0")
        self._nprb_var = tk.IntVar(value=217)
        self._mu_var   = tk.StringVar(value=MU_LABELS[1])
        self._ohp_var  = tk.StringVar(value="DL FR1 14%")
        self._oh_var   = tk.DoubleVar(value=14.0)

        row(0, "v_Layers (MIMO layers)",
            _spinbox(body, self._v_var, 1, 8, cmd=cb),
            "f  scaling factor",
            _combo(body, self._f_var, [str(x) for x in F_VALUES], width=10, cmd=cb))
        row(1, "N_PRB  (allocated PRBs)",
            _spinbox(body, self._nprb_var, 1, 275, cmd=cb),
            "SCS  μ",
            _combo(body, self._mu_var, MU_LABELS, width=14, cmd=cb))
        row(2, "OH  overhead  preset",
            _combo(body, self._ohp_var, list(OH_PRESETS), width=14,
                   cmd=self._on_oh_preset),
            "OH value  (%)",
            _spinbox(body, self._oh_var, 0, 50, inc=0.5, fmt="%.1f", width=8, cmd=cb))

        # rate info bar
        rbar = tk.Frame(self, bg=C["bg4"], padx=10, pady=5)
        rbar.pack(fill="x")
        self._ri = {}
        for key, label, color in [
            ("bps","Bits/slot:",C["cyan2"]),
            ("bprb","Bits/PRB:",C["cyan2"]),
            ("se","SE:",C["purple"]),
            ("mcs","Rate@MCS:",C["green"]),
            ("pk","Peak:",C["amber"]),
        ]:
            fr = tk.Frame(rbar, bg=C["bg4"])
            fr.pack(side="left", padx=6)
            _lbl(fr, label, color=C["fg3"], bg=C["bg4"]).pack(side="left")
            lbl = _lbl(fr, "—", color=color, font=FONTS["mono_b"], bg=C["bg4"])
            lbl.pack(side="left", padx=(2,0))
            self._ri[key] = lbl

        # traces
        for var in [self._v_var, self._nprb_var, self._oh_var]:
            var.trace_add("write", lambda *_: self._on_change())
        for var in [self._f_var, self._mu_var, self._mcs_var]:
            var.trace_add("write", lambda *_: self._on_change())

    def _rebuild_mcs_options(self, select_idx=0):
        tbl = MCS_TABLES[self._tbl_var.get()]
        opts = [f"MCS {r[0]:2d}  {r[1]:8s}  CR={r[3]:>5.1f}/1024  SE={r[4]:.4f}" for r in tbl]
        self._mcs_cb["values"] = opts
        idx = min(select_idx, len(opts)-1)
        self._mcs_cb.current(idx)
        self._on_change()

    def _on_table_change(self):
        prev = self._mcs_cb.current()
        self._rebuild_mcs_options(select_idx=prev)

    def _on_oh_preset(self):
        k = self._ohp_var.get()
        if k != "Custom":
            self._oh_var.set(OH_PRESETS[k])
        self._on_change()

    def get(self) -> dict | None:
        try:
            tbl_key = self._tbl_var.get()
            tbl = MCS_TABLES[tbl_key]
            idx = self._mcs_cb.current()
            if idx < 0: idx = 0
            row = tbl[idx]
            return {
                "tbl_key": tbl_key, "mcs": row[0], "mod": row[1],
                "qm": row[2], "cr": row[3], "se": row[4],
                "v":    int(self._v_var.get()),
                "f":    float(self._f_var.get()),
                "nprb": int(self._nprb_var.get()),
                "mu":   MU_VALUES.get(self._mu_var.get(), 1),
                "oh":   float(self._oh_var.get()) / 100.0,
            }
        except Exception:
            return None

    def update_labels(self, v: dict, ratio: float, pk: float, mc: float):
        mod_col = MOD_COLORS.get(v["mod"], C["fg"])
        self._mod_lbl.config(
            text=f"  {v['mod']}  Qm={v['qm']}  CR={v['cr']}/1024  SE={v['se']:.4f} b/sym  ({v['cr']/948*100:.1f}% of R_max)",
            fg=mod_col)
        bps = bits_per_slot(v)
        self._ri["bps"].config(text=f"{bps/1000:.2f} kbits")
        self._ri["bprb"].config(text=f"{bps/v['nprb']:.1f} bits")
        self._ri["se"].config(text=f"{v['se']:.4f} b/sym")
        self._ri["mcs"].config(text=f"{mc:.2f} Mbps")
        self._ri["pk"].config(text=f"{pk:.2f} Mbps")
        self._pdr_lbl.config(text=f"{mc:.2f} / {pk:.2f} Mbps")


# ══════════════════════════════════════════════════════════════
#  MCS CHART (Canvas-based bar chart)
# ══════════════════════════════════════════════════════════════
class MCSChart(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=C["bg2"], **kw)
        self._canvas = tk.Canvas(self, bg=C["bg2"], highlightthickness=0, height=120)
        self._canvas.pack(fill="x", expand=True, padx=4, pady=(4,0))
        self._legend = tk.Frame(self, bg=C["bg2"])
        self._legend.pack(fill="x", padx=4, pady=3)
        self._canvas.bind("<Configure>", lambda _: self._redraw())
        self._rows = []
        self._sel  = 0

    def update(self, tbl_key: str, sel_idx: int):
        self._rows = MCS_TABLES[tbl_key]
        self._sel  = sel_idx
        self._redraw()

    def _redraw(self):
        c = self._canvas
        c.delete("all")
        W = c.winfo_width()
        H = c.winfo_height()
        if not self._rows or W < 10:
            return
        rows = self._rows
        max_se = max(r[4] for r in rows)
        n = len(rows)
        gap = max(3, (W-6)//n)
        bw  = max(2, gap-1)
        pad_b = 20
        pad_t = 10

        # gridlines
        for se_v in [0,1,2,3,4,5,6,7,8]:
            if se_v > max_se + 0.3:
                break
            y = (H-pad_b) - (se_v/max_se)*(H-pad_b-pad_t)
            c.create_line(0, y, W, y, fill=C["border"], width=0.5)
            if se_v % 2 == 0:
                c.create_text(2, y-2, text=str(se_v), fill=C["fg3"],
                               font=("Consolas",7), anchor="w")

        # bars
        mods_seen = []
        for i, row in enumerate(rows):
            idx, mod, qm, cr, se = row
            col = MOD_COLORS.get(mod, C["fg2"])
            if mod not in mods_seen:
                mods_seen.append(mod)
            x = 4 + i*gap
            bh = (se/max_se)*(H-pad_b-pad_t)
            y  = (H-pad_b) - bh
            sel = (i == self._sel)
            alpha = "" if sel else "77"
            c.create_rectangle(x, y, x+bw, H-pad_b,
                                fill=col, outline=col if sel else "")
            if sel:
                c.create_rectangle(x-1, y-1, x+bw+1, H-pad_b+1,
                                   fill="", outline=col, width=2)
                c.create_text(x+bw//2, y-4, text=f"{se:.2f}",
                               fill=col, font=("Consolas",7), anchor="s")
            if idx % 4 == 0 or i == len(rows)-1:
                c.create_text(x+bw//2, H-pad_b+6, text=str(idx),
                               fill=C["fg3"], font=("Consolas",7))

        # axis labels
        c.create_text(2, 6, text="SE (b/sym)", fill=C["fg2"],
                      font=("Consolas",7), anchor="w")
        c.create_text(W-2, H-3, text="MCS index →", fill=C["fg3"],
                      font=("Consolas",7), anchor="e")

        # legend
        for w in self._legend.winfo_children():
            w.destroy()
        for mod in mods_seen:
            col = MOD_COLORS.get(mod, C["fg2"])
            fr = tk.Frame(self._legend, bg=C["bg2"])
            fr.pack(side="left", padx=6)
            tk.Frame(fr, bg=col, width=10, height=10).pack(side="left")
            _lbl(fr, f" {mod}", color=col, font=FONTS["mono_sm"], bg=C["bg2"]).pack(side="left")


# ══════════════════════════════════════════════════════════════
#  MCS REFERENCE TABLE (Treeview)
# ══════════════════════════════════════════════════════════════
class MCSRefTable(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=C["bg2"], **kw)
        cols = ("MCS","Mod","Qm","CR×1024","SE b/sym","% R_max")
        self._tv = ttk.Treeview(self, columns=cols, show="headings",
                                 height=10, style="Dark.Treeview")
        for col in cols:
            w = 80 if col in ("MCS","Qm") else 120
            self._tv.heading(col, text=col)
            self._tv.column(col, width=w, anchor="center")
        sb = ttk.Scrollbar(self, orient="vertical", command=self._tv.yview)
        self._tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._tv.pack(side="left", fill="both", expand=True)
        self._tv.tag_configure("sel_row", background=C["bg5"], foreground=C["amber"])

    def update(self, tbl_key: str, sel_idx: int):
        tbl = MCS_TABLES[tbl_key]
        for row in self._tv.get_children():
            self._tv.delete(row)
        for i, (idx, mod, qm, cr, se) in enumerate(tbl):
            pct = f"{cr/948*100:.1f}%"
            tags = ("sel_row",) if i == sel_idx else ()
            iid = self._tv.insert("", "end",
                                   values=(idx, mod, qm, f"{cr}", f"{se:.4f}", pct),
                                   tags=tags)
            if i == sel_idx:
                self._tv.see(iid)


# ══════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("5G NR PDR Calculator  —  TS 38.306 Eq.(1)  +  TS 38.214 V17.1.0 MCS Tables")
        self.configure(bg=C["bg"])
        self.minsize(1100, 700)
        self._cards: list[LayerCard] = []
        self._setup_ttk()
        self._build()

    def _setup_ttk(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=C["bg"], foreground=C["fg"],
                         font=FONTS["mono"])
        style.configure("Vertical.TScrollbar", background=C["bg3"],
                         troughcolor=C["bg2"], arrowcolor=C["fg2"],
                         borderwidth=0, width=8)
        style.configure("Dark.TCombobox", fieldbackground=C["bg2"],
                         background=C["bg3"], foreground=C["fg"],
                         arrowcolor=C["amber"], selectbackground=C["bg4"],
                         selectforeground=C["cyan2"], bordercolor=C["border"])
        style.map("Dark.TCombobox",
                  fieldbackground=[("readonly", C["bg2"])],
                  selectbackground=[("readonly", C["bg4"])],
                  selectforeground=[("readonly", C["cyan2"])])
        style.configure("Dark.Treeview", background=C["bg3"],
                         foreground=C["fg2"], fieldbackground=C["bg3"],
                         rowheight=20, font=FONTS["mono_sm"],
                         bordercolor=C["border"])
        style.configure("Dark.Treeview.Heading", background=C["bg2"],
                         foreground=C["fg3"], font=FONTS["mono_sm"],
                         relief="flat", borderwidth=0)
        style.map("Dark.Treeview",
                  background=[("selected", C["bg4"])],
                  foreground=[("selected", C["cyan"])])

    def _build(self):
        # topbar
        top = tk.Frame(self, bg="#070a12", pady=8, padx=16)
        top.pack(fill="x")
        _lbl(top, "5G NR  PDR Calculator",
             color=C["amber"], font=FONTS["mono_hd"], bg="#070a12").pack(side="left")
        _lbl(top, "  TS 38.306 Eq.(1)  +  TS 38.214 V17.1.0 MCS Tables",
             color=C["fg3"], font=FONTS["mono_sm"], bg="#070a12").pack(side="left")
        _lbl(top, f"R_max = 948/1024 = {R_MAX:.6f}",
             color=C["cyan"], font=FONTS["mono_sm"], bg="#070a12").pack(side="right")

        # formula bar
        fbar = tk.Frame(self, bg=C["bg2"], padx=16, pady=7,
                        highlightbackground=C["border"], highlightthickness=1)
        fbar.pack(fill="x")
        _lbl(fbar, "PDR_peak = 10⁻⁶ × Σⱼ[v·Q_m·f·R_max·(N_PRB·12/Tₛᵘ)·(1−OH)] × TDD_ratio",
             color=C["cyan"], bg=C["bg2"], font=FONTS["mono"]).pack(anchor="w")
        _lbl(fbar, "Rate@MCS uses actual CR from 38.214 table  |  SE = Q_m·(CR/1024)  |  Bits/slot = N_PRB·12·14·(1−OH)·Q_m·(CR/1024)",
             color=C["fg3"], bg=C["bg2"], font=FONTS["mono_sm"]).pack(anchor="w", pady=(2,0))

        # main body
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=C["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(10,5), pady=6)

        right = tk.Frame(body, bg=C["bg2"],
                         highlightbackground=C["border"], highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=6)

        self._build_tdd(left)
        self._build_layers(left)
        self._build_results(right)

    def _build_tdd(self, parent):
        _section(parent, "TDD Slot Configuration")
        tdd = tk.Frame(parent, bg=C["bg2"], padx=12, pady=9,
                       highlightbackground=C["border"], highlightthickness=1)
        tdd.pack(fill="x", pady=(0,6))
        tdd.columnconfigure(1, weight=1)

        _lbl(tdd, "Slot pattern  (D=DL, U=UL, S=Special):", bg=C["bg2"]).grid(
            row=0, column=0, sticky="w", pady=2)
        self._tdd_var = tk.StringVar(value="DDDSUUDDDSUU")
        e = tk.Entry(tdd, textvariable=self._tdd_var, width=30,
                     bg=C["bg"], fg=C["cyan"], insertbackground=C["cyan"],
                     font=("Consolas",13,), relief="flat",
                     highlightbackground=C["border2"], highlightthickness=1)
        e.grid(row=0, column=1, sticky="ew", padx=(6,0), pady=2)
        self._tdd_var.trace_add("write", lambda *_: self._refresh())

        _lbl(tdd, "DL symbols in S slot (0–14):", bg=C["bg2"]).grid(
            row=1, column=0, sticky="w", pady=2)
        self._s_dl_var = tk.IntVar(value=6)
        _spinbox(tdd, self._s_dl_var, 0, 14, cmd=self._refresh).grid(
            row=1, column=1, sticky="w", padx=(6,0), pady=2)
        self._s_dl_var.trace_add("write", lambda *_: self._refresh())

        # quick-load
        ql = tk.Frame(tdd, bg=C["bg2"])
        ql.grid(row=2, column=0, columnspan=2, sticky="w", pady=(3,0))
        _lbl(ql, "Quick: ", color=C["fg3"], bg=C["bg2"]).pack(side="left")
        for pat, label in [("DDDDDDDSUU","ms5 7D·1S·2U"),("DDSUU","ms2.5"),
                            ("DDDDDDDDDDSUUU","ms10"),("DDDSUUDDDSUU","2×ms5")]:
            btn = tk.Button(ql, text=label, bg=C["bg3"], fg=C["cyan2"],
                            font=FONTS["mono_sm"], relief="flat", bd=0,
                            padx=5, pady=1, cursor="hand2",
                            command=lambda p=pat: [self._tdd_var.set(p), self._refresh()])
            btn.pack(side="left", padx=2)

        self._tdd_stats_lbl = _lbl(tdd, "—", color=C["amber"],
                                    font=FONTS["mono_b"], bg=C["bg2"])
        self._tdd_stats_lbl.grid(row=3, column=0, columnspan=2, sticky="w", pady=(4,0))

        # slot visualiser
        _lbl(tdd, "Slot pattern visualiser:", color=C["fg3"],
             bg=C["bg2"], font=FONTS["mono_sm"]).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(5,1))
        self._slot_canvas = tk.Canvas(tdd, bg=C["bg"], highlightthickness=0, height=32)
        self._slot_canvas.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0,2))
        self._slot_canvas.bind("<Configure>", lambda _: self._draw_slots())

    def _build_layers(self, parent):
        hdr = tk.Frame(parent, bg=C["bg"])
        hdr.pack(fill="x", pady=(4,2))
        _lbl(hdr, "▸ Layers / Component Carriers",
             color=C["amber"], font=FONTS["mono_hd"]).pack(side="left")
        tk.Frame(hdr, bg=C["border"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8,8), pady=5)
        tk.Button(hdr, text="  + Add Layer  ",
                  bg=C["bg3"], fg=C["cyan2"], font=FONTS["mono_b"],
                  relief="flat", bd=0, cursor="hand2", padx=6, pady=3,
                  activebackground=C["bg4"], activeforeground=C["cyan2"],
                  command=self._add_layer).pack(side="right")

        wrap = tk.Frame(parent, bg=C["bg"])
        wrap.pack(fill="both", expand=True)
        self._cv = tk.Canvas(wrap, bg=C["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self._cv.yview,
                             style="Vertical.TScrollbar")
        self._cv.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._cv.pack(side="left", fill="both", expand=True)
        self._lf = tk.Frame(self._cv, bg=C["bg"])
        self._lf_id = self._cv.create_window((0,0), window=self._lf, anchor="nw")
        self._cv.bind("<Configure>", lambda e: self._cv.itemconfig(self._lf_id, width=e.width))
        self._lf.bind("<Configure>", lambda _: self._cv.configure(scrollregion=self._cv.bbox("all")))
        self._cv.bind_all("<MouseWheel>", lambda e: self._cv.yview_scroll(int(-e.delta/120),"units"))
        self._add_layer()

    def _build_results(self, parent):
        right = tk.Frame(parent, bg=C["bg2"])
        right.pack(fill="both", expand=True, padx=12, pady=8)

        _section(right, "Effective PDR", bg=C["bg2"])
        big = tk.Frame(right, bg=C["bg3"], highlightbackground=C["amber"], highlightthickness=1, pady=12)
        big.pack(fill="x", pady=(0,8))
        _lbl(big, "Peak PDR  (R_max = 948/1024)", color=C["fg2"],
             bg=C["bg3"], font=FONTS["mono_sm"], anchor="center").pack(fill="x")
        self._big_lbl = _lbl(big, "—", color=C["amber"], bg=C["bg3"],
                              font=FONTS["mono_xl"], anchor="center")
        self._big_lbl.pack(fill="x")
        _lbl(big, "Mbps  (PHY DL peak)", color=C["fg3"],
             bg=C["bg3"], font=FONTS["mono_sm"], anchor="center").pack(fill="x")

        # metric grid
        metrics = tk.Frame(right, bg=C["bg2"])
        metrics.pack(fill="x", pady=(0,8))
        metrics.columnconfigure((0,1), weight=1)

        def metric(r, c, label, color):
            f = tk.Frame(metrics, bg=C["bg3"],
                         highlightbackground=C["border"], highlightthickness=1)
            f.grid(row=r, column=c, padx=3, pady=3, sticky="ew")
            _lbl(f, label, color=C["fg3"], bg=C["bg3"],
                 font=FONTS["mono_sm"]).pack(anchor="w", padx=8, pady=(4,0))
            v = tk.StringVar(value="—")
            _lbl(f, textvariable=v, color=color, bg=C["bg3"],
                 font=FONTS["mono_b"]).pack(anchor="w", padx=8, pady=(0,4))
            return v

        self._v_ratio  = metric(0,0,"TDD DL ratio",   C["cyan"])
        self._v_notdd  = metric(0,1,"PDR (no TDD)",   C["fg"])
        self._v_mcs    = metric(1,0,"Rate @ MCS (×TDD)", C["green"])
        self._v_eff    = metric(1,1,"MCS efficiency", C["amber"])

        _section(right, "Per-Layer Breakdown", bg=C["bg2"])
        self._bdown = tk.Frame(right, bg=C["bg2"])
        self._bdown.pack(fill="x")

        _section(right, "MCS SE Chart  (Layer 1 table)", bg=C["bg2"])
        self._chart = MCSChart(right)
        self._chart.pack(fill="x", pady=(0,6))

        _section(right, "MCS Reference Table  (Layer 1)", bg=C["bg2"])
        self._mcs_tbl = MCSRefTable(right)
        self._mcs_tbl.pack(fill="x", pady=(0,6))

        _section(right, "Key Parameters  (Layer 1)", bg=C["bg2"])
        pf = tk.Frame(right, bg=C["bg2"])
        pf.pack(fill="x")
        self._pd_rows = []
        for _ in range(16):
            row = tk.Frame(pf, bg=C["bg2"],
                           highlightbackground=C["border"], highlightthickness=0)
            row.pack(fill="x")
            tk.Frame(row, bg=C["border"], height=1).pack(fill="x")
            lk = _lbl(row, "", color=C["fg3"], bg=C["bg2"], font=FONTS["mono_sm"])
            lk.pack(side="left", padx=(0,0))
            lv = _lbl(row, "", color=C["cyan2"], bg=C["bg2"], font=FONTS["mono_sm"], anchor="e")
            lv.pack(side="right")
            self._pd_rows.append((lk, lv))

    # ── layer ops
    def _add_layer(self):
        card = LayerCard(self._lf, on_remove=self._rm_layer, on_change=self._refresh)
        card.pack(fill="x", pady=3, padx=1)
        self._cards.append(card)
        self._refresh()

    def _rm_layer(self, card):
        if card in self._cards:
            self._cards.remove(card)
        card.destroy()
        self._refresh()

    # ── slot vis
    def _draw_slots(self):
        c = self._slot_canvas
        c.delete("all")
        pat = self._tdd_var.get().upper()
        try: s_dl = int(self._s_dl_var.get())
        except: s_dl = 6
        W = c.winfo_width()
        if W < 10 or not pat: return
        chars = [x for x in pat if x in "DUS"]
        n = len(chars)
        if n == 0: return
        bw = max(3, (W-4)//n - 1)
        gap = (W-4)//n
        colors = {"D":("#1a3a52",C["cyan"]), "U":("#1e1a1a",C["fg3"]), "S":("#3a2800",C["amber"])}
        for i, ch in enumerate(chars):
            x = 2 + i*gap
            bg_c, fg_c = colors.get(ch, (C["bg3"], C["fg2"]))
            c.create_rectangle(x, 2, x+bw, 30, fill=bg_c, outline=bg_c)
            if bw > 12:
                c.create_text(x+bw//2, 16, text=ch, fill=fg_c, font=("Consolas",8,"bold"))

    # ── main refresh
    def _refresh(self, *_):
        pat = self._tdd_var.get()
        try: s_dl = int(self._s_dl_var.get())
        except: s_dl = 6
        ratio, stats = tdd_ratio(pat, s_dl)
        nD,nS,nU,total,dlEq = stats["D"],stats["S"],stats["U"],stats["total"],stats["dlEq"]
        self._tdd_stats_lbl.config(
            text=f"D={nD}  S={nS}(×{s_dl}sym)  U={nU}  |  total={total}  |  DL_equiv={dlEq:.3f}  |  DL ratio={ratio*100:.2f}%")
        self._draw_slots()

        if not self._cards: return
        vals = [c.get() for c in self._cards if c.get()]
        if not vals: return

        tot_pk=0; tot_mc=0
        for i,(card,v) in enumerate(zip(self._cards,vals)):
            pk = pdr_peak(v, ratio); mc = pdr_mcs(v, ratio)
            card.update_labels(v, ratio, pk, mc)
            tot_pk+=pk; tot_mc+=mc

        tot_pk_notdd = sum(pdr_peak(v, 1.0) for v in vals)
        eff = (tot_mc/tot_pk*100) if tot_pk>0 else 0

        self._big_lbl.config(text=f"{tot_pk:.1f}")
        self._v_ratio.set(f"{ratio:.4f}  ({ratio*100:.1f}%)")
        self._v_notdd.set(f"{tot_pk_notdd:.2f} Mbps")
        self._v_mcs.set(f"{tot_mc:.2f} Mbps")
        self._v_eff.set(f"{eff:.1f}%")

        # breakdown
        for w in self._bdown.winfo_children(): w.destroy()
        for i,v in enumerate(vals):
            pk=pdr_peak(v,ratio); mc=pdr_mcs(v,ratio)
            fr = tk.Frame(self._bdown, bg=C["bg3"],
                          highlightbackground=C["border"], highlightthickness=1, padx=8, pady=4)
            fr.pack(fill="x", pady=2)
            _lbl(fr, f"L{i+1}  MCS{v['mcs']}  {v['mod']}  v={v['v']}  PRB={v['nprb']}  μ={v['mu']}  OH={v['oh']*100:.0f}%",
                 color=C["fg2"], bg=C["bg3"], font=FONTS["mono_sm"]).pack(side="left")
            _lbl(fr, f"{mc:.2f} / {pk:.2f} Mbps",
                 color=C["green"], bg=C["bg3"], font=FONTS["mono_b"]).pack(side="right")

        # chart & table (Layer 1)
        v0 = vals[0]
        tbl = MCS_TABLES[v0["tbl_key"]]
        sel_idx = next((i for i,r in enumerate(tbl) if r[0]==v0["mcs"]), 0)
        self._chart.update(v0["tbl_key"], sel_idx)
        self._mcs_tbl.update(v0["tbl_key"], sel_idx)

        # key params
        bps = bits_per_slot(v0); tsv = Ts(v0["mu"])
        params = [
            ("MCS index (L1)",   f"{v0['mcs']}  →  {TBL_KEYS.index(v0['tbl_key'])+1} of 4 tables"),
            ("Modulation",        f"{v0['mod']}  →  Qm = {v0['qm']} bits/sym"),
            ("Code rate CR",      f"{v0['cr']}/1024 = {v0['cr']/1024:.6f}"),
            ("Spectral eff SE",   f"{v0['se']:.4f} b/sym  (Qm × CR/1024)"),
            ("R_max (38.306)",    f"948/1024 = {R_MAX:.6f}"),
            ("MCS efficiency",    f"CR/948 = {v0['cr']/948*100:.2f}%"),
            ("SE @ R_max",        f"{v0['qm']}×{R_MAX:.4f} = {v0['qm']*R_MAX:.4f} b/sym"),
            ("T_s^μ (μ="+str(v0['mu'])+")", f"{tsv*1e6:.3f} μs"),
            ("Slots/sec",         f"{round(1/tsv/14):,}"),
            ("Total RE/slot",     f"{v0['nprb']}×12×14 = {v0['nprb']*168}"),
            ("RE/slot after OH",  f"{v0['nprb']*168*(1-v0['oh']):.0f}  (OH={v0['oh']*100:.1f}%)"),
            ("Bits/slot @ MCS",   f"{bps/1000:.2f} kbits  ({bps/v0['nprb']:.1f}/PRB)"),
            ("Bits/slot @ R_max", f"{v0['nprb']*168*(1-v0['oh'])*v0['qm']*R_MAX/1000:.2f} kbits"),
            ("DL equiv/period",   f"{dlEq:.3f} / {total} slots  ({ratio*100:.2f}%)"),
        ]
        for i,(k,val) in enumerate(params):
            if i < len(self._pd_rows):
                self._pd_rows[i][0].config(text=k)
                self._pd_rows[i][1].config(text=val)


if __name__ == "__main__":
    app = App()
    app.mainloop()