# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

"""
Script to scan the input directory for files with pattern "olive_ci_*.py"
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
examples = []
for filepath in dirpath.rglob("olive_ci_*.json"):
    with filepath.open() as strm:
        config = json.load(strm)
        config["path"] = str(filepath)
        config["cwd"] = str(filepath.parent.relative_to(dirpath))

        for key, value in _defaults.items():
            if key not in config:
                config[key] = value

        examples.append(config)

matrix = {"include": examples}
output = json.dumps(matrix)
print(output)
