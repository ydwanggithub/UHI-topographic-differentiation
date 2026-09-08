"""Checks for released data definitions and demonstration calculations."""

import json
from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from study import (CONFIG, FEATURES, JOINT, TARGET, city_split,
                   joint_scenario, load_pairs, load_sample, validate_features,
                   validate_profile_levels, verify_release_files)


class ReleasedDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame = load_sample()
        cls.pairs, cls.target, cls.donor = load_pairs()

    def test_checksum_manifest(self):
        self.assertGreaterEqual(verify_release_files(), 52)

    def test_sampling_counts(self):
        self.assertEqual(len(self.frame), 4100)
        self.assertEqual(self.frame.city.nunique(), 41)
        self.assertTrue(self.frame.groupby("city", observed=True).size().eq(100).all())
        self.assertTrue(self.frame.cell_id.is_unique)

    def test_original_city_groups(self):
        counts = self.frame.groupby("stratum", observed=True).city.nunique().to_dict()
        self.assertEqual(counts, {"Flat": 8, "Transitional": 12, "Hilly": 14, "Mountainous": 7})
        self.assertTrue(self.frame.groupby("city", observed=True).stratum.nunique().eq(1).all())

    def test_suhi_definition(self):
        np.testing.assert_allclose(self.frame.LST_K - self.frame.rural_reference_lst_k,
                                   self.frame[TARGET], atol=1e-10, rtol=0)
        self.assertTrue(self.frame.groupby("city", observed=True).rural_reference_lst_k.nunique().eq(1).all())

    def test_annual_temperature_summary(self):
        annual = self.frame[[f"LST_{year}_K" for year in range(2020, 2026)]]
        np.testing.assert_array_equal(annual.notna().sum(axis=1), self.frame.LST_valid_years)
        self.assertTrue(self.frame.LST_valid_years.ge(4).all())
        np.testing.assert_allclose(annual.mean(axis=1), self.frame.LST_K, atol=1e-8, rtol=0)

    def test_candidate_and_primary_features(self):
        self.assertEqual(len(CONFIG["candidate_features"]), 23)
        self.assertEqual(len(FEATURES), 21)
        self.assertEqual(set(CONFIG["candidate_features"]) - set(FEATURES), {"FAR", "FVC"})
        self.assertFalse(set(FEATURES) & {"city", "lon", "lat", TARGET, "LST_K", "rural_reference_lst_k"})
        self.assertEqual(set(FEATURES), set(JOINT) | set(CONFIG["fixed_variables"]))

    def test_derived_columns(self):
        np.testing.assert_allclose(self.frame.FAR, self.frame.Bld_Volume_density / 3, atol=1e-12)
        np.testing.assert_allclose(self.frame.FVC,
                                   np.clip((self.frame.NDVI_mean - .05) / .80, 0, 1) ** 2, atol=1e-12)

    def test_every_city_can_be_held_out(self):
        for city in self.frame.city.unique():
            train, test = city_split(self.frame, city)
            self.assertEqual(len(train), 4000)
            self.assertEqual(len(test), 100)
            self.assertNotIn(city, set(train.city))
            self.assertFalse(set(train.cell_id) & set(test.cell_id))

    def test_unknown_city_rejected(self):
        with self.assertRaises(ValueError):
            city_split(self.frame, "Unknown city")

    def test_missing_predictor_rejected(self):
        with self.assertRaises(ValueError):
            validate_features(self.frame.drop(columns=["NDVI_mean"]))

    def test_nonfinite_predictor_rejected(self):
        broken = self.frame.copy()
        broken.loc[0, "NDVI_mean"] = np.nan
        with self.assertRaises(ValueError):
            validate_features(broken)

    def test_existing_profile_coverage(self):
        self.assertEqual(len(self.pairs), 1230)
        self.assertEqual(self.pairs.city.nunique(), 41)
        self.assertEqual(set(self.pairs.profile_level), {"moderate", "primary", "upper"})
        self.assertTrue(self.pairs.groupby(["city", "profile_level"], observed=True).size().eq(10).all())
        validate_profile_levels(self.target, self.donor, self.pairs)

    def test_joint_replacement_preserves_other_inputs(self):
        scenario = joint_scenario(self.target, self.donor)
        np.testing.assert_array_equal(scenario[JOINT], self.donor[JOINT])
        np.testing.assert_array_equal(scenario[CONFIG["fixed_variables"]], self.target[CONFIG["fixed_variables"]])
        np.testing.assert_allclose(scenario.FVC, np.clip((scenario.NDVI_mean - .05) / .80, 0, 1) ** 2)

    def test_cross_city_reference_rejected(self):
        donor = self.donor.copy()
        donor.loc[0, "city"] = "Unknown city"
        with self.assertRaises(ValueError):
            joint_scenario(self.target, donor)

    def test_cover_sum_rejected(self):
        donor = self.donor.copy()
        donor.loc[0, ["PLAND_veg", "PLAND_imperv"]] = 1.0
        with self.assertRaises(ValueError):
            joint_scenario(self.target, donor)

    def test_building_incompatibility_rejected(self):
        donor = self.donor.copy()
        target = self.target.copy()
        donor.loc[0, "PLAND_imperv"] = 0.0
        target.loc[0, "Built_surface_fraction"] = 0.5
        with self.assertRaises(ValueError):
            joint_scenario(target, donor)

    def test_summary_and_figure_counts(self):
        self.assertEqual(len(list((ROOT / "data/summary").glob("*.csv"))), 34)
        self.assertEqual(len(list((ROOT / "papers/figures").glob("*.png"))), 15)
        self.assertFalse(list((ROOT / "papers/figures").glob("v7_*")))

    def test_data_definitions_cover_csv_columns(self):
        definitions = (ROOT / "data/VARIABLES.md").read_text()
        for feature in CONFIG["candidate_features"]:
            self.assertIn(f"`{feature}`", definitions)

    def test_sample_source_counts(self):
        provenance = json.loads((ROOT / "data/provenance.json").read_text())
        self.assertEqual(provenance["model_sample"]["source_rows"], 198258)
        self.assertEqual(provenance["greening_sample"]["eligible_source_rows"], 70296)
        self.assertEqual(provenance["greening_sample"]["source_pairs"], 119632)


if __name__ == "__main__":
    unittest.main()
