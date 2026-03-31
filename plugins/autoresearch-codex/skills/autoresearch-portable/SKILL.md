---
name: autoresearch-portable
description: Use when the user wants to run or adapt karpathy/autoresearch inside Codex on a VPS, local Linux box, or Apple Silicon Mac, especially when they mention CPU-only, CUDA GPU, MPS, program.md, results.tsv, val_bpb, or an autonomous local experiment loop. This skill detects the local runtime, bootstraps a portable autoresearch workspace, and prepares the baseline Codex workflow.
---

# Portable Autoresearch

Bootstrap a Codex-ready autoresearch workspace that works on conservative local hardware, not just an H100. This skill packages a portable template plus scripts that detect whether the machine should use CPU, CUDA, or Apple Silicon defaults.

## Use This Skill For

- Running `karpathy/autoresearch` on a VPS or local workstation
- Adapting the workflow for CPU-only Linux hosts
- Setting up a safer default for small NVIDIA GPUs
- Bootstrapping Apple Silicon Macs with `mps` defaults
- Creating `program.md`, `LOCAL_SETUP.md`, `results.tsv`, and the baseline run loop for Codex

## Workflow

1. Detect the runtime first:

```bash
python3 scripts/detect_runtime.py
```

Run the command from this skill directory, or resolve the script path relative to this skill directory instead of guessing.

2. Choose the target repo:

- If the current directory already looks like autoresearch (`prepare.py`, `train.py`, `program.md`), bootstrap in place.
- Otherwise create a new workspace, usually `./autoresearch-portable`.

3. Run the bootstrap script:

```bash
python3 scripts/bootstrap_portable_autoresearch.py --dest <target-dir>
```

Default behavior:

- Tries to clone `https://github.com/karpathy/autoresearch` into the target when the directory does not exist yet
- Falls back to creating the directory locally if cloning is unavailable
- Overlays a portable template for `prepare.py`, `train.py`, `program.md`, `LOCAL_SETUP.md`, `.gitignore`, and `pyproject.toml`

4. Read the generated workspace files in the target repo:

- `program.md`
- `LOCAL_SETUP.md`
- `prepare.py`
- `train.py`

5. If the user wants to fully initialize the repo, run:

```bash
uv sync
uv run prepare.py --num-shards 2
test -f results.tsv || printf 'commit\tval_bpb\tmemory_gb\tstatus\tdescription\n' > results.tsv
uv run train.py > run.log 2>&1
```

6. If the user wants the autonomous loop, follow the generated `program.md` and only edit `train.py` during experiments.

## Runtime Rules

- Linux with `nvidia-smi`: configure CUDA wheels and default to `AUTORESEARCH_DEVICE=cuda`
- Linux without `nvidia-smi`: configure CPU wheels and default to `AUTORESEARCH_DEVICE=cpu`
- Apple Silicon: keep the default PyTorch package source and default to `AUTORESEARCH_DEVICE=mps`
- Unknown platforms: fall back to generic `torch==2.9.1` and `AUTORESEARCH_DEVICE=cpu`

## Files In This Skill

- `scripts/detect_runtime.py`: machine detection without requiring PyTorch
- `scripts/bootstrap_portable_autoresearch.py`: clone or create a workspace and overlay the portable template
- `assets/portable-template/`: the template files copied into the target autoresearch repo

## Constraints

- Keep `prepare.py` fixed after bootstrap unless the user explicitly wants to change the evaluation harness
- During experiment loops, only edit `train.py`
- Prefer conservative defaults that run on small hardware over aggressive defaults that only fit larger GPUs
