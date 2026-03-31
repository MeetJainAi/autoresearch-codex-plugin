# Local VPS Setup

This fork is configured for CPU, CUDA, and Apple Silicon local setups.

## Install

```bash
uv sync
```

Run the commands from the generated workspace root.

## Prepare a minimal cache

```bash
uv run prepare.py --num-shards 2
```

That downloads two training shards plus the pinned validation shard, then trains the tokenizer into `~/.cache/autoresearch/`.

## Baseline run

```bash
uv run train.py > run.log 2>&1
grep "^val_bpb:\|^peak_vram_mb:" run.log
```

## Useful overrides

```bash
AUTORESEARCH_DEVICE=cpu uv run train.py
AUTORESEARCH_DEVICE=mps uv run train.py
AUTORESEARCH_TIME_BUDGET=60 uv run train.py
AUTORESEARCH_MAX_SEQ_LEN=128 uv run train.py
AUTORESEARCH_EVAL_TOKENS=65536 uv run train.py
```

## If you later attach an NVIDIA GPU

`pyproject.toml` is generated for the detected machine profile during bootstrap. If you move the repo to a different class of machine later, regenerate it with the plugin bootstrap script or adjust the torch index manually before running `uv sync`.

## Codex prompt

```text
Read program.md and LOCAL_SETUP.md, verify the cache exists, create a fresh autoresearch-local/<today> branch, initialize results.tsv, run the baseline, and then start the experiment loop by editing only train.py.
```
