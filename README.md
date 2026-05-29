# Gluing Leviathan

**Title**: Gluing Leviathan — A Local-to-Global Theory of Civilizational Reconstruction
**Date**: May 2026
**Author**: PIATRA . INSTITUTE

## Contents

- [`paper/`](./paper/) — manuscript sources (`PAPER.md`, `project.md`, build scripts)
- [`simulation/`](./simulation/) — cellular sheaf and attractor-dynamics simulation that generates every numeric claim in the paper
- [`chat.md`](./chat.md) — exploratory dialogue from which the paper was distilled

## Origin

No precursor in the current `research/` tree. Initiated from an open-ended conversation about post-collapse institutional reconstruction (`chat.md`) which surfaced the local-to-global compatibility frame and the eight-attractor taxonomy. The paper formalises that frame as a cellular sheaf with computable obstruction class and pairs it with a parameter-sweep dynamical layer.

## Reproducing the numbers in the paper

```
cd simulation
uv run run_all.py
```

This writes `simulation/output/results.json` and the four phase-diagram and violence-slice figures used to support Sections 6–7 of the paper.

## Building the PDF

```
cd paper
bash scripts/build-paper.sh
```

Requires `pandoc` and `xelatex` on the host. The build script reproduces the typography of the other PIATRA papers (Palatino, 11pt, 1in margins, 1.15 line-stretch).
