"""Demonstrate city-held-out prediction and equal-city SHAP summaries."""

import argparse
import json

import numpy as np
import pandas as pd
from catboost import Pool
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error

from study import CONFIG, FEATURES, OUTPUT, TARGET, city_split, fit_model, load_sample


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--held-out-city", default="Wuhan")
    parser.add_argument("--all-cities", action="store_true", help="Evaluate all 41 held-out cities")
    args = parser.parse_args()
    frame = load_sample()
    OUTPUT.mkdir(exist_ok=True)
    cities = sorted(frame.city.unique()) if args.all_cities else [args.held_out_city]
    scores = []
    for city in cities:
        train, test = city_split(frame, city)
        model = fit_model(train)
        predicted = model.predict(test[FEATURES])
        scores.append({"city": city, "stratum": test.stratum.iloc[0],
                       "training_cells": len(train), "held_out_cells": len(test),
                       "r2": r2_score(test[TARGET], predicted),
                       "rmse_k": root_mean_squared_error(test[TARGET], predicted),
                       "mae_k": mean_absolute_error(test[TARGET], predicted)})
    scores = pd.DataFrame(scores)
    scores.to_csv(OUTPUT / "demo_city_validation.csv", index=False)

    regional = fit_model(frame)
    shap = regional.get_feature_importance(Pool(frame[FEATURES]), type="ShapValues", thread_count=4)
    np.testing.assert_allclose(shap.sum(axis=1), regional.predict(frame[FEATURES]), atol=1e-8)
    absolute = pd.DataFrame(np.abs(shap[:, :-1]), columns=FEATURES)
    absolute["city"] = frame.city.to_numpy()
    city_means = absolute.groupby("city", sort=True).mean()
    category_means = pd.DataFrame({
        category: city_means[[f for f in members if f in FEATURES]].sum(axis=1)
        for category, members in CONFIG["categories"].items()
    })
    city_means["stratum"] = frame.groupby("city", observed=True).stratum.first()
    category_means["stratum"] = city_means.stratum
    # Average cities before expressing category contributions as shares.
    stratum_means = category_means.groupby("stratum", observed=True).mean()
    stratum_shares = stratum_means.div(stratum_means.sum(axis=1), axis=0) * 100
    city_means.to_csv(OUTPUT / "demo_city_mean_absolute_shap.csv")
    stratum_shares.to_csv(OUTPUT / "demo_stratum_shap_shares.csv")
    metadata = {"sample_cells": len(frame), "model_inputs": FEATURES,
                "parameters": CONFIG["catboost_parameters"],
                "validation": "Each listed city is excluded from its prediction model",
                "interpretation": "A separate regional model fitted to the released sample",
                "result_scope": "Demonstration sample; full-study results are in data/summary"}
    (OUTPUT / "demo_catboost_run.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(scores.to_string(index=False))
    print("\nEqual-city category shares from the demonstration model (%):")
    print(stratum_shares.round(2).to_string())
    print("\nThese sample results do not replace the manuscript estimates.")


if __name__ == "__main__":
    main()
