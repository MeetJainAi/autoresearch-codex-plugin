# Autoresearch Codex Plugin

Portable Codex plugin for running Karpathy-style autoresearch on local machines, VPSes, small NVIDIA GPUs, and Apple Silicon Macs.

## Status

Release target: `0.1.1`

Verified on `2026-03-31`:

- Linux CPU VPS
- install path
- runtime detection
- bootstrap into a fresh workspace
- `uv sync`
- `uv run prepare.py --num-shards 2`
- short `uv run train.py` smoke run

Not yet runtime-verified in this repository:

- Linux CUDA execution
- Apple Silicon MPS execution

Those paths are supported by the bootstrap logic, but they still need hardware-specific release testing before a broader stability claim.

## Install

From a checkout of this repository:

```bash
bash install.sh
```

Published-repo install pattern:

```bash
git clone <repo-url>
cd autoresearch-codex-plugin
bash install.sh
```

After the plugin is installed, restart Codex if needed and use:

```text
Use $autoresearch-portable to bootstrap autoresearch in this repo.
```

## What It Installs

- A local Codex plugin at `~/plugins/autoresearch-codex`
- A marketplace entry at `~/.agents/plugins/marketplace.json`
- A portable skill named `$autoresearch-portable`

## What The Skill Does

- Detects CPU, CUDA, or Apple Silicon runtime
- Clones or creates an autoresearch workspace
- Overlays a portable `prepare.py`, `train.py`, `program.md`, `LOCAL_SETUP.md`, `.gitignore`, and `pyproject.toml`
- Pins the generated workspace to the Python minor version used during bootstrap
- Leaves you with a Codex-friendly experiment loop for `results.tsv`, baseline runs, and iterative `train.py` edits

## Manual Verification Commands

These are the commands used for the current release check on the Linux CPU VPS:

```bash
cd ~/plugins/autoresearch-codex/skills/autoresearch-portable
python3 scripts/detect_runtime.py --format json
python3 scripts/bootstrap_portable_autoresearch.py --dest ~/workspace/autoresearch-plugin-verification
cd ~/workspace/autoresearch-plugin-verification
uv sync
uv run prepare.py --num-shards 2
AUTORESEARCH_TIME_BUDGET=10 AUTORESEARCH_EVAL_TOKENS=4096 uv run train.py > plugin-smoke.log 2>&1
grep -nE '^val_bpb:|^peak_vram_mb:' plugin-smoke.log
```

## Repository Layout

- `plugins/autoresearch-codex/.codex-plugin/plugin.json`: plugin manifest
- `plugins/autoresearch-codex/skills/autoresearch-portable/SKILL.md`: user-facing skill
- `plugins/autoresearch-codex/skills/autoresearch-portable/scripts/`: runtime detection and bootstrap scripts
- `install.sh`: local installer entrypoint
- `scripts/install_local_plugin.py`: copies the plugin into `~/plugins`
- `RELEASE_CHECKLIST.md`: pre-publish and publish steps

## Release Notes

`0.1.1` fixes the publishability issues found during the first verification pass:

- `python` commands changed to `python3` in skill docs
- machine-specific paths removed from generated docs
- `__pycache__` and `.pyc` files no longer copied into installs or generated workspaces
- generated workspaces now write `.python-version` from the bootstrap interpreter
- skill docs no longer overwrite an existing `results.tsv`

See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) before publishing.
