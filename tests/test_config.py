import pathlib
import json
import pytest
from engine.config import load_config, EngineRunner

@pytest.fixture
def cfg_path(tmp_path):
    cfg = {
        "size": 5,
        "initial": [0, 0, 0, 0, 0],
        "operations": [
            {"type": "update", "index": 1, "delta": 10},
            {"type": "range_sum", "left": 0, "right": 2},
            {"type": "update", "index": 4, "delta": 3},
            {"type": "range_sum", "left": 1, "right": 4}
        ]
    }
    p = tmp_path / "cfg.yaml"
    p.write_text(json.dumps(cfg))  # using JSON but .yaml extension is allowed
    return p

def test_load_and_run(cfg_path, tmp_path):
    cfg = load_config(cfg_path)
    runner = EngineRunner(cfg)
    results = runner.run()
    assert results == [10, 13]
    out_path = tmp_path / "out.json"
    runner.dump_state(out_path)
    data = json.loads(out_path.read_text())
    assert data["array"] == [0, 10, 0, 0, 3]
    assert data["results"] == [10, 13]
