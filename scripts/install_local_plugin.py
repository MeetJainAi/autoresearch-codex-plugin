#!/usr/bin/env python3
"""Install the local autoresearch Codex plugin into the user's home plugins directory."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


PLUGIN_NAME = "autoresearch-codex"
COPYTREE_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def install_plugin(repo_root: Path) -> tuple[Path, Path]:
    source = repo_root / "plugins" / PLUGIN_NAME
    if not source.exists():
        raise SystemExit(f"Plugin source not found: {source}")

    plugins_dir = Path.home() / "plugins"
    dest = plugins_dir / PLUGIN_NAME
    marketplace_path = Path.home() / ".agents" / "plugins" / "marketplace.json"

    plugins_dir.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest, ignore=COPYTREE_IGNORE)

    marketplace = load_json(marketplace_path)
    if not marketplace:
        marketplace = {
            "name": "local-codex-plugins",
            "interface": {"displayName": "Local Codex Plugins"},
            "plugins": [],
        }

    entry = {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./plugins/{PLUGIN_NAME}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Coding",
    }

    existing = [p for p in marketplace.get("plugins", []) if p.get("name") != PLUGIN_NAME]
    existing.append(entry)
    marketplace["plugins"] = existing
    save_json(marketplace_path, marketplace)
    return dest, marketplace_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, help="Repository root that contains plugins/autoresearch-codex")
    args = parser.parse_args()

    plugin_path, marketplace_path = install_plugin(Path(args.repo_root).resolve())
    print(f"Installed plugin: {plugin_path}")
    print(f"Updated marketplace: {marketplace_path}")
    print("Next step: open Codex and say 'Use $autoresearch-portable to bootstrap autoresearch in this repo.'")


if __name__ == "__main__":
    main()
