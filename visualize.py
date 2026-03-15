import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

# Arguman al ya da varsayilan kullan
input_csv  = sys.argv[1] if len(sys.argv) > 1 else "read_stats.csv"
output_png = sys.argv[2] if len(sys.argv) > 2 else "qc_plots.png"

# Cikti klasorunu olustur
os.makedirs(os.path.dirname(output_png), exist_ok=True) if os.path.dirname(output_png) else None

df = pd.read_csv(input_csv)

print("=" * 50)
print("OZET ISTATISTIKLER")
print("=" * 50)

for col, label in [("read_length", "Read Uzunlugu (bp)"),
                   ("gc_content",  "GC Icerigi (%)"),
                   ("mean_quality","Ortalama Kalite (Phred)")]:
    print(f"\n{label}:")
    print(f"  Ortalama : {df[col].mean():.2f}")
    print(f"  Medyan   : {df[col].median():.2f}")
    print(f"  Min      : {df[col].min():.2f}")
    print(f"  Maks     : {df[col].max():.2f}")
    print(f"  Std      : {df[col].std():.2f}")

print("\n" + "=" * 50)
q20 = (df["mean_quality"] >= 20).sum()
q20_pct = q20 / len(df) * 100
print(f"Q20 uzeri read sayisi : {q20} / {len(df)} ({q20_pct:.1f}%)")
print("=" * 50)

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Barcode77 - Long Read QC Ozeti", fontsize=16, fontweight="bold")

# 1. Read Uzunlugu
log_lengths = np.log10(df["read_length"])
axes[0].hist(log_lengths, bins=80, color="#4C72B0", edgecolor="white", linewidth=0.3)
axes[0].axvline(np.log10(df["read_length"].median()), color="red", linestyle="--",
                linewidth=1.5, label=f'Medyan: {df["read_length"].median():.0f} bp')
axes[0].set_title("Read Uzunlugu Dagilimi (log10)")
axes[0].set_xlabel("log10(Uzunluk bp)")
axes[0].set_ylabel("Read Sayisi")
axes[0].legend()

# 2. GC Icerigi
axes[1].hist(df["gc_content"], bins=60, color="#55A868", edgecolor="white", linewidth=0.3)
axes[1].axvline(df["gc_content"].median(), color="red", linestyle="--", linewidth=1.5,
                label=f'Medyan: {df["gc_content"].median():.1f}%')
axes[1].axvline(40, color="orange", linestyle=":", linewidth=1.2, label="Normal alt sinir (40%)")
axes[1].axvline(60, color="orange", linestyle=":", linewidth=1.2, label="Normal ust sinir (60%)")
axes[1].set_title("GC Icerigi Dagilimi")
axes[1].set_xlabel("GC Icerigi (%)")
axes[1].set_ylabel("Read Sayisi")
axes[1].legend(fontsize=8)

# 3. Kalite Skoru
axes[2].hist(df["mean_quality"], bins=60, color="#C44E52", edgecolor="white", linewidth=0.3)
axes[2].axvline(df["mean_quality"].median(), color="black", linestyle="--", linewidth=1.5,
                label=f'Medyan: {df["mean_quality"].median():.1f}')
axes[2].axvline(20, color="orange", linestyle=":", linewidth=1.5, label="Q20 esigi")
axes[2].set_title("Ortalama Kalite Skoru Dagilimi")
axes[2].set_xlabel("Phred Kalite Skoru")
axes[2].set_ylabel("Read Sayisi")
axes[2].legend()

plt.tight_layout()
plt.savefig(output_png, dpi=150, bbox_inches="tight")
print(f"\nGrafik kaydedildi: {output_png}")
