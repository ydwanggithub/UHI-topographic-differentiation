# Demonstration samples

All three CSVs were selected from the revised 2020-2025 analysis data. No values were simulated.

| File | Contents |
| --- | --- |
| `model_sample_2020_2025.csv` | 100 cells per city, 4,100 cells in total, sampled from the 198,258-cell modeling dataset |
| `greening_pairs_2020_2025.csv` | Up to 10 existing target-reference pairs per city and scenario, selected from the 119,632 pairs in the revised analysis |
| `greening_cells_2020_2025.csv` | The actual eligible urban cells needed to supply both members of every released pair |

Sampling uses seed 20260908 and retains the original city ownership and four terrain strata. `../provenance.json` records the source hashes, sampling order, and exact exported counts. Cells can participate in more than one greening pair or scenario; `cell_id` is unique in each cell table.

The modeling CSV includes all 23 candidate variables. The 21 primary inputs and their order are defined in `../study_config.json`. The response is `SUHI_strict_mean_K`. Its rural reference is calculated from the full study data and supplied as `rural_reference_lst_k`. The annual LST columns and valid-year counts retain their observed values; a missing annual value remains blank.

In the pair table, `cell_id` is the target cell and `donor_cell_id` is its existing greener reference in the same city. The internal profile names `moderate`, `primary`, and `upper` correspond to S1, S2, and S3. `area_m2` is the target cell area used for averaging. `context_distance` is the distance between standardized context profiles used to select the reference, not a geographic distance in meters.

The examples fit a small demonstration model. Full-study results remain in `../summary/`, including the urban means that account for unchanged eligible land. Column definitions and source products are listed in `../VARIABLES.md`.
