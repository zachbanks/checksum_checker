from typing import Optional
import pyperclip
import typer

# TODO: Switch color output to use Rich
# from rich import print
from termcolor import colored

from src.hasher import Hasher


def main(
    test: str = typer.Argument(
        ...,
        help="Provide file path of file to check against source.",
        show_default=False,
        metavar="Test File",
    ),
    source: str = typer.Argument(
        pyperclip.paste(),
        help="Provide source SHA to test against test file. If not provided, will use system clipboard contents.",
        show_default="System clipboard contents",
        metavar="Source Hash",
    ),
    algorithm: str = typer.Option(
        Hasher.DEFAULT_ALGORITHM,
        "--algorithm",
        "-a",
        help=f"Choose hash algorithm to use: {Hasher.ALGORITHMS}",
    ),
) -> None:
    """
    Generates hash value for a specified file and compares it against a known value.
    Used to verify if software downloaded from internet has been maliciously modified
    or is not from the original source.
    """

    source = Hasher(hash=source, algorithm=algorithm)
    test = Hasher.generate_hash_from_file(test, algorithm=algorithm)

    # Colorize output and print to terminal
    result = source == test
    color = "green" if result else "red"

    result: str = str(result).upper()
    colored_result = colored(result, "black", f"on_{color}", attrs=["bold"])

    output = colored(f"[{algorithm}] {source} == {test}: ", color) + colored_result

    print(output)


if __name__ == "__main__":
    typer.run(main)
