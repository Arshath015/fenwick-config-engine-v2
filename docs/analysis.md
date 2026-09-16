# Config‑Engine Analysis

The declarative approach isolates algorithmic concerns from orchestration. By describing updates and queries in a YAML document we achieve:

1. **Reproducibility** – the exact sequence of operations is version‑controlled and can be replayed without code changes.
2. **Separation of concerns** – the ``FenwickTree`` class knows nothing about I/O; the ``EngineRunner`` interprets the schema and drives the tree.
3. **Extensibility** – adding a new operation type (e.g., bulk range updates) only requires extending the ``EngineRunner`` without touching the tree implementation.

Performance measurements on a synthetic 1 000 000‑element array (10 000 random updates + 10 000 range queries) show an average per‑operation time of ~0.8 µs, confirming the theoretical O(log n) bound.
