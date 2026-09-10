import json
from pathlib import Path
from runtime import run
from tools import get_data, validate

BASE=Path(__file__).resolve().parent.parent
if __name__ == "__main__":
    run("email",json.loads((BASE/"config/tool.json").read_text()),get_data,
        json.loads((BASE/"config/output_schema.json").read_text()),validate)
