# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

"""
Script to scan the input directory for files with name "olive_ci.json"
and generate output that can be set as matrix for another CI job.

Example:
    python generate_matrix.py <input directory>
"""
import json
import sys
from pathlib import Path

_defaults = {
    "requirements_file": None,
    "olive_version": "main",
}

dirpath = Path(sys.argv[1])
device = sys.argv[2]

examples = []
for filepath in dirpath.rglob("olive_ci.json"):
    with filepath.open() as strm:
        for config in json.load(strm):
            if config["device"] == device:
                config["name"] = f"{filepath.parent.name} | {config['name']}"
                config["path"] = str(filepath)
                config["cwd"] = str(filepath.parent.relative_to(dirpath))

                for key, value in _defaults.items():
                    if key not in config:
                        config[key] = value

                examples.append(config)

matrix = {"include": examples}
output = json.dumps(matrix)
print(output)
