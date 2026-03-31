# Release Checklist

## Scope

This repository ships a local-install Codex plugin that bootstraps a portable autoresearch workspace.

Current intended release: `0.1.1`

## Pre-Release

- Confirm `plugins/autoresearch-codex/.codex-plugin/plugin.json` version matches the release tag.
- Confirm `README.md` status and verification notes match the latest test run.
- Confirm `LICENSE` is present and matches the plugin manifest license.
- Confirm no `__pycache__`, `.pyc`, `.venv`, or smoke-log artifacts are tracked.
- Confirm `install.sh` installs into `~/plugins/autoresearch-codex`.
- Confirm the installed skill can run `python3 scripts/detect_runtime.py --format json`.
- Confirm a fresh bootstrap works:
  - `python3 scripts/bootstrap_portable_autoresearch.py --dest <fresh-dir>`
- Confirm the generated workspace includes:
  - `program.md`
  - `LOCAL_SETUP.md`
  - `prepare.py`
  - `train.py`
  - `.python-version`
  - `pyproject.toml`
  - `results.tsv`
- Confirm `uv sync` succeeds in the generated workspace.
- Confirm `uv run prepare.py --num-shards 2` succeeds.
- Confirm a short smoke run succeeds:
  - `AUTORESEARCH_TIME_BUDGET=10 AUTORESEARCH_EVAL_TOKENS=4096 uv run train.py > plugin-smoke.log 2>&1`
  - `grep -nE '^val_bpb:|^peak_vram_mb:' plugin-smoke.log`

## Recommended Extra Matrix Before A Broader Release

- Test Linux with an exposed NVIDIA GPU.
- Test Apple Silicon with `mps`.
- Verify CUDA bootstrap selects the intended PyTorch index.
- Verify MPS bootstrap keeps the generic torch source and trains successfully.

## Publish

1. Initialize or update the git repository.
2. Commit the release candidate.
3. Create a tag matching the manifest version, for example `v0.1.1`.
4. Push the branch and tag to GitHub.
5. Publish release notes summarizing:
   - verified environments
   - known limitations
   - exact install command

## Post-Publish

- Re-run the install flow from a clean checkout of the public repo URL.
- Confirm the marketplace entry still points to `./plugins/autoresearch-codex`.
- Open a follow-up issue for CUDA and Apple Silicon runtime verification if they remain untested.
