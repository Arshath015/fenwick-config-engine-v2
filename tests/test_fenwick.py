import pytest
from engine.fenwick import FenwickTree

@pytest.fixture
def sample_tree():
    # Build a tree from known values
    return FenwickTree([1, 2, 3, 4, 5])

def test_prefix_sum(sample_tree):
    assert sample_tree.prefix_sum(0) == 1
    assert sample_tree.prefix_sum(2) == 1 + 2 + 3
    assert sample_tree.prefix_sum(4) == 15

def test_range_sum(sample_tree):
    assert sample_tree.range_sum(1, 3) == 2 + 3 + 4
    assert sample_tree.range_sum(0, 4) == 15
    with pytest.raises(ValueError):
        sample_tree.range_sum(3, 2)  # left > right
    with pytest.raises(IndexError):
        sample_tree.range_sum(-1, 2)  # negative left not allowed

def test_update_and_requery(sample_tree):
    sample_tree.update(2, 5)  # element 3 becomes 8
    assert sample_tree.range_sum(2, 2) == 8
    assert sample_tree.prefix_sum(4) == 1 + 2 + 8 + 4 + 5
