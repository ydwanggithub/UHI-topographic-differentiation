"""
Minimal demo: scatter plot of LST_K against DEM, coloured by stratum.

Run from repository root:
    python code/demo_scatter_plot.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "clean_41_smod_sample_n2000.csv"
OUT = Path(__file__).resolve().parent / "demo_scatter.png"


def main() -> None:
    df = pd.read_csv(SAMPLE).dropna(subset=["LST_K", "DEM", "stratum"])

    fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=150)
    for stratum, group in df.groupby("stratum"):
        ax.scatter(group["DEM"], group["LST_K"], s=6, alpha=0.5, label=stratum)
    ax.set_xlabel("DEM (m)")
    ax.set_ylabel("LST (K)")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT)
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
