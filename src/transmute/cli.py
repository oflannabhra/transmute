"""Command-line interface for transmute."""

from pathlib import Path

import click
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from transmute.converter import Converter
from transmute.core.exceptions import TransmuteError
from transmute.formats import FormatRegistry

console = Console()


def get_format_choices() -> list[str]:
    """Get list of available formats for CLI choices."""
    return FormatRegistry.list_formats()


@click.group()
@click.version_option(package_name="transmute-mtg")
def cli() -> None:
    """Transmute - MTG Collection CSV Converter."""


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "-i",
    "--input-format",
    type=str,
    help="Input format (auto-detected if not specified)",
)
@click.option(
    "-o",
    "--output-format",
    type=str,
    required=True,
    help="Output format",
)
@click.option(
    "--scryfall/--no-scryfall",
    default=False,
    help="Fetch missing card data from Scryfall API",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show detailed progress",
)
def convert(
    input_file: Path,
    output_file: Path,
    input_format: str | None,
    output_format: str,
    scryfall: bool,
    verbose: bool,
) -> None:
    """
    Convert a collection CSV from one format to another.

    Examples:

        transmute convert collection.csv output.csv -o manabox

        transmute convert goldfish.csv helvault.csv -i mtggoldfish -o helvault --scryfall
    """
    # Validate formats
    available = get_format_choices()
    if input_format and input_format.lower() not in available:
        console.print(f"[red]Error:[/] Unknown input format: {input_format}")
        console.print(f"Available formats: {', '.join(available)}")
        raise SystemExit(1)
    if output_format.lower() not in available:
        console.print(f"[red]Error:[/] Unknown output format: {output_format}")
        console.print(f"Available formats: {', '.join(available)}")
        raise SystemExit(1)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
            disable=not verbose,
        ) as progress:
            task = progress.add_task("Converting...", total=100)

            def on_progress(stage: str, current: int, total: int) -> None:
                pct = (current / total) * 100 if total > 0 else 0
                progress.update(task, description=f"{stage}...", completed=pct)

            def on_error(entry, error) -> None:  # noqa: ANN001
                if verbose:
                    console.print(f"[yellow]Warning:[/] {entry.card.name}: {error}")

            converter = Converter(
                use_scryfall=scryfall,
                on_progress=on_progress,
                on_error=on_error,
            )

            converter.convert(
                input_path=input_file,
                output_path=output_file,
                input_format=input_format,
                output_format=output_format,
            )

        console.print(f"[green]Success![/] Converted to {output_file}")

    except TransmuteError as e:
        console.print(f"[red]Error:[/] {e}")
        raise SystemExit(1) from e


@cli.command("formats")
def list_formats() -> None:
    """List all supported CSV formats."""
    console.print("\n[bold]Supported Formats:[/]\n")

    for name in FormatRegistry.list_formats():
        handler = FormatRegistry.get(name)
        console.print(f"  [cyan]{name:15}[/] - {handler.display_name}")

    console.print()


@cli.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
def detect(file: Path) -> None:
    """Auto-detect the format of a CSV file."""
    handler = FormatRegistry.detect_format(file)

    if handler:
        console.print(f"Detected format: [cyan]{handler.display_name}[/] ({handler.name})")
    else:
        console.print("[yellow]Could not auto-detect format[/]")
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
