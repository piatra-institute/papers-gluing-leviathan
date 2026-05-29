"""The three-settlement river system used as the paper's worked example.

A: upstream fortified settlement
B: downstream farming village
C: trading town

Edges:
- AB (river):    must agree on resource rule
- BC (grain):    must agree on money rule
- AC (road):     must agree on violence rule + contract enforcement

Each repair widens specific vertex profiles so that previously incompatible
endpoints share at least one admissible value on the contested dimension.
"""

from copy import deepcopy
from typing import Dict, Iterable, List

from sheaf import CellComplex, Sheaf


PROFILES_BASELINE: Dict[str, dict] = {
    "A": {  # upstream fortified settlement
        "P": ("private_alienable",),
        "L": ("wage", "serf"),
        "M": ("metal_coin",),
        "C": ("court", "armed"),
        "V": ("warlord", "militia"),
        "R": ("private_diversion",),
        "K": ("scribal", "manual"),
    },
    "B": {  # downstream farming village
        "P": ("clan", "commons"),
        "L": ("household", "cooperative"),
        "M": ("grain_ledger", "barter"),
        "C": ("kin_oath", "guild"),
        "V": ("militia", "federated"),
        "R": ("common", "kin_allocated"),
        "K": ("oral",),
    },
    "C": {  # trading town
        "P": ("private_alienable",),
        "L": ("wage",),
        "M": ("metal_coin", "credit"),
        "C": ("court", "guild"),
        "V": ("monopoly", "militia"),
        "R": ("private_diversion", "state_allocation"),
        "K": ("scribal", "manual"),
    },
}

EDGES_BASELINE = [
    ("A", "B", "river"),
    ("B", "C", "grain"),
    ("A", "C", "road"),
]


REPAIRS: Dict[str, Dict[str, Dict[str, tuple]]] = {
    "water_compact": {
        # A and B both admit "common" water on the shared river
        "A": {"R": ("private_diversion", "common")},
        "B": {"R": ("common", "kin_allocated")},
    },
    "exchange_table": {
        # B and C both admit grain ledger AND metal coin at the trade interface
        "B": {"M": ("grain_ledger", "metal_coin")},
        "C": {"M": ("metal_coin", "grain_ledger", "credit")},
    },
    "safe_conduct": {
        # A and C converge on militia + court for the military road
        "A": {"V": ("militia",), "C": ("court",)},
        "C": {"V": ("militia",), "C": ("court",)},
    },
}


def apply_repairs(profiles: Dict[str, dict], names: Iterable[str]) -> Dict[str, dict]:
    out = deepcopy(profiles)
    for name in names:
        for v, dims in REPAIRS[name].items():
            for d, vals in dims.items():
                out[v][d] = vals
    return out


def report(profiles: Dict[str, dict], edges: List[tuple], label: str) -> dict:
    complex = CellComplex(["A", "B", "C"], edges)
    sheaf = Sheaf(complex, profiles)
    H0, H1 = sheaf.cohomology()
    n_glob = len(sheaf.global_sections())
    return {
        "label": label,
        "stalk_sizes": {v: sheaf.stalk_size(v) for v in complex.vertices},
        "edge_stalk_sizes": {
            f"{u}-{w}-{etype}": len(sheaf.edge_stalk((u, w, etype)))
            for (u, w, etype) in edges
        },
        "n_global_sections": n_glob,
        "H0": H0,
        "H1": H1,
        "n_overlap_disagreements": sheaf.n_overlap_disagreements(),
    }
