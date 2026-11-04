"""Command-line interface to the independent, offline capability graph planner."""
import argparse
import json
import sys
from pathlib import Path
from .engine import ManifestError, check, design, generate, parse_manifest


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("manifest", type=Path)
    gen_cmd = sub.add_parser("generate")
    gen_cmd.add_argument("manifest", type=Path)
    gen_cmd.add_argument("--out", required=True, type=Path)
    check_cmd = sub.add_parser("check")
    check_cmd.add_argument("directory", type=Path)
    args = p.parse_args(argv)
    try:
        if args.command == "check":
            failures = check(args.directory)
            if failures:
                print(json.dumps({"status": "fail", "findings": failures}, indent=2))
                return 1
            print(json.dumps({"status": "pass", "findings": []}, indent=2))
            return 0
        manifest = parse_manifest(args.manifest)
        plan = design(manifest) if args.command == "plan" else generate(manifest, args.out)
        print(json.dumps(plan, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
