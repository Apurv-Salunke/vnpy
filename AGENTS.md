# Repository Guidelines

## Project Structure & Module Organization
- Core framework code lives in `vnpy/` (notably `vnpy/trader`, `vnpy/event`, `vnpy/chart`, `vnpy/rpc`, and `vnpy/alpha`).
- Optional app modules are maintained as sibling packages at repo root, e.g. `vnpy_ctastrategy/`, `vnpy_optionmaster/`, `vnpy_webtrader/`, each with its own `README.md`, `pyproject.toml`, and `script/run.py`.
- Tests are in `tests/` (currently focused on alpha factors in `tests/test_alpha101.py`).
- Examples and runnable demos are under `examples/`; architecture and contributor docs are in `docs/` and top-level `*.md` guides.

## Build, Test, and Development Commands
- Install locally (Linux): `bash install.sh`
- Install locally (macOS): `bash install_osx.sh`
- Editable dev install used by CI pattern: `uv pip install -e .[alpha,dev] --system`
- Lint: `ruff check .`
- Type-check: `mypy vnpy`
- Run tests: `pytest tests -q`
- Build distributions: `uv build`

Run lint and type checks before opening a PR; CI validates the same tools.

## Coding Style & Naming Conventions
- Python 3.10+; 4-space indentation; UTF-8 source files.
- Keep type hints complete for new/changed code (`mypy` is configured with strict options like `disallow_untyped_defs = true`).
- Follow Ruff rules configured in `pyproject.toml` (`B`, `E`, `F`, `UP`, `W`; `E501` ignored).
- Naming: `snake_case` for functions/modules, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.

## Testing Guidelines
- Framework: `pytest`.
- Place tests in `tests/` using `test_*.py` naming and `test_*` function/method names.
- Add or update tests with every behavior change, especially in data/alpha calculations.
- No fixed coverage threshold is enforced; submit meaningful assertions for edge cases and regressions.

## Commit & Pull Request Guidelines
- Commit style in history is mixed (`feat: ...`, `fix: ...`, `docs: ...`, and legacy `[Add]/[Mod]`). Prefer concise Conventional Commit-style prefixes.
- For large changes, open an issue first; keep PRs focused and small.
- Target the `dev` branch, include a clear change summary, and link related issues (e.g., `Close #123`).
- Ensure `ruff check .`, `mypy vnpy`, and relevant `pytest` commands pass before requesting review.
