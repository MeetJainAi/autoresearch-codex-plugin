#!/usr/bin/env python3
"""Detect the local runtime without requiring PyTorch to be installed."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys


def read_command_output(*cmd: str) -> str:
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
    return completed.stdout.strip()


def detect_runtime() -> dict:
    system = platform.system()
    machine = platform.machine().lower()
    nvidia_smi = shutil.which("nvidia-smi")
    gpu_name = ""
    if nvidia_smi:
        gpu_name = read_command_output(
            "nvidia-smi", "--query-gpu=name", "--format=csv,noheader"
        ).splitlines()[:1]
        gpu_name = gpu_name[0] if gpu_name else ""

    is_apple_silicon = system == "Darwin" and machine in {"arm64", "aarch64"}
    if nvidia_smi:
        device = "cuda"
        torch_profile = "linux-cuda"
    elif is_apple_silicon:
        device = "mps"
        torch_profile = "default"
    else:
        device = "cpu"
        torch_profile = "linux-cpu" if system == "Linux" else "default"

    result = {
        "platform": system,
        "machine": machine,
        "python": platform.python_version(),
        "recommended_device": device,
        "torch_profile": torch_profile,
        "has_nvidia_smi": bool(nvidia_smi),
        "gpu_name": gpu_name,
        "env": {
            "AUTORESEARCH_DEVICE": device,
            "AUTORESEARCH_MAX_SEQ_LEN": "256",
            "AUTORESEARCH_TIME_BUDGET": "120",
            "AUTORESEARCH_EVAL_TOKENS": "131072",
        },
    }
    result["summary"] = (
        f"{system} {machine}: use {device} with torch profile {torch_profile}"
        + (f" ({gpu_name})" if gpu_name else "")
    )
    return result


def format_shell(runtime: dict) -> str:
    lines = [f"export {key}={value}" for key, value in runtime["env"].items()]
    lines.append(f"# {runtime['summary']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("json", "text", "shell"),
        default="json",
        help="Output format",
    )
    args = parser.parse_args()

    runtime = detect_runtime()
    if args.format == "json":
        json.dump(runtime, sys.stdout, indent=2)
        sys.stdout.write("\n")
    elif args.format == "shell":
        print(format_shell(runtime))
    else:
        print(runtime["summary"])


if __name__ == "__main__":
    main()
