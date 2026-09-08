"""Check the revised sample and reconstruct its rural-reference SUHI."""

import numpy as np

from study import CONFIG, FEATURES, TARGET, load_sample, verify_release_files


def main() -> None:
    frame = load_sample()
    computed = frame.LST_K - frame.rural_reference_lst_k
    np.testing.assert_allclose(computed, frame[TARGET], atol=1e-10, rtol=0)
    verified = verify_release_files()
    print(f"Period: {CONFIG['period']}")
    print(f"Sample: {len(frame):,} cells, {frame.city.nunique()} cities")
    print(f"Candidate variables: {len(CONFIG['candidate_features'])}; model inputs: {len(FEATURES)}")
    print(f"Maximum SUHI reconstruction difference: {abs(computed - frame[TARGET]).max():.3g} K")
    print(frame.groupby('stratum', observed=True).agg(cities=('city', 'nunique'), cells=('cell_id', 'size')).to_string())
    print(f"Verified {verified} released data and figure checksums.")


if __name__ == "__main__":
    main()
