# Simulation: Gluing Leviathan

Reproducible computation backing every numeric claim in the paper.

## Layout

```
simulation/
├── institutions.py       enumerated institutional state space (P, L, M, C, V, R, K)
├── sheaf.py              cellular sheaf class, restriction maps, cohomology
├── three_settlement.py   the worked A/B/C river-system example used in Section 6
├── attractor_sweep.py    8-attractor fitness model + 4D parameter sweep
├── figures.py            matplotlib figure generation
├── run_all.py            single-command orchestrator
├── pyproject.toml        uv project definition (numpy + matplotlib)
└── output/               generated results.json + figures
```

## Run

```
uv run run_all.py
```

This:

1. Builds the three-settlement sheaf in baseline and under each repair combination, computes $\dim H^{0}$, $\dim H^{1}$, and the integer global-section count for each.
2. Runs an $11^4 = 14{,}641$-cell parameter sweep over (violence intensity, transport security, energy surplus, literacy retention) and records the basin distribution over the eight attractors at every cell.
3. Computes a 1D violence slice at the favourable $(t, e, l) = (0.85, 0.85, 0.85)$ point.
4. Writes `output/results.json` and four PNG figures (three phase diagrams at low/mid/high $(e, l)$ and one violence-slice line plot).

## What each script proves

`three_settlement.py` is the empirical content of Section 6. It is small enough to read as a standalone exposition of the sheaf model.

`attractor_sweep.py` is the empirical content of Section 7. The eight fitness functions are deliberately transparent bumps in the 4D cube; readers can substitute their own and re-run.

`run_all.py` is the only entry point for reproducing the paper. Every numeric claim in `paper/PAPER.md` is sourced from a key under `output/results.json` after running it.

## Cross-checking the paper

The numbers cited in `PAPER.md` should match `output/results.json`:

- $25{,}600$ candidate configurations: `state_space_size`
- per-row entries of the three-settlement table: `three_settlement.<config>`
- basin volumes: `attractor_sweep.basin_volumes`
- scenario shares: `attractor_sweep.scenarios`
- violence slice values: `violence_slice.series.capitalist`

If a paper number drifts from a JSON value, the JSON wins.
