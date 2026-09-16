# fenwick-config-engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

Fast range‑sum queries via a config‑first Fenwick Tree engine.

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Theoretical Background](#theoretical-background)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Analysis Document](#analysis-document)
- [Testing](#testing)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

## Overview

This submodule provides a tiny engine that builds a Fenwick (Binary Indexed) Tree from a declarative YAML/JSON configuration. The engine executes a series of *update* and *range_sum* commands, collects results, and can dump the final state to disk.

## Tech Stack

- Python 3.9+
- Standard library (`json`, `pathlib`, `typing`)
- **PyYAML** for YAML parsing
- **pytest** for testing

## Architecture

```text
fenwick-config-engine/
├─ engine/
│  ├─ __init__.py          # public exports
│  ├─ fenwick.py           # core BIT implementation
│  └─ config.py            # config loader & runner
├─ config/
│  └─ example_config.yaml # sample declarative run description
├─ tests/
│  ├─ test_fenwick.py     # unit tests for FenwickTree
│  └─ test_config.py      # integration tests for EngineRunner
├─ examples/
│  └─ run_fenwick.py      # runnable demo, writes results/output.json
├─ docs/
│  └─ analysis.md         # internal analysis of the config‑driven approach
└─ README.md               # this document
```

## Theoretical Background

The Fenwick Tree (or Binary Indexed Tree) is a data structure that stores prefix sums in a compact form. Each node at index *i* (1‑based) aggregates the sum of a range of length ``i & -i`` ending at *i*. This property enables both point updates and prefix‑sum queries in logarithmic time because the algorithm traverses only the set bits of the index.

For a range sum ``[l, r]`` we compute ``prefix_sum(r) - prefix_sum(l‑1)``. The construction from an initial array can be performed in linear time by iteratively adding each element to its parent using the same ``i + (i & -i)`` rule.

The config‑driven engine does not alter these complexities; it merely externalises the sequence of operations. This makes benchmarking, reproducibility, and dynamic workflow composition trivial – the same binary can run entirely different workloads simply by swapping the YAML file.

## Installation

```bash
git clone https://github.com/yourorg/fenwick-config-engine.git
cd fenwick-config-engine
pip install -r requirements.txt
```

*There is no published PyPI package; the repository is intended for internal consumption.*

## Usage

```bash
python examples/run_fenwick.py
```

The script loads ``config/example_config.yaml``, runs the defined operations, prints the range‑sum results and writes the final array plus results to ``examples/results/output.json``.

## API Reference

### class engine.fenwick.FenwickTree
- ``__init__(data: Iterable[int] | None = None)`` – optional initial values.
- ``build(values: List[int])`` – O(n) construction.
- ``update(index: int, delta: int)`` – add *delta* at *index*.
- ``prefix_sum(index: int) -> int`` – sum of ``[0, index]``.
- ``range_sum(left: int, right: int) -> int`` – inclusive range sum.
- ``to_list() -> List[int]`` – reconstruct underlying array.

### class engine.config.EngineRunner
- ``__init__(config: dict)`` – validates and builds a FenwickTree.
- ``run() -> List[int]`` – execute configured operations, returning all ``range_sum`` results.
- ``dump_state(path: str | Path)`` – write ``{"array": [...], "results": [...]}`` JSON.

## Analysis Document

See the in‑repo analysis at [docs/analysis.md](docs/analysis.md).

## Testing

```bash
pytest -q
```

The test suite covers core tree operations, edge‑case error handling, and full engine integration.

## Limitations

- The engine only supports integer values; floating‑point accumulation is not guaranteed to be exact.
- No bulk or lazy range‑update operations are implemented.
- Configuration schema is fixed; extending it requires code changes.

## Roadmap

- Add support for ``range_add`` via a Fenwick variant (dual BIT).
- Validate config against a JSON‑Schema file for stricter user feedback.
- Provide a CLI wrapper (argparse) to select config files at runtime.

## License

MIT License
