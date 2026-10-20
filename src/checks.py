"""Claim checks: every number quoted in a notebook's written summary is recomputed and asserted."""
from __future__ import annotations

import numpy as np
import pandas as pd


def _plain(value):
    """numpy scalars -> plain Python values, so the Computed column reads cleanly."""
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return type(value)(_plain(v) for v in value)
    if isinstance(value, dict):
        return {_plain(k): _plain(v) for k, v in value.items()}
    if isinstance(value, set):
        return sorted(_plain(v) for v in value)
    return value


class Claims:
    def __init__(self) -> None:
        self.rows = []

    def check(self, claim: str, ok, computed="") -> None:
        self.rows.append({"Claim": claim, "Passed": bool(ok), "Computed": str(_plain(computed))})

    def report(self) -> pd.DataFrame:
        """Return the results table; raise if any claim no longer matches the data."""
        table = pd.DataFrame(self.rows)
        failed = table.loc[~table["Passed"], "Claim"].tolist()
        print(f"{int(table['Passed'].sum())} of {len(table)} claims verified against the data.")
        if failed:
            raise AssertionError("Claims that no longer match the data: " + " | ".join(failed))
        return table
