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

dirpath = sys.argv[1]
examples = []
for filepath in Path(dirpath).rglob("olive_ci_*.json"):
    name = str(filepath.parent) + "/" + str(filepath.name)[len("olive_ci_"):-len(".json")]
    examples.append({ "name": name, "config": str(filepath), "runs-on": "ubuntu-latest" })

matrix = {"include": examples}
output = json.dumps(matrix)
# print("re.escape", re.escape(output))       # \{"include":\ \[\{"name":\ "bert/ptq_cpu",\ "config":\ "bert\\\\olive_ci_ptq_cpu\.json"\},\ \{"name":\ "phi3_5/qnn",\ "config":\ "phi3_5\\\\olive_ci_qnn\.json"\}\]\}
# print("shlex.quote", shlex.quote(output))   # '{"include": [{"name": "bert/ptq_cpu", "config": "bert\\olive_ci_ptq_cpu.json"}, {"name": "phi3_5/qnn", "config": "phi3_5\\olive_ci_qnn.json"}]}'
# print("json.dumps", json.dumps(output))     # {\"include\": [{\"name\": \"bert/ptq_cpu\", \"config\": \"bert\\\\olive_ci_ptq_cpu.json\"}, {\"name\": \"phi3_5/qnn\", \"config\": \"phi3_5\\\\olive_ci_qnn.json\"}]}
output = json.dumps(output)[1:-1]
print(f"::set-output name=matrix::{output}")
