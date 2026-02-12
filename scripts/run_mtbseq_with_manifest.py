#!/usr/bin/env python3
"""Thin MTBseq wrapper with structured logging and run manifest output."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_version_cmd(command: str) -> str:
    try:
        out = subprocess.check_output(["bash", "-lc", command], stderr=subprocess.STDOUT, text=True, timeout=10)
        first = out.strip().splitlines()
        return first[0] if first else ""
    except Exception as exc:  # noqa: BLE001
        return f"unavailable ({exc})"


def collect_versions() -> Dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "bwa": run_version_cmd("bwa 2>&1 | head -n 1"),
        "samtools": run_version_cmd("samtools --version 2>&1 | head -n 1"),
        "gatk3": run_version_cmd("gatk3 --version 2>&1 | head -n 1"),
        "picard": run_version_cmd("picard --version 2>&1 | head -n 1"),
        "java": run_version_cmd("java -version 2>&1 | head -n 1"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run MTBseq with structured JSONL logs and run manifest output.")
    parser.add_argument("--run-id", default=f"run-{uuid.uuid4().hex[:12]}", help="Unique run identifier.")
    parser.add_argument("--log-dir", default="modern_logs", help="Directory for log files.")
    parser.add_argument("--manifest", default="run.json", help="Path to run manifest JSON file.")
    parser.add_argument("--dry-run", action="store_true", help="Write manifest and exit without executing command.")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run, e.g. -- ./MTBseq --step TBfull")
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("Missing command. Example: modern_run_mtbseq.py -- ./MTBseq --step TBfull")
    return args


def main() -> int:
    args = parse_args()

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = log_dir / f"{args.run_id}.jsonl"
    plain_path = log_dir / f"{args.run_id}.log"
    manifest_path = Path(args.manifest)

    start_time = now_utc()
    versions = collect_versions()

    manifest = {
        "run_id": args.run_id,
        "start_time": start_time,
        "end_time": None,
        "duration_seconds": None,
        "cwd": os.getcwd(),
        "command": args.command,
        "command_shell": shlex.join(args.command),
        "dry_run": bool(args.dry_run),
        "exit_code": None,
        "versions": versions,
        "artifacts": {
            "jsonl_log": str(jsonl_path),
            "plain_log": str(plain_path),
        },
    }

    if args.dry_run:
        manifest["end_time"] = now_utc()
        manifest["duration_seconds"] = 0.0
        manifest["exit_code"] = 0
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"[dry-run] manifest written: {manifest_path}")
        return 0

    t0 = time.time()
    with plain_path.open("w", encoding="utf-8") as plain, jsonl_path.open("w", encoding="utf-8") as jsonl:
        proc = subprocess.Popen(
            args.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        assert proc.stdout is not None
        for line in proc.stdout:
            sys.stdout.write(line)
            plain.write(line)
            event = {
                "timestamp": now_utc(),
                "run_id": args.run_id,
                "stream": "stdout",
                "message": line.rstrip("\n"),
            }
            jsonl.write(json.dumps(event) + "\n")

        exit_code = proc.wait()

    manifest["exit_code"] = int(exit_code)
    manifest["end_time"] = now_utc()
    manifest["duration_seconds"] = round(time.time() - t0, 3)

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"manifest written: {manifest_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
