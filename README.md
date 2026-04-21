# nr-pdr-calculator

# 5G NR Peak Data Rate (PDR) Calculator

A desktop GUI calculator for estimating **5G NR Peak Data Rate (PDR)** based on **3GPP TS 38.306 Equation (1)**.

The application lets you:
- configure modulation, MIMO layers, PRBs, numerology, and overhead
- define TDD slot patterns
- compute per-layer and total PHY peak data rate
- visualize TDD downlink ratio and per-layer contribution

## Features

- Dark-themed Tkinter GUI
- Supports multiple component carriers / layers
- TDD slot pattern handling with `D`, `U`, and `S`
- Per-layer breakdown
- Live peak data rate updates
- Based on:

\[
PDR = 10^{-6} \cdot \sum_j \left[
v_{\text{Layers}}^{(j)} \cdot Q_m^{(j)} \cdot f^{(j)} \cdot R_{\max}
\cdot \frac{N_{\text{PRB}}^{\text{BW}(j),\mu} \cdot 12}{T_s^\mu}
\cdot (1 - OH^{(j)})
\right] \times TDD\_DL\_ratio
\]

## Requirements

- Python 3.8+
- Tkinter

## Run

```bash
python3 pdr_calculator.py