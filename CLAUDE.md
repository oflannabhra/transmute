# mtg (transmute-mtg)

State: `STATE.md` (facts), `work.yaml` (tasks; status lives only here),
`plans/` (how-to per task). The session brief is injected at start.

## Rules

- Python via uv only: `uv sync`, `uv run pytest`, `uv run ruff check --fix src/ tests/`,
  `uv run ruff format src/ tests/`. CI runs the same checks.
- New format: `FormatHandler` subclass in `src/transmute/formats/<name>.py`,
  register it in `formats/__init__.py`, add `tests/formats/test_<name>.py`,
  add a README row and CSV example.
- Releases are tag-driven (`git tag vX.Y.Z && git push origin vX.Y.Z`);
  never edit a version string. Never push or tag unless told.
- `~/Projects/transmute-web` pins `transmute-mtg>=1.0.0`; a breaking change
  to `Converter`, `FormatRegistry`, or the models needs a task there too.
