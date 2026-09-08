"""Apply existing joint greening profiles to a city-held-out sample model."""

import argparse

import numpy as np
import pandas as pd

from study import CONFIG, FEATURES, OUTPUT, city_split, fit_model, joint_scenario, load_pairs, load_sample


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", default="Wuhan")
    args = parser.parse_args()
    train, _ = city_split(load_sample(), args.city)
    model = fit_model(train)
    pairs, target, donor = load_pairs(args.city)
    scenario = joint_scenario(target, donor)
    result = pairs.copy()
    result["scenario"] = result.profile_level.map(CONFIG["scenario_names"])
    result["baseline_prediction_k"] = model.predict(target[FEATURES])
    result["scenario_prediction_k"] = model.predict(scenario[FEATURES])
    result["cooling_k"] = result.baseline_prediction_k - result.scenario_prediction_k
    result["delta_ndvi"] = scenario.NDVI_mean - target.NDVI_mean
    result["delta_vegetation_fraction"] = scenario.PLAND_veg - target.PLAND_veg
    result["delta_impervious_fraction"] = scenario.PLAND_imperv - target.PLAND_imperv
    OUTPUT.mkdir(exist_ok=True)
    result.to_csv(OUTPUT / "demo_joint_greening_pairs.csv", index=False)
    summaries = []
    for scenario_name, group in result.groupby("scenario", sort=True):
        summaries.append({"city": args.city, "scenario": scenario_name, "sampled_pairs": len(group),
                          "sampled_changed_cell_cooling_k": np.average(group.cooling_k, weights=group.area_m2)})
    table = pd.DataFrame(summaries)
    table.to_csv(OUTPUT / "demo_joint_greening_summary.csv", index=False)
    print(table.to_string(index=False))
    print("\nMeans cover the sampled changed cells only. Manuscript urban means also include unchanged eligible land.")


if __name__ == "__main__":
    main()
