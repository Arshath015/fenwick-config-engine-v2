"""Fenwick (Binary Indexed) Tree implementation.

Provides O(log n) point updates and prefix‑sum queries, and O(log n) range sum
via prefix differences. The class is deliberately lightweight – it does not
depend on any external library and stores the internal BIT as a list of
integers.
"""

from __future__ import annotations

from typing import List, Iterable


class FenwickTree:
    """Binary Indexed Tree supporting point updates and prefix sums.

    Parameters
    ----------
    data: Iterable[int] | None
        Optional initial sequence. If omitted the tree is created with size 0
        and can be expanded later via ``build``.
    """

    def __init__(self, data: Iterable[int] | None = None) -> None:
        self._size: int = 0
        self._tree: List[int] = []
        if data is not None:
            self.build(list(data))

    # ---------------------------------------------------------------------
    # Construction helpers
    # ---------------------------------------------------------------------
    def build(self, values: List[int]) -> None:
        """Build the BIT from a list of values in O(n).

        The internal array uses 1‑based indexing; index 0 is unused.
        """
        self._size = len(values)
        self._tree = [0] * (self._size + 1)
        for idx, val in enumerate(values, start=1):
            self._tree[idx] += val
            parent = idx + (idx & -idx)
            if parent <= self._size:
                self._tree[parent] += self._tree[idx]

    # ---------------------------------------------------------------------
    # Core operations
    # ---------------------------------------------------------------------
    def update(self, index: int, delta: int) -> None:
        """Add *delta* to element at *index* (0‑based).

        Raises
        ------
        IndexError
            If *index* is out of bounds.
        """
        if not 0 <= index < self._size:
            raise IndexError("FenwickTree.update index out of range")
        i = index + 1
        while i <= self._size:
            self._tree[i] += delta
            i += i & -i

    def prefix_sum(self, index: int) -> int:
        """Return sum of elements ``[0, index]`` inclusive (0‑based).

        If *index* < 0 the result is 0, matching typical mathematical convention.
        """
        if index < 0:
            return 0
        if index >= self._size:
            index = self._size - 1
        i = index + 1
        result = 0
        while i > 0:
            result += self._tree[i]
            i -= i & -i
        return result

    def range_sum(self, left: int, right: int) -> int:
        """Return sum of ``[left, right]`` inclusive.

        The method validates the interval and raises ``ValueError`` when the
        interval is ill‑formed (``left > right`` or out of bounds).
        """
        if left > right:
            raise ValueError("left index must not exceed right index")
        if left < 0 or right >= self._size:
            raise IndexError("range_sum indices out of bounds")
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

    # ---------------------------------------------------------------------
    # Utility helpers
    # ---------------------------------------------------------------------
    def to_list(self) -> List[int]:
        """Return the current underlying array reconstructed from the BIT."""
        return [self.range_sum(i, i) for i in range(self._size)]

    def __len__(self) -> int:
        return self._size
