"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Themester."""


if __name__ == "__main__":
    main(prog_name="themester")  # pragma: no cover
