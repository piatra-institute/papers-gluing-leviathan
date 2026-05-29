"""Reproducible orchestration of all simulation outputs cited in the paper.

Writes ``output/results.json`` and the figure files under ``output/``. Every
numeric claim in the paper should be traceable to a key in the JSON file.

Run with:

    cd simulation
    uv run run_all.py
"""

import json
from pathlib import Path

from attractor_sweep import (
    ATTRACTORS,
    aggregate_basin_volume,
    basin_fractions,
    basin_volumes_at_beta,
    slice_violence_effect,
    sweep,
)
from figures import plot_phase_diagram, plot_violence_slice
from institutions import total_state_space_size
from three_settlement import (
    EDGES_BASELINE,
    PROFILES_BASELINE,
    apply_repairs,
    report,
)


OUT = Path(__file__).parent / "output"


def fmt_basin(arr) -> dict:
    return {a: float(v) for a, v in zip(ATTRACTORS, arr)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    results: dict = {
        "state_space_size": total_state_space_size(),
    }

    # ------------------------------------------------------------------
    # Three-settlement worked example
    # ------------------------------------------------------------------
    results["three_settlement"] = {}
    results["three_settlement"]["baseline"] = report(
        PROFILES_BASELINE, EDGES_BASELINE, "baseline"
    )
    for r in ("water_compact", "exchange_table", "safe_conduct"):
        profiles = apply_repairs(PROFILES_BASELINE, [r])
        results["three_settlement"][r] = report(profiles, EDGES_BASELINE, r)

    # Pairs of repairs
    pair_combos = [
        ("water_compact", "exchange_table"),
        ("water_compact", "safe_conduct"),
        ("exchange_table", "safe_conduct"),
    ]
    for combo in pair_combos:
        profiles = apply_repairs(PROFILES_BASELINE, combo)
        key = "+".join(combo)
        results["three_settlement"][key] = report(profiles, EDGES_BASELINE, key)

    # All three repairs
    profiles = apply_repairs(
        PROFILES_BASELINE, ("water_compact", "exchange_table", "safe_conduct")
    )
    results["three_settlement"]["all_repairs"] = report(
        profiles, EDGES_BASELINE, "all_repairs"
    )

    # ------------------------------------------------------------------
    # Attractor parameter sweep
    # ------------------------------------------------------------------
    grid_size = 11
    grid, sweep_results = sweep(grid_size=grid_size)
    vols = aggregate_basin_volume(sweep_results)
    results["attractor_sweep"] = {
        "grid_size": grid_size,
        "n_cells": grid_size ** 4,
        "basin_volumes": fmt_basin(vols),
    }

    # Robustness of the basin geometry to the Boltzmann sharpness beta
    results["beta_robustness"] = {
        f"beta_{int(b)}": fmt_basin(basin_volumes_at_beta(b, grid_size))
        for b in (5.0, 12.0, 20.0)
    }

    # Selected scenario points (chosen to illustrate the propositions)
    scenarios = {
        "low_v_high_t_high_e_high_l": (0.1, 0.9, 0.9, 0.9),
        "high_v_low_t_low_e_low_l":   (0.9, 0.1, 0.1, 0.1),
        "mid_v_mid_t_mid_e_high_l":   (0.5, 0.5, 0.5, 0.9),
        "low_v_low_t_low_e_low_l":    (0.1, 0.1, 0.1, 0.1),
        "low_v_mid_t_mid_e_high_l":   (0.1, 0.5, 0.5, 0.9),
        "mid_v_high_t_mid_e_high_l":  (0.5, 0.9, 0.5, 0.9),
        "high_v_low_t_mid_e_mid_l":   (0.85, 0.15, 0.4, 0.4),
    }
    results["attractor_sweep"]["scenarios"] = {
        k: fmt_basin(basin_fractions(*pt)) for k, pt in scenarios.items()
    }

    # Violence slice (Proposition 3)
    violence_slice = slice_violence_effect(grid_size=21)
    # Drop the inner _violence_grid for a tidier JSON serialization
    grid_axis = violence_slice.pop("_violence_grid")
    results["violence_slice"] = {
        "grid": grid_axis,
        "fixed": {"transport": 0.85, "energy": 0.85, "literacy": 0.85},
        "series": violence_slice,
    }
    # Restore for figure generation
    violence_slice["_violence_grid"] = grid_axis

    # ------------------------------------------------------------------
    # Figures
    # ------------------------------------------------------------------
    plot_phase_diagram(
        grid, sweep_results, e_idx=8, l_idx=8,
        savepath=str(OUT / "phase_diagram_high_e_high_l.png"),
        title_suffix="high energy, high literacy",
    )
    plot_phase_diagram(
        grid, sweep_results, e_idx=5, l_idx=5,
        savepath=str(OUT / "phase_diagram_mid_e_mid_l.png"),
        title_suffix="mid energy, mid literacy",
    )
    plot_phase_diagram(
        grid, sweep_results, e_idx=2, l_idx=2,
        savepath=str(OUT / "phase_diagram_low_e_low_l.png"),
        title_suffix="low energy, low literacy",
    )
    plot_violence_slice(violence_slice, savepath=str(OUT / "violence_slice.png"))

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    with (OUT / "results.json").open("w") as f:
        json.dump(results, f, indent=2)

    # Console summary
    print(f"State-space size: {results['state_space_size']}")
    print()
    print("Three-settlement results:")
    for label, r in results["three_settlement"].items():
        print(
            f"  {label:>40s}  "
            f"H0={r['H0']:>3d}  H1={r['H1']:>3d}  "
            f"#sections={r['n_global_sections']:>4d}  "
            f"#disagreements={r['n_overlap_disagreements']:>5d}"
        )
    print()
    print("Attractor basin volumes (fraction of 4D parameter grid):")
    for a, v in results["attractor_sweep"]["basin_volumes"].items():
        print(f"  {a:>22s}  {v:.3f}")
    print()
    print(f"Wrote: {OUT / 'results.json'}")


if __name__ == "__main__":
    main()
