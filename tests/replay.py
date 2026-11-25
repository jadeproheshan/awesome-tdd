"""Replay saved sample outcomes; does not invoke an AI or prove general skill behavior."""
import json
from pathlib import Path
import subprocess
import sys

SCENARIOS = {
    # Current single-entry skill: fresh agent-created fixtures.
    "unified-cart": (7, 0, 0),
    "unified-points-review": (13, 29, 0),
    "unified-points-complete": (13, 0, 0),
    "unified-already-green": (2, 0, 0),
    "unified-read-only": (1, 1, 0),
    "unified-todo-review": (7, 0, 9),
    "unified-todo-complete": (7, 0, 0),
    # Historical sample regressions; not new single-entry agent evaluations.
    "booking": (6, 0, 0),
    "inventory-review": (10, 33, 0),
    "inventory-complete": (10, 0, 0),
    "red-already-green": (2, 0, 0),
    "verify-read-only": (1, 1, 0),
    "green-refactor": (2, 0, 0),
}
# A fresh process per fixture prevents same-named Python modules contaminating discovery.
RUN = '''import json, unittest
suite = unittest.defaultTestLoader.discover('.', pattern='test_*.py')
r = unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'tests': r.testsRun, 'failures': len(r.failures), 'errors': len(r.errors)}))
raise SystemExit(0 if r.wasSuccessful() else 1)
'''


def main():
    base = Path(__file__).resolve().parent / "scenarios"
    ok = True
    for name, expected in SCENARIOS.items():
        result = subprocess.run([sys.executable, "-B", "-c", RUN], cwd=base / name,
                                capture_output=True, text=True)
        try:
            counts = json.loads(result.stdout.strip())
            actual = (counts["tests"], counts["failures"], counts["errors"])
        except (ValueError, KeyError):
            actual = None
        expected_exit = int(bool(expected[1] or expected[2]))
        matched = actual == expected and result.returncode == expected_exit
        print(f'{"PASS" if matched else "FAIL"} {name}: {actual}, exit={result.returncode}')
        if not matched:
            print(result.stdout)
            print(result.stderr)
        ok = ok and matched
    print("Expected failing fixtures are intentional: review stop and read-only acceptance.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
