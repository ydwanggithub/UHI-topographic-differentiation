# Variables in the released samples

## Identifiers and temperature

| Column | Definition | Unit |
| --- | --- | --- |
| `cell_id` | Study grid identifier retained from the revised data | identifier |
| `city`, `province` | City ownership and province | text |
| `stratum` | Original city-level regional geomorphic group | Flat, Transitional, Hilly, Mountainous |
| `lon`, `lat` | Cell-center longitude and latitude | decimal degrees |
| `LST_K` | Mean of available annual summer LST medians, 2020-2025 | K |
| `LST_2020_K` to `LST_2025_K` | Annual summer LST medians | K |
| `LST_valid_years` | Number of valid annual summer LST values | count |
| `LST_obs_count` | Valid Landsat observation count retained by the extraction | count |
| `rural_reference_lst_k` | Full-data mean LST in the primary rural reference of the assigned city | K |
| `SUHI_strict_mean_K` | Cell LST minus the assigned city's primary rural mean LST | K difference |
| `retained_urban_core` | Urban core membership in the revised data | Boolean |
| `Built_surface_fraction` | GHSL 2020 built surface area divided by grid-cell area | fraction |

LST is obtained from quality-screened Landsat 8 and 9 Collection 2 Level 2 surface temperature. Summer refers to June-August. The modeling sample contains complete predictor observations and at least four valid summer LST values. Missing annual temperatures remain blank. Kelvin temperature differences and degrees C differences have identical numerical magnitudes.

## Candidate variables

| CSV column | Manuscript symbol | Definition | Unit | Source and period |
| --- | --- | --- | --- | --- |
| `Tair_mean` | Tair | Mean 2 m air temperature | degrees C | ERA5-Land, mean of annual summer means, 2020-2025 |
| `Tair_max` | Tmax | Mean monthly maximum 2 m air temperature | degrees C | ERA5-Land, summer mean of monthly maxima, 2020-2025 |
| `Precip_annual` | Precip | Mean annual precipitation | mm/year | ERA5-Land, mean of annual totals, 2020-2025 |
| `VPD_summer` | VPD | Vapor pressure deficit | kPa | ERA5-Land, mean of annual summer means, 2020-2025 |
| `Solar_RAD` | Solar | Downward shortwave radiation | W/m2 | ERA5-Land, mean of annual summer means, 2020-2025 |
| `NDVI_mean` | NDVI | Normalized difference vegetation index | index | Sentinel-2 surface reflectance, mean of annual summer medians, 2020-2025 |
| `EVI_mean` | EVI | Enhanced vegetation index | index | Sentinel-2 surface reflectance, mean of annual summer medians, 2020-2025 |
| `FVC` | FVC | Fractional vegetation cover derived from NDVI | fraction | Squared rescaling of NDVI |
| `LAI` | LAI | Leaf area index | m2/m2 | MODIS MOD15A2H V6.1, mean of annual summer means, 2020-2025 |
| `PLAND_imperv` | ISA | Impervious surface fraction | fraction | Dynamic World V1, mean of annual built probabilities, 2020-2025 |
| `PLAND_water` | %Water | Water fraction | fraction | Dynamic World V1, mean of annual summer water probabilities, 2020-2025 |
| `PLAND_veg` | %Veg | Vegetation fraction | fraction | Dynamic World V1, mean of annual summer vegetation probabilities, 2020-2025 |
| `ED_total` | ED | Impervious edge contrast proxy | index | Sobel contrast of the Dynamic World mean built probability field |
| `AI_imperv` | AIisa | Impervious aggregation proxy | index | Local mean built probability from Dynamic World |
| `Mean_Bld_Height` | BldH | Mean building height | m | GHSL building height, 2018 |
| `Bld_Volume_density` | BVD | Building volume per unit land area | m3/m2 | GHSL 2018 height multiplied by 2020 built surface fraction |
| `FAR` | FAR | Floor area ratio proxy | ratio | BVD divided by a 3 m floor height |
| `Sky_View_Factor` | SVF | Empirical sky view factor proxy | ratio | GHSL height and built surface fraction |
| `DEM` | DEM | Elevation above sea level | m | ALOS AW3D30 V4.1, PRISM observations from 2006-2011 |
| `Slope` | Slope | Local slope | degrees | ALOS AW3D30 |
| `Aspect` | Aspect | Circular mean slope aspect | degrees | ALOS AW3D30 |
| `TRI` | TRI | Elevation standard deviation in a 3 by 3 neighborhood of the native grid | m | ALOS AW3D30 |
| `Relative_elevation` | RelDEM | Cell elevation minus the surrounding 5 km mean | m | ALOS AW3D30 |

All cover fractions range from 0 to 1, including the columns whose manuscript symbols contain `%`. `AI_imperv` denotes the impervious aggregation proxy. The response, annual LST, rural reference, coordinates, and city labels do not enter the predictor matrix.

The primary tree models omit `FAR = Bld_Volume_density / 3` and `FVC = clip((NDVI_mean - 0.05) / 0.80, 0, 1)^2`. Both derived columns are preserved so the 23-candidate data definitions remain explicit.

## Joint greening pairs

| Column | Definition |
| --- | --- |
| `cell_id` | Target urban cell |
| `donor_cell_id` | Observed greener reference cell in the same city |
| `profile_level` | Existing scenario profile, mapped to S1-S3 in `study_config.json` |
| `context_distance` | Distance in standardized environmental context space |
| `area_m2` | Area of the target grid cell in square meters |

S1, S2, and S3 require NDVI increases of 0.10-0.20, 0.20-0.30, and 0.30-0.45, respectively. Minimum vegetation-fraction increases and impervious-fraction decreases are 0.10, 0.15, and 0.20; LAI does not decrease. The target's water fraction plus reference vegetation and impervious fractions remains at or below 1.02. Reference impervious fraction plus the 0.05 tolerance is at least the target's retained building fraction.

The seven substituted columns are `NDVI_mean`, `EVI_mean`, `LAI`, `PLAND_veg`, `PLAND_imperv`, `ED_total`, and `AI_imperv`. Remaining primary model inputs stay fixed. FVC is recalculated from scenario NDVI, and FAR remains determined by the unchanged BVD.
