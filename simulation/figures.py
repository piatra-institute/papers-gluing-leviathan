"""Matplotlib figure generation for the paper."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from attractor_sweep import ATTRACTORS  # noqa: E402


_COLORS = [
    "#2b3a55",  # kin_commons    deep blue
    "#8b1a1a",  # warlord        red
    "#6e4b1f",  # neo_feudal     brown
    "#7a5c8c",  # monastic       violet
    "#1f6f4a",  # guild_merchant green
    "#3a3a3a",  # state_command  charcoal
    "#c08a00",  # capitalist     gold
    "#4f8fb0",  # commons_fed    light blue
]


def plot_phase_diagram(
    grid: np.ndarray,
    results: np.ndarray,
    e_idx: int,
    l_idx: int,
    savepath: str,
    title_suffix: str,
) -> None:
    dominant = np.argmax(results[:, :, e_idx, l_idx, :], axis=-1)
    cmap = matplotlib.colors.ListedColormap(_COLORS)
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.imshow(
        dominant.T,
        origin="lower",
        cmap=cmap,
        vmin=0,
        vmax=len(ATTRACTORS) - 1,
        extent=[0, 1, 0, 1],
        aspect="auto",
        interpolation="nearest",
    )
    ax.set_xlabel("Violence intensity (v)")
    ax.set_ylabel("Transport security (t)")
    ax.set_title(
        f"Dominant attractor   |   energy={grid[e_idx]:.2f}, literacy={grid[l_idx]:.2f}"
    )

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=_COLORS[i], label=ATTRACTORS[i])
        for i in range(len(ATTRACTORS))
    ]
    ax.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
        fontsize=9,
    )
    plt.tight_layout()
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(savepath, dpi=140, bbox_inches="tight")
    plt.close(fig)


def plot_violence_slice(slice_data: dict, savepath: str) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    grid = slice_data["_violence_grid"]
    for i, a in enumerate(ATTRACTORS):
        ax.plot(grid, slice_data[a], color=_COLORS[i], label=a, linewidth=2.0)
    ax.set_xlabel("Violence intensity (v)")
    ax.set_ylabel("Basin share")
    ax.set_title(
        "Basin shares as violence rises (transport=0.85, energy=0.85, literacy=0.85)"
    )
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=9)
    plt.tight_layout()
    Path(savepath).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(savepath, dpi=140, bbox_inches="tight")
    plt.close(fig)
