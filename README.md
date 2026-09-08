# Topography shapes surface urban heat island controls with implications for green infrastructure cooling across 41 cities in central China

**Yuandong Wang, Jiahui Zhou, Yuyao Wang, and Lihong Meng**

Manuscript submitted to *Sustainable Cities and Society*.

Repository version: **2026.09.08**.

This study compares surface urban heat island (SUHI) controls and modeled green infrastructure cooling across 41 cities in central China. Summer Landsat observations for 2020-2025 are expressed relative to each city's rural temperature reference. CatBoost and SHAP describe variation in thermal controls across four regional terrain strata. Joint greening scenarios compare cooling associated with changes in vegetation and accompanying surface cover.

## Contents

| Directory or file | Contents |
| --- | --- |
| `code/` | Executable examples for SUHI calculation, city-held-out CatBoost prediction, SHAP summaries, and joint greening |
| `data/sample/` | Current modeling sample and existing target-reference pairs for the greening example |
| `data/summary/` | The 34 CSV files accompanying the revised Supplementary Material |
| `data/study_config.json` | The 23 candidate variables, 21 model inputs, model parameters, and scenario definitions |
| `data/VARIABLES.md` | Column definitions, units, data sources, and aggregation periods |
| `data/provenance.json` | Sample selection, source hashes, and version information |
| `papers/figures/` | The 15 PNG figures used in the revised manuscript |
| `tests/` | Data, scenario, and repository consistency checks |

The examples use subsets of the revised data. Full-study numerical results are supplied separately in `data/summary/`; the examples illustrate the calculations on the released sample. The complete image collection, full analysis grid, fitted study models, and full processing pipeline are not included in this demonstration release.

## Data and definitions

The modeling sample contains **4,100 cells**, with 100 cells drawn from each of the 41 cities in the revised 198,258-cell modeling dataset. Cell ownership and the original city-level geomorphic assignments are retained. Time-varying inputs summarize 2020-2025; building and terrain products retain their stated observation epochs.

SUHI is calculated as a cell's summer LST minus its city's mean rural reference LST. The reference comprises cells 10-15 km beyond the urban core, with urban core overlap below 1% and impervious and water fractions each below 10%. `rural_reference_lst_k` contains the reference calculated from the full study data. It is not re-estimated from the small demonstration sample. A difference of 1 K is numerically equal to a difference of 1 degree C; absolute Kelvin temperatures are converted to degrees C by subtracting 273.15.

The primary model has **21 inputs**. All 23 candidate columns remain available, including FVC and FAR, whose deterministic definitions are documented in `data/VARIABLES.md`. FAR and FVC are excluded from the primary tree models. City, coordinates, and temperature-reference columns are identifiers or response information, not model predictors.

The greening example uses existing reference pairs from the revised analysis. NDVI, EVI, LAI, vegetation fraction, impervious fraction, impervious edge contrast, and impervious aggregation change together. Terrain, climate, water fraction, and building form remain fixed. The held-out city is excluded from model training. Greening summaries from the small pair sample describe changed cells; the manuscript's urban means also account for unchanged eligible land.

## Run the examples

Use Python 3.11. The pinned dependencies have been tested with the commands below.

```bash
git clone https://github.com/ydwanggithub/UHI-topographic-differentiation.git
cd UHI-topographic-differentiation
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS or Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

python code/demo_load_sample.py
python code/demo_catboost_shap.py --held-out-city Wuhan
python code/demo_joint_greening.py --city Wuhan
python -m unittest discover -s tests -v
```

Alternatively, create the supplied Conda environment with `conda env create -f environment.yml` and activate `uhi-topo-demo`.

To run leave-one-city-out prediction for all 41 cities on the demonstration sample:

```bash
python code/demo_catboost_shap.py --all-cities
```

Outputs are written to `outputs/`. The examples run on a CPU with the study's 450 iterations, depth of 7, learning rate of 0.05, and L2 leaf regularization of 5.0. The study models were trained on the full dataset using a GPU. Sample size and computing backend differ, so demonstration predictions and scores are not the manuscript estimates.

## Summary results and figures

`data/summary/README.md` identifies the populations, reference definitions, and table correspondence for the accompanying CSV files. These CSVs and the 15 manuscript PNGs are byte-identical to the corresponding files in the revised submission. SHA-256 checksums are provided in `data/file_checksums.json`. The previous public files remain available through Git history.

## Citation

Use `CITATION.cff` for the current title and author list. The manuscript remains under review; no journal volume, page range, or article DOI is assigned here.

Wang, Y., Zhou, J., Wang, Y., & Meng, L. (2026). Topography shapes surface urban heat island controls with implications for green infrastructure cooling across 41 cities in central China. Manuscript submitted to *Sustainable Cities and Society*.

## License and contact

Code is distributed under the MIT License. The authors' figures and derived demonstration and summary data are distributed under CC BY 4.0. The original third-party data products retain their respective terms. See `LICENSE`.

Corresponding author: Yuandong Wang, Gannan Normal University, `wangyuandong@gnnu.edu.cn`.
