"""Macro-attractor dynamics layer.

Each candidate macro-order is scored against four parameters describing
the post-collapse environment:

- v: violence intensity (0 = pacified, 1 = predation everywhere)
- t: transport security (0 = no safe routes, 1 = secure trade)
- e: energy / surplus (0 = subsistence, 1 = abundant)
- l: literacy retention (0 = oral only, 1 = full scribal infrastructure)

The fitness functions are deliberately transparent. Each attractor has a
peak in some region of [0,1]^4 and decays elsewhere. The basin of an
attractor at a given parameter point is its share of the Boltzmann
distribution over the eight fitnesses with inverse temperature beta.
The dominant attractor at a point is argmax of the basin. Volumes
reported by ``aggregate_basin_volume`` are simply the fraction of the
4D parameter grid that each attractor wins.
"""

from typing import Dict, List, Tuple

import numpy as np


ATTRACTORS: Tuple[str, ...] = (
    "kin_commons",
    "warlord_tribute",
    "neo_feudal",
    "monastic",
    "guild_merchant",
    "state_command",
    "capitalist",
    "commons_federation",
)


def _peak(x: float, center: float, width: float = 0.35) -> float:
    """Smooth bump centered at ``center`` with given half-width."""
    z = (x - center) / width
    return float(np.exp(-z * z))


def fitness(attractor: str, v: float, t: float, e: float, l: float) -> float:
    if attractor == "kin_commons":
        # small scale, no predation, no surplus, no literacy needed
        return _peak(v, 0.1) * _peak(t, 0.1) * _peak(e, 0.2) * _peak(l, 0.1)
    if attractor == "warlord_tribute":
        # predation high, transport poor, literacy low
        return _peak(v, 0.85) * _peak(t, 0.15) * _peak(e, 0.4) * _peak(l, 0.15)
    if attractor == "neo_feudal":
        # mid-high violence, low transport, agrarian, mid literacy
        return _peak(v, 0.65) * _peak(t, 0.25) * _peak(e, 0.4) * _peak(l, 0.4)
    if attractor == "monastic":
        # mid violence, mid transport, mid surplus, high literacy
        return _peak(v, 0.4) * _peak(t, 0.45) * _peak(e, 0.45) * _peak(l, 0.85)
    if attractor == "guild_merchant":
        # low violence, high transport, mid-high surplus, high literacy
        return _peak(v, 0.2) * _peak(t, 0.85) * _peak(e, 0.65) * _peak(l, 0.8)
    if attractor == "state_command":
        # monopolised violence (high but ordered), high transport, mid surplus, high literacy
        return _peak(v, 0.55) * _peak(t, 0.75) * _peak(e, 0.55) * _peak(l, 0.85)
    if attractor == "capitalist":
        # low violence, high transport, high surplus, high literacy
        return _peak(v, 0.15) * _peak(t, 0.9) * _peak(e, 0.9) * _peak(l, 0.9)
    if attractor == "commons_federation":
        # low violence, mid transport, mid surplus, high literacy
        return _peak(v, 0.2) * _peak(t, 0.5) * _peak(e, 0.5) * _peak(l, 0.8)
    raise ValueError(f"unknown attractor {attractor}")


def basin_fractions(v: float, t: float, e: float, l: float, beta: float = 12.0) -> np.ndarray:
    fits = np.array([fitness(a, v, t, e, l) for a in ATTRACTORS])
    weights = np.exp(beta * fits)
    return weights / weights.sum()


def sweep(grid_size: int = 11) -> Tuple[np.ndarray, np.ndarray]:
    grid = np.linspace(0.0, 1.0, grid_size)
    out = np.zeros((grid_size, grid_size, grid_size, grid_size, len(ATTRACTORS)))
    for i, v in enumerate(grid):
        for j, t in enumerate(grid):
            for k, e in enumerate(grid):
                for m, l in enumerate(grid):
                    out[i, j, k, m] = basin_fractions(v, t, e, l)
    return grid, out


def aggregate_basin_volume(results: np.ndarray) -> np.ndarray:
    """Fraction of the 4D parameter grid won by each attractor."""
    dominant = np.argmax(results, axis=-1)
    n_cells = dominant.size
    vols = np.zeros(len(ATTRACTORS))
    for a in range(len(ATTRACTORS)):
        vols[a] = float(np.sum(dominant == a)) / n_cells
    return vols


def basin_volumes_at_beta(beta: float, grid_size: int = 11) -> np.ndarray:
    """Aggregate basin volumes over the 4D grid at a given inverse temperature.
    Used to substantiate the robustness-of-basin-geometry claim in the paper."""
    grid = np.linspace(0.0, 1.0, grid_size)
    out = np.zeros((grid_size, grid_size, grid_size, grid_size, len(ATTRACTORS)))
    for i, v in enumerate(grid):
        for j, t in enumerate(grid):
            for k, e in enumerate(grid):
                for m, l in enumerate(grid):
                    out[i, j, k, m] = basin_fractions(v, t, e, l, beta)
    return aggregate_basin_volume(out)


def slice_violence_effect(grid_size: int = 21) -> Dict[str, List[float]]:
    """Hold (transport, energy, literacy) fixed at favourable capitalist
    values; sweep violence from 0 to 1 and report each attractor's basin
    share. Used in the paper's Proposition 3."""
    grid = np.linspace(0.0, 1.0, grid_size)
    out: Dict[str, List[float]] = {a: [] for a in ATTRACTORS}
    for v in grid:
        b = basin_fractions(v, 0.85, 0.85, 0.85)
        for a, val in zip(ATTRACTORS, b):
            out[a].append(float(val))
    out["_violence_grid"] = list(grid)
    return out
