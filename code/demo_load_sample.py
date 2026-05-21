"""
Minimal demo: load the released sample CSV and inspect its schema.

Run from repository root:
    python code/demo_load_sample.py
"""
from pathlib import Path
import pandas as pd

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "clean_41_smod_sample_n2000.csv"


def main() -> None:
    df = pd.read_csv(SAMPLE)
    print(f"loaded {SAMPLE.name}: {len(df):,} rows, {len(df.columns)} columns")
    print()
    print("columns:")
    for col in df.columns:
        print(f"  - {col}")
    print()
    print("per-stratum row counts:")
    print(df["stratum"].value_counts())


if __name__ == "__main__":
    main()
