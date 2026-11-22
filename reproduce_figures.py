import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create output directory for figures
os.makedirs("figures", exist_ok=True)

# ==========================================
# 1. ENCRYPTION PERFORMANCE ON CORTEX-M4 (TABLE 7)
# ==========================================
df_perf = pd.DataFrame({
    "Algorithm": [
        "AES-GCM", "AES-128-CTR", "ChaCha20-Poly1305", "PRESENT-80",
        "SIMON-128", "ASCON-128a", "SPECK-128", "LEA-128",
        "GreenSec+AEAD", "GreenSec (Cipher)"
    ],
    "Type": [
        "AEAD", "Cipher", "AEAD", "Cipher",
        "Cipher", "AEAD", "Cipher", "Cipher",
        "AEAD", "Cipher"
    ],
    "Cycles_Per_Block": [6070, 4850, 3780, 2500, 1890, 1540, 1420, 1120, 1070, 420],
    "Cycles_CI": [45, 38, 32, 22, 18, 15, 14, 12, 11, 5],
    "Throughput_Kbps": [134, 168, 215, 325, 429, 527, 571, 724, 759, 1933],
    "Energy_uJ_Per_Block": [72.8, 58.2, 45.3, 30.0, 22.7, 18.5, 17.0, 13.4, 12.8, 5.0],
    "Energy_CI": [0.5, 0.4, 0.4, 0.3, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1],
    "Gain_vs_GCM": [1.0, 1.3, 1.6, 2.4, 3.2, 3.9, 4.3, 5.4, 5.7, 14.6]
})
df_perf.to_csv("encryption_performance.csv", index=False)

# ==========================================
# 2. MEMORY FOOTPRINT ON CORTEX-M4 -O2 (TABLE 8)
# ==========================================
df_mem = pd.DataFrame({
    "Algorithm": [
        "AES-GCM", "AES-128-CTR", "ChaCha20-Poly1305",
        "GreenSec+AEAD", "LEA-128 (24r)", "SIMON-128", "ASCON-128a"
    ],
    "Flash_Bytes": [3680, 2840, 2560, 1820, 1680, 1240, 980],
    "RAM_Bytes": [256, 192, 176, 112, 128, 96, 40]
})
df_mem.to_csv("memory_footprint.csv", index=False)

# ==========================================
# 3. PIPELINE LATENCY BREAKDOWN (TABLE 9)
# ==========================================
df_pipe = pd.DataFrame({
    "Pipeline_Stage": ["Phase I (ASCON-8 Init)", "Phase II (LEA-5 CTR)", "Phase III (ASCON-MAC)"],
    "Cycles": [320, 420, 330],
    "Latency_us": [4.0, 5.2, 4.1],
    "Percentage_Total_Time": [29.9, 39.2, 30.9]
})
df_pipe.to_csv("pipeline_latency.csv", index=False)

# ==========================================
# 4. ECG BATTERY LIFETIME (FIG. 7 & SEC 5.3)
# ==========================================
df_batt = pd.DataFrame({
    "Scheme": ["AES-GCM", "AES-128-CTR", "PRESENT-80", "SIMON/SPECK", "ASCON-128a", "GreenSec+AEAD", "GreenSec (Cipher)"],
    "Battery_Lifetime_Hours": [14.8, 16.6, 21.5, 24.8, 25.8, 28.1, 30.6]
})
df_batt.to_csv("battery_lifetime.csv", index=False)

# ==========================================
# 5. GENERATE HIGH-RESOLUTION FIGURES (300 DPI)
# ==========================================

# Fig 1: AEAD vs Cipher-Only Energy & Latency (Table 7 / Fig 6)
aead_subset = df_perf[df_perf["Algorithm"].isin(["AES-GCM", "ChaCha20-Poly1305", "ASCON-128a", "GreenSec+AEAD", "GreenSec (Cipher)"])]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))
colors = ["#c0392b", "#e67e22", "#8e44ad", "#16a085", "#1b4f72"]

b1 = ax1.bar(aead_subset["Algorithm"], aead_subset["Energy_uJ_Per_Block"], color=colors, edgecolor="black", width=0.55)
for b, v in zip(b1, aead_subset["Energy_uJ_Per_Block"]):
    ax1.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontweight="bold", fontsize=9.5)
ax1.set_ylabel("Energy per Block (µJ)", fontweight="bold")
ax1.set_title("(a) Energy Consumption on Cortex-M4 @ 80 MHz", fontweight="bold")
ax1.set_ylim(0, 82)
ax1.tick_params(axis="x", rotation=20)
ax1.grid(axis="y", linestyle="--", alpha=0.4)

b2 = ax2.bar(aead_subset["Algorithm"], aead_subset["Cycles_Per_Block"], color=colors, edgecolor="black", width=0.55)
for b, v in zip(b2, aead_subset["Cycles_Per_Block"]):
    ax2.text(b.get_x() + b.get_width()/2, v + 130, f"{v}", ha="center", fontweight="bold", fontsize=9.5)
ax2.set_ylabel("Cycles per Block", fontweight="bold")
ax2.set_title("(b) Execution Latency on Cortex-M4 @ 80 MHz", fontweight="bold")
ax2.set_ylim(0, 6800)
ax2.tick_params(axis="x", rotation=20)
ax2.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("figures/Fig1_Energy_Latency_AEAD.png", dpi=300, bbox_inches="tight")
plt.close()

# Fig 2: ECG Monitoring Battery Lifetime (200 mAh, 3.0V, 500 B/s)
plt.figure(figsize=(9, 4.8))
batt_colors = ["#c0392b", "#d35400", "#f39c12", "#8e44ad", "#2980b9", "#16a085", "#1b4f72"]
bars = plt.bar(df_batt["Scheme"], df_batt["Battery_Lifetime_Hours"], color=batt_colors, edgecolor="black", width=0.55)
plt.axhline(24.0, color="black", linestyle="--", linewidth=1.2, label="24h Holter Target")
for b, v in zip(bars, df_batt["Battery_Lifetime_Hours"]):
    plt.text(b.get_x() + b.get_width()/2, v + 0.6, f"{v:.1f}h", ha="center", fontweight="bold", fontsize=9.5)
plt.ylabel("Battery Lifetime (Hours)", fontsize=11, fontweight="bold")
plt.title("Continuous ECG Monitoring Battery Lifetime (200 mAh, 3.0V, 500 B/s)", fontsize=12, fontweight="bold")
plt.xticks(rotation=20, ha="right")
plt.ylim(0, 35)
plt.legend(loc="upper left", fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("figures/Fig2_ECG_Battery_Lifetime.png", dpi=300, bbox_inches="tight")
plt.close()

# Fig 3: Memory Footprint (Flash & RAM on Cortex-M4 -O2)
x = np.arange(len(df_mem["Algorithm"]))
width = 0.35
fig, ax1 = plt.subplots(figsize=(10, 4.8))
ax2 = ax1.twinx()

r1 = ax1.bar(x - width/2, df_mem["Flash_Bytes"], width, label="Flash (Bytes)", color="#2980b9", edgecolor="black")
r2 = ax2.bar(x + width/2, df_mem["RAM_Bytes"], width, label="RAM (Bytes)", color="#e67e22", edgecolor="black")

ax1.set_ylabel("Flash Memory (Bytes)", color="#2980b9", fontweight="bold", fontsize=11)
ax2.set_ylabel("RAM Memory (Bytes)", color="#e67e22", fontweight="bold", fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(df_mem["Algorithm"], rotation=20, ha="right", fontsize=10)
ax1.set_title("Memory Footprint on ARM Cortex-M4 (-O2)", fontsize=12, fontweight="bold")
ax1.grid(axis="y", linestyle="--", alpha=0.35)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

plt.tight_layout()
plt.savefig("figures/Fig3_Memory_Footprint.png", dpi=300, bbox_inches="tight")
plt.close()

# Fig 4: Pipelined Execution Latency Breakdown (Table 9)
plt.figure(figsize=(7.5, 4.5))
pipe_colors = ["#2e86c1", "#16a085", "#1b4f72"]
bars = plt.bar(df_pipe["Pipeline_Stage"], df_pipe["Cycles"], color=pipe_colors, edgecolor="black", width=0.5)
for b, c, us, pct in zip(bars, df_pipe["Cycles"], df_pipe["Latency_us"], df_pipe["Percentage_Total_Time"]):
    plt.text(b.get_x() + b.get_width()/2, c + 12, f"{c} cyc\n({us} µs | {pct}%)", ha="center", fontweight="bold", fontsize=9.5)
plt.ylabel("Execution Cycles (Cortex-M4 @ 80 MHz)", fontsize=11, fontweight="bold")
plt.title("GreenSec-WBSN Three-Phase Pipeline Breakdown (Total: 1070 Cycles / 13.3 µs)", fontsize=11, fontweight="bold")
plt.ylim(0, 520)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("figures/Fig4_Pipeline_Breakdown.png", dpi=300, bbox_inches="tight")
plt.close()

print("Done! Generated 4 CSV files and 4 figures in /figures.")