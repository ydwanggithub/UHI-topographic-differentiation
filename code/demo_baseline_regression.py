"""
Minimal demo: fit a plain ordinary-least-squares regression of LST_K on
two predictors (DEM and NDVI) on the released sample.

This is illustrative only. It shows the column layout works with standard
scikit-learn, nothing more.

Run from repository root:
    python code/demo_baseline_regression.py
"""
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "clean_41_smod_sample_n2000.csv"


def main() -> None:
    df = pd.read_csv(SAMPLE).dropna(subset=["LST_K", "DEM", "NDVI"])

    X = df[["DEM", "NDVI"]].to_numpy()
    y = df["LST_K"].to_numpy()

    model = LinearRegression().fit(X, y)
    y_hat = model.predict(X)

    print(f"n = {len(df):,}")
    print(f"intercept = {model.intercept_:.3f}")
    print(f"coef DEM   = {model.coef_[0]:+.4f}")
    print(f"coef NDVI  = {model.coef_[1]:+.4f}")
    print(f"in-sample R^2 = {r2_score(y, y_hat):.4f}")


if __name__ == "__main__":
    main()
