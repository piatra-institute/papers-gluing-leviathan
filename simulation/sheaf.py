"""Cellular sheaf over a 1-dimensional cell complex (vertices + edges).

Stalks live on cells; restriction maps move from vertex stalks down to
edge stalks via projection onto the dimensions listed in
``EDGE_COMPATIBILITY``. Global sections are enumerated combinatorially.
The cohomology dimensions H^0 and H^1 are computed over R by lifting
each stalk to its indicator vector space and forming the coboundary
operator d: C^0 -> C^1.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from institutions import (
    EDGE_COMPATIBILITY,
    all_sections,
    local_feasible,
)


@dataclass
class CellComplex:
    vertices: List[str]
    edges: List[Tuple[str, str, str]]  # (u, v, edge_type)


class Sheaf:
    def __init__(self, complex: CellComplex, vertex_profiles: Dict[str, dict]):
        self.complex = complex
        self.vertex_profiles = vertex_profiles
        self.stalks: Dict[str, list] = {
            v: [s for s in all_sections() if local_feasible(s, vertex_profiles[v])]
            for v in complex.vertices
        }
        self._edge_stalk_cache: Dict[tuple, list] = {}

    def stalk_size(self, v: str) -> int:
        return len(self.stalks[v])

    def edge_stalk(self, edge: Tuple[str, str, str]) -> list:
        if edge in self._edge_stalk_cache:
            return self._edge_stalk_cache[edge]
        u, v, etype = edge
        dims = EDGE_COMPATIBILITY[etype]
        values = set()
        for s in self.stalks[u] + self.stalks[v]:
            values.add(tuple(getattr(s, d) for d in dims))
        result = sorted(values)
        self._edge_stalk_cache[edge] = result
        return result

    def restriction(self, vertex: str, edge: Tuple[str, str, str]) -> np.ndarray:
        u, v, etype = edge
        assert vertex in (u, v), f"vertex {vertex} not in edge {edge}"
        dims = EDGE_COMPATIBILITY[etype]
        edge_stalk = self.edge_stalk(edge)
        index_of = {tup: i for i, tup in enumerate(edge_stalk)}
        n_e = len(edge_stalk)
        n_v = self.stalk_size(vertex)
        M = np.zeros((n_e, n_v))
        for j, s in enumerate(self.stalks[vertex]):
            tup = tuple(getattr(s, d) for d in dims)
            M[index_of[tup], j] = 1.0
        return M

    def global_sections(self) -> List[Dict[str, object]]:
        """Backtracking enumeration of consistent vertex assignments."""
        verts = self.complex.vertices
        edges = self.complex.edges
        sections: List[Dict[str, object]] = []

        def edge_dims(etype: str) -> tuple:
            return EDGE_COMPATIBILITY[etype]

        def consistent(assignment: dict, v: str, candidate) -> bool:
            for u, w, etype in edges:
                other = None
                if u == v and w in assignment:
                    other = assignment[w]
                elif w == v and u in assignment:
                    other = assignment[u]
                if other is not None:
                    for d in edge_dims(etype):
                        if getattr(candidate, d) != getattr(other, d):
                            return False
            return True

        def backtrack(i: int, assignment: dict):
            if i == len(verts):
                sections.append(dict(assignment))
                return
            v = verts[i]
            for s in self.stalks[v]:
                if not consistent(assignment, v, s):
                    continue
                assignment[v] = s
                backtrack(i + 1, assignment)
                del assignment[v]

        backtrack(0, {})
        return sections

    def coboundary(self) -> np.ndarray:
        """Construct the coboundary d: C^0 -> C^1 as a single block matrix.

        Vertex stalks are concatenated in the order of ``self.complex.vertices``.
        Each row block corresponds to one edge: rows = edge stalk dimension,
        cols = total C^0 dimension. Entry sign is +1 for the second endpoint,
        -1 for the first (giving an oriented coboundary).
        """
        verts = self.complex.vertices
        v_dims = [self.stalk_size(v) for v in verts]
        v_offset, total = {}, 0
        for v, n in zip(verts, v_dims):
            v_offset[v] = total
            total += n

        rows = []
        for edge in self.complex.edges:
            u, w, _ = edge
            R_u = self.restriction(u, edge)
            R_w = self.restriction(w, edge)
            n_e = R_u.shape[0]
            row = np.zeros((n_e, total))
            row[:, v_offset[u]:v_offset[u] + self.stalk_size(u)] = -R_u
            row[:, v_offset[w]:v_offset[w] + self.stalk_size(w)] = R_w
            rows.append(row)

        if not rows:
            return np.zeros((0, total))
        return np.vstack(rows)

    def cohomology(self) -> Tuple[int, int]:
        """Return (dim H^0, dim H^1) over R."""
        d = self.coboundary()
        n_C0 = sum(self.stalk_size(v) for v in self.complex.vertices)
        n_C1 = d.shape[0]
        if d.size == 0:
            return n_C0, 0
        rank = int(np.linalg.matrix_rank(d, tol=1e-9))
        H0 = n_C0 - rank
        H1 = n_C1 - rank
        return H0, H1

    def n_overlap_disagreements(self) -> int:
        """Counts pairs (s_u, s_v) with s_u in F(u), s_v in F(v) that
        disagree on at least one edge dimension. Used as a coarse
        scalar diagnostic alongside H^1."""
        n = 0
        for u, w, etype in self.complex.edges:
            dims = EDGE_COMPATIBILITY[etype]
            for s_u in self.stalks[u]:
                for s_w in self.stalks[w]:
                    if any(getattr(s_u, d) != getattr(s_w, d) for d in dims):
                        n += 1
        return n
