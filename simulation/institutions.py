"""Finite institutional state space.

Each local region carries a 7-tuple LocalSection drawn from the Cartesian
product of the seven institutional dimensions (property, labor, money,
contract, violence, resource, knowledge). Vertex profiles restrict which
values are admissible in a given region.
"""

from collections import namedtuple
from itertools import product

PROPERTY = ("commons", "clan", "private_alienable", "state")
LABOR = ("household", "wage", "serf", "slave", "cooperative")
MONEY = ("barter", "grain_ledger", "metal_coin", "credit")
CONTRACT = ("kin_oath", "guild", "court", "armed")
VIOLENCE = ("raiding", "warlord", "militia", "monopoly", "federated")
RESOURCE = ("common", "private_diversion", "state_allocation", "kin_allocated")
KNOWLEDGE = ("oral", "scribal", "manual", "school")

DIMENSIONS = ("P", "L", "M", "C", "V", "R", "K")
VALUES = {
    "P": PROPERTY,
    "L": LABOR,
    "M": MONEY,
    "C": CONTRACT,
    "V": VIOLENCE,
    "R": RESOURCE,
    "K": KNOWLEDGE,
}

LocalSection = namedtuple("LocalSection", DIMENSIONS)


def all_sections():
    """Iterate over the full Cartesian product of institutional values."""
    for combo in product(*[VALUES[d] for d in DIMENSIONS]):
        yield LocalSection(*combo)


def total_state_space_size():
    n = 1
    for d in DIMENSIONS:
        n *= len(VALUES[d])
    return n


def local_feasible(section, profile):
    """Filter a section against a per-vertex profile.

    A profile is a dict mapping dimension key -> tuple of admissible values
    in that region. Dimensions absent from the profile are unrestricted.
    """
    for dim, allowed in profile.items():
        if getattr(section, dim) not in allowed:
            return False
    return True


# Restriction selectors for each edge type. The edge stalk is the projection
# of vertex stalks onto the listed dimensions; the agreement constraint
# requires both endpoints to agree on those dimensions.
EDGE_COMPATIBILITY = {
    "river":     ("R",),         # shared water: resource rule must agree
    "grain":     ("M",),         # grain route: money rule must agree
    "road":      ("V", "C"),     # military road: violence + contract enforcement
    "border":    ("P", "L"),     # generic border: property + labor
    "court":     ("C", "M"),     # legal interface: contract + money
    "watershed": ("R", "V"),     # complex resource boundary
}
