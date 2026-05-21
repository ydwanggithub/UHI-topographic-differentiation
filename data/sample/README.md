# Sample data

`clean_41_smod_sample_n2000.csv` is a 2,000-cell stratified sample (500 cells per topographic stratum) drawn from a much larger analysis grid (~1.19 million cells at 250 m resolution across 41 cities in central China).

The sample preserves the column schema of the full database (36 columns covering LST, climate, vegetation, urban form, and topographic drivers) and is intended **only for demonstration that the example scripts in `code/` execute end-to-end on the published column schema**, not for statistical reanalysis.

## Column groups

- Identification: `city_name`, `province`, `stratum`, `lon`, `lat`
- Thermal: `LST_K`
- Climate: `Tair_mean`, `Tmax`, `VPD`, `Precip`, `Solar`
- Surface vegetation: `NDVI`, `EVI`, `FVC`, `LAI`
- Urban 2D: `PLAND_imperv`, `pct_water`, `pct_veg`, `ED`, `AIisa`
- Urban 3D: `BldH`, `BVD`, `FAR`, `SVF`
- Topographic: `DEM`, `Slope`, `Aspect`, `TRI`, `RelDEM`

Stratum labels: `Flat`, `Transitional`, `Hilly`, `Mountainous`.

## Access to the full data

The full driver grid is not included in this repository. For collaboration or access requests, contact the corresponding author of the associated manuscript.
