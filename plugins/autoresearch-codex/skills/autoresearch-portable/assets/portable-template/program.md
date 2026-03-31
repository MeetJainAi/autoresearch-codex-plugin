# autoresearch, local Codex edition

This fork is tuned for a local VPS, a small NVIDIA GPU, or an Apple Silicon Mac. It can run on CPU, CUDA, or MPS.

## Ground rules

1. Read `README.md`, `prepare.py`, and `train.py` before changing anything.
2. During the experiment loop, only edit `train.py`.
3. Treat `prepare.py` as fixed once setup is complete. It defines the runtime budget, sequence length, data loader, and evaluation metric for this fork.
4. Do not install new packages or change dependencies during the loop.
5. Keep `results.tsv` and `run.log` untracked.

## Local defaults

This fork intentionally uses lighter defaults than upstream:

- `MAX_SEQ_LEN=256`
- `TIME_BUDGET=120`
- `EVAL_TOKENS=131072`
- `DEPTH=4`
- `WINDOW_PATTERN="L"`
- CPU and MPS fallback with SDPA if flash-attention kernels are unavailable

These values can be overridden before a run with environment variables:

```bash
AUTORESEARCH_DEVICE=cpu
AUTORESEARCH_DEVICE=mps
AUTORESEARCH_MAX_SEQ_LEN=256
AUTORESEARCH_TIME_BUDGET=120
AUTORESEARCH_EVAL_TOKENS=131072
```

## Setup

Set up a new run like this:

1. Pick a fresh tag based on today's date, for example `mar30`.
2. Create a dedicated branch:

```bash
git checkout -b autoresearch-local/<tag>
```

3. Verify the cache exists in `~/.cache/autoresearch/`. If not, run:

```bash
uv run prepare.py --num-shards 2
```

4. Create `results.tsv` if it does not exist:

```text
commit	val_bpb	memory_gb	status	description
```

5. Run the untouched baseline once:

```bash
uv run train.py > run.log 2>&1
```

6. Parse the result:

```bash
grep "^val_bpb:\|^peak_vram_mb:" run.log
```

7. Commit the baseline `train.py` state so future kept runs have a stable parent commit.

## Logging

Log every run to `results.tsv` with tab separators:

```text
commit	val_bpb	memory_gb	status	description
```

- `commit`: 7-char short hash for kept runs, or the current `HEAD` short hash for discarded/crashed local attempts
- `val_bpb`: use `0.000000` for crashes
- `memory_gb`: `peak_vram_mb / 1024`, or `0.0` on CPU crashes
- `status`: `keep`, `discard`, or `crash`
- `description`: short plain-English summary

## Experiment loop

Repeat indefinitely:

1. Note the current kept baseline:

```bash
git rev-parse --short HEAD
```

2. Edit `train.py` with one clear idea.
3. Run:

```bash
uv run train.py > run.log 2>&1
```

4. If the run crashed, inspect:

```bash
tail -n 50 run.log
```

5. Record the result in `results.tsv`.
6. If `val_bpb` improved, commit the new `train.py`:

```bash
git add train.py
git commit -m "try: <short description>"
```

7. If it did not improve, restore `train.py` back to the kept commit:

```bash
git restore --source=HEAD -- train.py
```

## Research heuristics for this fork

- Prefer simple changes with measurable gains.
- Avoid H100-specific tricks unless they still help with SDPA or small GPUs.
- On CPU, favor smaller models, smaller total batch size, and fewer moving parts.
- Change one main variable at a time so the log stays interpretable.
- If a run takes far longer than the configured `TIME_BUDGET` plus startup/eval overhead, treat it as a failure and move on.
