# Contributing to Transmute

## Development Setup

```bash
# Clone the repository
git clone https://github.com/oflannabhra/transmute.git
cd transmute

# Install dependencies (requires uv)
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/
```

## Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/formats/test_helvault.py

# Run without coverage
uv run pytest --no-cov
```

## Code Style

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. The configuration is in `pyproject.toml`.

```bash
# Check for issues
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/
```

## Adding a New Format

1. Create a new handler in `src/transmute/formats/`:

```python
from typing import ClassVar
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler

class MyFormatHandler(FormatHandler):
    name: ClassVar[str] = "myformat"
    display_name: ClassVar[str] = "My Format"
    required_columns: ClassVar[set[str]] = {"Name", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        # Parse CSV row into CardEntry
        ...

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        # Convert CardEntry to CSV row
        ...

    def get_headers(self) -> list[str]:
        return ["Name", "Quantity", ...]
```

2. Register the handler in `src/transmute/formats/__init__.py`

3. Add tests in `tests/formats/test_myformat.py`

4. Update the README with format documentation

## Release Process

Releases are automated via GitHub Actions. To create a new release:

1. Update the version in `pyproject.toml`
2. Commit the change: `git commit -am "Bump version to X.Y.Z"`
3. Create and push a tag: `git tag vX.Y.Z && git push origin vX.Y.Z`

The workflow will automatically:
- Run tests
- Build the package
- Publish to PyPI
- Create a GitHub release

## PyPI Trusted Publisher Setup

For maintainers setting up PyPI publishing for the first time:

1. Go to [PyPI](https://pypi.org) and log in
2. Navigate to your project → Publishing → Add a new publisher
3. Configure the trusted publisher:
   - **Owner**: `oflannabhra`
   - **Repository**: `transmute`
   - **Workflow name**: `release.yml`
   - **Environment**: `pypi`

4. In GitHub, create an environment named `pypi`:
   - Go to Repository Settings → Environments → New environment
   - Name it `pypi`
   - Optionally add protection rules (require approval, limit to tags)
