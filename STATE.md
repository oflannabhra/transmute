# STATE — mtg (transmute-mtg)

Facts only. Tasks and their status live in `work.yaml`; how-tos in `plans/`;
history in git. Task ids in parentheses point at `work.yaml`.

## What exists

- `transmute-mtg` on PyPI: CLI + library converting Magic: The Gathering
  collection CSVs between 16 formats (archidekt, cardkingdom, cardsphere,
  deckbox, deckbuilder, deckstats, dragonshield, helvault, manabox, moxfield,
  mtggoldfish, mtgmanager, mtgo, mtgstocks, mtgstudio, tcgplayer). Published
  versions: 0.1.0, 1.0.0. Latest tag `v1.0.0` (2026-01-28).
- GitHub repo `oflannabhra/transmute`; the local remote still points at the
  pre-rename name `git@github.com:oflannabhra/mtg-csv-converter.git`, which
  GitHub redirects. `flanhub/projects.yaml` registers this repo as `mtg`.
- Layout: `src/transmute/{cli.py,converter.py,core/,formats/,scryfall/}`.
  `core/models.py` (`Card`, `CardEntry`), `core/enums.py` (`Condition`,
  `Finish` nonfoil/foil/etched, `Language` ISO codes). Each format is a
  `FormatHandler` subclass in `formats/<name>.py` registered in
  `formats/__init__.py`; `FormatRegistry.detect_format` auto-detects from
  headers. `scryfall/api.py` rate-limits at 75 ms/request with a custom
  `User-Agent`; `scryfall/enrichment.py` fills missing set names, collector
  numbers, scryfall/oracle ids when `--scryfall` is passed.
- CLI (click): `transmute convert IN OUT -i FMT -o FMT [--scryfall]`,
  `transmute formats`, `transmute detect FILE`.
- Tests: `tests/` (pytest, 34 tests, coverage on by default via
  `addopts`). Format tests exist only for archidekt, helvault, moxfield,
  mtggoldfish; the other 12 handlers are covered only indirectly by
  `test_converter.py`.
- CI: `.github/workflows/ci.yml` runs ruff check, ruff format check, pytest
  with coverage upload to Codecov on push/PR to `main`. `release.yml` on
  `v*` tags: test → `uv build` → publish to PyPI via trusted publisher
  (GitHub environment `pypi`, OIDC, no token) → GitHub release with
  generated notes.
- Version is dynamic from git tags (`hatch-vcs`, `dynamic = ["version"]`);
  there is no version string in `pyproject.toml`.
- Downstream consumer: `~/Projects/transmute-web` (Litestar app) depends on
  `transmute-mtg>=1.0.0` and calls the library with `scryfall=False`.

## Decisions

- 2026-01-07 Rewrite from the 2021 single-script tool to a `src/` package
  with a `FormatHandler` ABC per format; publish as `transmute-mtg`.
- 2026-01-07 Releases are tag-driven through GitHub Actions with PyPI
  trusted publishing; no manual `twine`.
- 2026-01-28 Version comes from git tags via `hatch-vcs`, not from
  `pyproject.toml` (commit `32f4199`).
- 2026-01-28 MTGGoldfish handler follows the new export shape with
  `Collector Number` and `Scryfall ID` columns (issue #4, PR #5).

## Quirks

- The first two `v1.0.0` release runs failed before the dynamic-version fix
  landed; the tag was moved and the third run succeeded. Re-tagging is the
  recovery path if a release run fails.
- `.gitignore` still carries `test/output.csv` from the 2021 layout.
  Untracked local cruft from that era (`env/`, `test/`, root `transmute/`
  holding only `__pycache__`, `.vscode/`) is ignored by git and safe to
  delete.
- `README.md` and `CONTRIBUTING.md` clone URLs use `oflannabhra/transmute`,
  which matches GitHub; only the local remote uses the old name.
- Helvault output requires `scryfall_id`; converting to it without
  `--scryfall` from a source lacking the id produces empty ids.

## Secrets

- Secrets layout (flanhub sops-secrets, 2026-09-15): `.sops.yaml` + `.envrc`
  are in place; a `secrets.enc.yaml` (sops + age) appears with the first
  local secret and direnv exports it. Recipients: mac + CT 110.
- None in the repo. PyPI publishing uses OIDC trusted publishing (GitHub
  environment `pypi`); Codecov uses the repo secret `CODECOV_TOKEN`
  (upload failures do not fail CI).
