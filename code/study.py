"""Shared data definitions for the SUHI and joint greening examples."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "data/study_config.json").read_text(encoding="utf-8"))
FEATURES = CONFIG["features"]
TARGET = CONFIG["target"]
JOINT = CONFIG["joint_variables"]
OUTPUT = ROOT / "outputs"


def read_csv(path):
    return pd.read_csv(path, float_precision="round_trip")


def validate_features(frame):
    missing = sorted(set(FEATURES) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing model columns: {missing}")
    if not np.isfinite(frame[FEATURES].to_numpy(dtype=float)).all():
        raise ValueError("Model inputs contain missing or nonfinite values")


def load_sample():
    frame = read_csv(ROOT / "data/sample/model_sample_2020_2025.csv")
    validate_features(frame)
    if not frame.cell_id.is_unique or not np.isfinite(frame[TARGET]).all():
        raise ValueError("Invalid sample identifiers or outcomes")
    return frame


def city_split(frame, city):
    if city not in set(frame.city):
        raise ValueError(f"City not in sample: {city}")
    train = frame.loc[frame.city.ne(city)].copy()
    test = frame.loc[frame.city.eq(city)].copy()
    if train.empty or test.empty:
        raise ValueError("Both training and held-out data are required")
    if set(train.city) & set(test.city) or set(train.cell_id) & set(test.cell_id):
        raise ValueError("Training and held-out data overlap")
    return train, test


def fit_model(frame):
    validate_features(frame)
    model = CatBoostRegressor(**CONFIG["catboost_parameters"])
    model.fit(frame[FEATURES], frame[TARGET])
    return model


def joint_scenario(target, donor):
    if len(target) != len(donor):
        raise ValueError("Unequal target and greener-reference lengths")
    if not np.array_equal(target.city.to_numpy(), donor.city.to_numpy()):
        raise ValueError("A reference profile belongs to another city")
    if (target.PLAND_water.to_numpy() + donor.PLAND_veg.to_numpy()
            + donor.PLAND_imperv.to_numpy() > 1.02 + 1e-12).any():
        raise ValueError("Scenario exceeds the allowed land cover sum")
    if (donor.PLAND_imperv.to_numpy() + .05 + 1e-12
            < target.Built_surface_fraction.to_numpy()).any():
        raise ValueError("Scenario conflicts with the retained building fraction")
    scenario = target.copy()
    scenario[JOINT] = donor[JOINT].to_numpy()
    scenario["FVC"] = np.clip((scenario.NDVI_mean - .05) / .80, 0, 1) ** 2
    scenario["FAR"] = scenario.Bld_Volume_density / 3
    fixed = CONFIG["fixed_variables"]
    np.testing.assert_array_equal(scenario[fixed], target[fixed])
    validate_features(scenario)
    return scenario


def validate_profile_levels(target, donor, pairs):
    for level, (lo, hi, vegetation, impervious) in CONFIG["profile_definitions"].items():
        mask = pairs.profile_level.eq(level).to_numpy()
        delta_ndvi = donor.NDVI_mean.to_numpy()[mask] - target.NDVI_mean.to_numpy()[mask]
        delta_lai = donor.LAI.to_numpy()[mask] - target.LAI.to_numpy()[mask]
        delta_veg = donor.PLAND_veg.to_numpy()[mask] - target.PLAND_veg.to_numpy()[mask]
        removed_isa = target.PLAND_imperv.to_numpy()[mask] - donor.PLAND_imperv.to_numpy()[mask]
        if not ((delta_ndvi >= lo - 1e-12).all() and (delta_ndvi <= hi + 1e-12).all()
                and (delta_lai >= -1e-12).all() and (delta_veg >= vegetation - 1e-12).all()
                and (removed_isa >= impervious - 1e-12).all()):
            raise ValueError(f"Profile does not meet {level} criteria")
    if not set(pairs.profile_level).issubset(CONFIG["profile_definitions"]):
        raise ValueError("Unknown scenario level")


def load_pairs(city=None):
    pairs = read_csv(ROOT / "data/sample/greening_pairs_2020_2025.csv")
    cells = read_csv(ROOT / "data/sample/greening_cells_2020_2025.csv")
    if not cells.cell_id.is_unique:
        raise ValueError("Duplicate greener-reference cell identifiers")
    if city is not None:
        pairs = pairs.loc[pairs.city.eq(city)].reset_index(drop=True)
    if pairs.empty:
        raise ValueError("No pairs for the requested city")
    source = cells.set_index("cell_id", drop=False)
    target = source.loc[pairs.cell_id].reset_index(drop=True)
    donor = source.loc[pairs.donor_cell_id].reset_index(drop=True)
    if not np.array_equal(pairs.city, target.city):
        raise ValueError("Pair identifiers and city labels disagree")
    validate_profile_levels(target, donor, pairs)
    return pairs, target, donor


def verify_release_files():
    checks = json.loads((ROOT / "data/file_checksums.json").read_text(encoding="utf-8"))
    for name, expected in checks.items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("Checksum path outside repository")
        with path.open("rb") as stream:
            observed = hashlib.file_digest(stream, "sha256").hexdigest()
        if observed != expected:
            raise ValueError(f"Checksum mismatch: {name}")
    return len(checks)
