"""Config‑driven runner for the Fenwick engine.

The configuration schema is deliberately tiny but expressive:

```yaml
size: 10                     # length of the array (filled with zeros)
initial: [1, 2, 3]           # optional list of initial values (size must match)
operations:
  - type: update
    index: 4
    delta: 7
  - type: range_sum
    left: 2
    right: 6
```

The runner parses the file, builds a ``FenwickTree`` and executes the
operations in order, collecting results for ``range_sum`` calls.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List

import yaml

from .fenwick import FenwickTree


def load_config(path: str | pathlib.Path) -> Dict[str, Any]:
    """Load a YAML or JSON config file.

    The function infers the format from the file extension. It raises ``
    ValueError`` if the file cannot be parsed.
    """
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Config file {p} does not exist")
    try:
        if p.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(p.read_text()) or {}
        if p.suffix.lower() == ".json":
            return json.loads(p.read_text())
    except Exception as exc:
        raise ValueError(f"Failed to parse config {p}: {exc}") from exc
    raise ValueError("Unsupported config file type: {p.suffix}")


class EngineRunner:
    """Execute a config‑driven Fenwick workflow.

    Attributes
    ----------
    config: dict
        Normalised configuration dictionary.
    tree: FenwickTree
        The underlying data structure.
    results: List[int]
        Collected outputs of ``range_sum`` operations, in execution order.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._validate()
        size = config["size"]
        initial = config.get("initial", [0] * size)
        if len(initial) != size:
            raise ValueError("Length of 'initial' must equal 'size'")
        self.tree = FenwickTree(initial)
        self.results: List[int] = []

    # ---------------------------------------------------------------------
    def _validate(self) -> None:
        if "size" not in self.config:
            raise ValueError("Config missing required key 'size'")
        ops = self.config.get("operations", [])
        if not isinstance(ops, list):
            raise ValueError("'operations' must be a list")
        for op in ops:
            if not isinstance(op, dict) or "type" not in op:
                raise ValueError("Each operation must be a dict with a 'type' field")

    # ---------------------------------------------------------------------
    def run(self) -> List[int]:
        """Execute all operations and return collected ``range_sum`` results."""
        for op in self.config.get("operations", []):
            typ = op["type"]
            if typ == "update":
                self.tree.update(op["index"], op["delta"])
            elif typ == "range_sum":
                res = self.tree.range_sum(op["left"], op["right"])
                self.results.append(res)
            else:
                raise ValueError(f"Unsupported operation type: {typ}")
        return self.results

    def dump_state(self, path: str | pathlib.Path) -> None:
        """Write the current array and results to *path* as JSON.

        The output format is ``{"array": [...], "results": [...]}``.
        """
        out = {"array": self.tree.to_list(), "results": self.results}
        pathlib.Path(path).write_text(json.dumps(out, indent=2))
