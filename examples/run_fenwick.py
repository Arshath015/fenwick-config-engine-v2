import pathlib
from engine.config import load_config, EngineRunner

def main():
    cfg_path = pathlib.Path(__file__).parent.parent / "config" / "example_config.yaml"
    config = load_config(cfg_path)
    runner = EngineRunner(config)
    results = runner.run()
    print("Range‑sum results:", results)
    # Persist final state for downstream analysis
    out_file = pathlib.Path(__file__).parent / "results" / "output.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    runner.dump_state(out_file)
    print(f"Full state written to {out_file}")

if __name__ == "__main__":
    main()
