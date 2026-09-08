SCSI-D-26-06097 supplementary data

The 34 CSV files accompany Supplementary_Material.pdf.
Column definitions follow Supplementary Sections S1-S5.

Spatial summaries
Unique ROI: temperature-valid cells after each shared physical site is assigned to one city.
Full ROI: the complete buffered city region before assigning shared sites; adjacent city regions can overlap.
Urban core: city-assigned core cells. Rural references retain their complete-ROI definitions.

City_sample_and_reference_counts.csv
- Table S3: unique_roi_cells, urban_cells, strict_rural_cells, valid_six_year_cells and clear_observations_median.
- Table S4: unique_roi_dem_mean_m, unique_roi_slope_mean_deg and unique_roi_lst_mean_c describe the unique ROI.
  urban_mean_dem_m and urban_mean_lst_k describe the assigned urban core; strict_rural_mean_dem_m and rural_strict_mean_lst_k describe the primary rural reference.
  Subtract 273.15 from Kelvin temperature columns to reproduce degrees C.
- Table S6: use stratum and unique_roi_lst_mean_c for the 41 city temperatures, with the exact two-sided Mann-Whitney test and Holm adjustment across all six comparisons.
- full_roi_total_cells, full_roi_quality_valid_cells and full_roi_lst_mean_c retain the complete-ROI summaries.
  valid_*_year_cells and clear_observations_* also describe temperature-valid cells in the full ROI; they do not have the same population as unique_roi_cells.
- The five city_suhi_* values use the assigned urban core and the corresponding rural reference.

City_temperature_product_comparisons.csv
- Table S10 uses the 41 complete-ROI means in full_roi_landsat_c, full_roi_modis_day_c, full_roi_modis_night_c and full_roi_air_temperature_c.
  Correlations are Pearson correlations across cities. Mean differences are Landsat minus the comparison product.
  These descriptive product comparisons retain their original full-ROI scope; the unique-ROI LST column for Tables S4 and S6 is in City_sample_and_reference_counts.csv.
- Columns ending in _k are in Kelvin; columns ending in _c are in degrees C.

Other city-level files
Annual_LST_coverage.csv describes available annual LST observations in full city ROIs.
City_SUHI_reference_comparisons.csv reports assigned-core contrasts under the five rural references (Tables S5-S9).
Within_city_elevation_LST_correlations.csv uses unique city ROIs.

Other notes
The canonical primary terrain contrast uses one city-bootstrap realization wherever the same result is repeated; independent model comparison outputs retain their original bootstrap draws.
Blank rho values are inapplicable to ordinary least squares.
checksums.json records SHA-256 hashes of every CSV file.
