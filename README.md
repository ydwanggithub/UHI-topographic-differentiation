# Topographic differentiation of urban heat island drivers across 41 cities in central China

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.10-blue.svg)](https://www.python.org/)

Companion repository for the manuscript:

> Wang, Y., Zhou, J., Shi, X., Meng, L. **Differential urban heat island drivers along topography reshape green-infrastructure planning across 41 cities in central China.** *Sustainable Cities and Society*, under review.

This repository releases a minimal demonstration package only. It contains:

1. A small stratified sample of the analysis grid.
2. Three short illustrative scripts (data loading, baseline regression, basic plotting) that show the sample schema in use.
3. The rendered manuscript figures.

The manuscript text, the full driver grid, and the analytical pipelines used to produce the published findings are not part of this release.

---

## Contents

```
.
├── README.md
├── LICENSE                  # CC BY 4.0
├── CITATION.cff
├── environment.yml
├── .gitignore
│
├── code/                    # three illustrative scripts
│   ├── demo_load_sample.py
│   ├── demo_baseline_regression.py
│   └── demo_scatter_plot.py
│
├── data/sample/
│   ├── clean_41_smod_sample_n2000.csv
│   └── README.md
│
└── papers/figures/          # rendered manuscript figures (PDF + PNG + SVG)
```

---

## Quick start

```bash
git clone https://github.com/ydwanggithub/UHI-topographic-differentiation.git
cd UHI-topographic-differentiation
conda env create -f environment.yml
conda activate uhi-topo-demo

python code/demo_load_sample.py
python code/demo_baseline_regression.py
python code/demo_scatter_plot.py
```

---

## Citation

```bibtex
@article{wang2026topographic,
  title   = {Differential urban heat island drivers along topography reshape green infrastructure planning across 41 cities in central China},
  author  = {Wang, Yuandong and Zhou, Jiahui and Shi, Xiaowen and Meng, Lihong},
  journal = {Sustainable Cities and Society},
  year    = {2026},
  note    = {Under review}
}
```

---

## License

Code is released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
