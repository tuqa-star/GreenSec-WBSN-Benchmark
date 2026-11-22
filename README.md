# GreenSec-WBSN-Benchmark

Official hardware benchmark datasets, memory footprint profiles, and 300-DPI figure reproduction scripts for our **Elsevier Microprocessors and Microsystems (2026)** article:

> **GreenSec-WBSN: a cross-layer embedded middleware with pipelined hardware-software Co-design for medical sensor networks**  
> *Tuqa Kareem Jebur, Jaime Lloret, Lourdes Peñalver, and Haider K. Hoomod*  
> Microprocessors and Microsystems, Vol. 125, 105349, 2026 (Open Access).  
> **DOI:** [10.1016/j.micpro.2026.105349](https://doi.org/10.1016/j.micpro.2026.105349)

---

## Key Hardware Highlights (ARM Cortex-M4 @ 80 MHz)
Benchmarked across 1,000 trials per measurement (STM32L476RG, ARM GCC 12.3.1 `-O2`, 64-byte ECG packets):

| Metric | GreenSec+AEAD | Improvement vs. Baselines |
| :--- | :---: | :--- |
| **Energy per Block** | **12.8 µJ** (Cipher-only: 5.0 µJ) | -82.4% vs. AES-GCM (72.8 µJ) \| -30.8% vs. ASCON-128a (18.5 µJ) |
| **Execution Latency** | **1,070 cycles/block** (13.3 µs) | 5.7× faster than AES-GCM (6,070 cycles) |
| **Throughput** | **759 Kbps** (Cipher-only: 1,933 Kbps) | Exceeds continuous medical telemetry needs |
| **Static RAM Footprint** | **112 Bytes** (Flash: 1,820 Bytes) | -56.3% RAM reduction vs. AES-GCM (256 Bytes) |
| **ECG Battery Lifetime** | **28.1 hours** (200 mAh, 3.0 V) | Exceeds 24-hour Holter monitoring target (+69% vs. AES-GCM) |

---

## Repository Contents
* `encryption_performance.csv` — Cycles/block, throughput (Kbps), energy (µJ/block), and 95% CIs across 10 AEAD and cipher-only baselines (Table 7).
* `memory_footprint.csv` — Flash and static RAM utilization on ARM Cortex-M4 `-O2` (Table 8).
* `pipeline_latency.csv` — Three-phase pipeline execution breakdown: ASCON-8 Init, LEA-5 CTR, and ASCON-MAC (Table 9).
* `battery_lifetime.csv` — Continuous 500 B/s ECG monitoring battery lifetime comparison (Fig. 7).
* `reproduce_figures.py` — Standalone Python script to regenerate all benchmark charts at 300 DPI.
* `figures/` — High-resolution PNG charts of energy, latency, memory footprint, and battery lifetime.

---

## How to Cite
If you use these hardware benchmark datasets or figures in your research, please cite our paper:

```bibtex
@ARTICLE{Jebur2026GreenSecWBSN,
  author={Jebur, Tuqa Kareem and Lloret, Jaime and Peñalver, Lourdes and Hoomod, Haider K.},
  journal={Microprocessors and Microsystems},
  title={GreenSec-WBSN: a cross-layer embedded middleware with pipelined hardware-software Co-design for medical sensor networks},
  year={2026},
  volume={125},
  pages={105349},
  doi={10.1016/j.micpro.2026.105349}
}
