"""Shared chart style for the notebooks: one palette, recessive axes, figures saved to reports/figures."""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

# Colour roles (validated categorical slots 1-2; blue/red as the profit/loss pair)
SALES = "#2a78d6"      # series 1 / single-series colour
PROFIT = "#eb6834"     # series 2
GAIN = "#2a78d6"       # positive values
LOSS = "#e34948"       # negative values
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SEQUENTIAL = LinearSegmentedColormap.from_list("blue_seq", BLUE_RAMP)
DIVERGING = LinearSegmentedColormap.from_list("red_gray_blue", ["#b8302f", LOSS, "#f0efec", "#3987e5", "#184f95"])


def apply_style() -> None:
    mpl.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK_2,
        "axes.titlecolor": INK, "axes.titlesize": 12, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 10, "axes.labelsize": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-",
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK_2, "ytick.labelcolor": INK_2,
        "xtick.labelsize": 9, "ytick.labelsize": 9,
        "legend.frameon": False, "legend.fontsize": 9, "legend.labelcolor": INK_2,
        "lines.linewidth": 2, "lines.solid_capstyle": "round",
        "font.family": "sans-serif", "figure.dpi": 100, "savefig.dpi": 150, "savefig.bbox": "tight",
        "text.parse_math": False,   # "$" in labels is a currency sign, not a math delimiter
    })


def money(v: float, decimals: int = 0) -> str:
    """$1.2M / $350K / $42 style labels; negative values keep their sign."""
    sign = "-" if v < 0 else ""
    v = abs(v)
    if v >= 1e6:
        return f"{sign}${v / 1e6:.{max(decimals, 1)}f}M"
    if v >= 1e3:
        return f"{sign}${v / 1e3:.{decimals}f}K"
    return f"{sign}${v:.{decimals}f}"


money_axis = FuncFormatter(lambda v, _: money(v))
pct_axis = FuncFormatter(lambda v, _: f"{v:g}%")


def value_grid_only(ax, axis: str = "y") -> None:
    """Keep gridlines on the value axis only."""
    ax.grid(False)
    ax.grid(True, axis=axis)
    ax.set_axisbelow(True)


def save(fig, name: str, folder: str | Path) -> Path:
    """Save a figure as PNG in reports/figures and return its path."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.png"
    fig.savefig(path)
    return path
